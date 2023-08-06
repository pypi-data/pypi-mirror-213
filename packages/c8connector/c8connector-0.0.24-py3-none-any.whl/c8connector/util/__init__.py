#  Copyright (c) 2023 Macrometa Corp All rights reserved.
import json
import os
import time

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.pool import SimpleConnectionPool
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class DB:
    def __init__(
            self, user: str, password: str, host: str, port: str, database: str = 'c8cws'
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.try_create_tables(database, host, password, port, user, 20)
        self.pool = SimpleConnectionPool(
            1, 25, user=user,
            password=password,
            host=host,
            port=port,
            database=database)

    @staticmethod
    def try_create_tables(database, host, password, port, user, max_tries):
        cursor, con = None, None
        backoff = 2
        done = False
        for i in range(max_tries):
            backoff = (i + 1) * backoff
            try:
                con = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = con.cursor()
                cursor.execute("CREATE TABLE workflow (uuid TEXT PRIMARY KEY, federation TEXT,"
                               " tenant TEXT, fabric TEXT, bin_workflow BYTEA, state JSONB);")
                done = True
            except OperationalError as e:
                print(f"Unable to connect to the central cloud RDS. {str(e).capitalize().strip()}."
                      f" Retrying in {backoff} seconds ...")
                time.sleep(backoff)
                continue
            except Exception as e:
                print(f"Skipping tables creation. {str(e).capitalize().strip()}.")
                done = True
                break
            finally:
                if cursor is not None:
                    cursor.close()
                if con is not None:
                    con.close()
        if not done:
            raise RuntimeError(f"Unable to connect to the central cloud RDS. "
                               f"Please check RDS connectivity and configurations.")

    def close(
            self
    ) -> None:
        self.pool.closeall()

    def update_state(self, uuid: str, state: object):
        state_json = json.dumps(state)
        conn = self.pool.getconn()
        cursor = conn.cursor()
        query = """
            UPDATE workflow
            SET state = %s
            WHERE uuid = %s;
        """
        cursor.execute(query, (state_json, uuid))
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    def get_state(self, uuid: str):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        query = """
            SELECT state
            FROM workflow
            WHERE uuid = %s;
        """
        cursor.execute(query, (uuid,))
        result = cursor.fetchone()
        cursor.close()
        self.pool.putconn(conn)
        if result is not None and result[0] is not None:
            return result[0]
        else:
            return None


class StateFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('state.json'):
            save_state()


uuid = os.getenv("WORKFLOW_UUID")
state_save_interval = os.getenv("STATE_SAVE_INTERVAL", 60)
state_file_dir = os.getenv("STATE_DIR", "/project/eltworkflow/state")

db = DB(
    user=os.getenv("RDS_USER"),
    password=os.getenv("RDS_PASSWORD"),
    host=os.getenv("RDS_HOST"),
    port=os.getenv("RDS_PORT"),
    database=os.getenv("RDS_DATABASE", "c8cws")
)


def load_state():
    # Read from the db and write the state into state.json file.
    print(f"Loading the state of workflow {uuid} from the database.")
    try:
        state_content = db.get_state(uuid)
        if state_content:
            with open(f"{state_file_dir}/state.json", "w") as state_file:
                json.dump(state_content, state_file)
    except Exception as e:
        print(f"Couldn't load state of {uuid} from database. {e}")
        return


def save_state():
    # Read the state.json file and write the state to the DB.
    print(f"Saving the state of workflow {uuid} to the database.")
    try:
        with open(f"{state_file_dir}/state.json", "r") as state_file:
            state_content = json.load(state_file)
            if state_content:
                db.update_state(uuid, state_content)
    except Exception as e:
        print(f"Couldn't persist state of {uuid} to database. {e}")
        return


def start_state_observer():
    event_handler = StateFileHandler()
    observer = Observer()
    observer.schedule(event_handler, state_file_dir, recursive=False)
    print(f"Starting state observer on `{state_file_dir}/state.json`")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
