import psycopg2
import psycopg2.extras
import time
from sshtunnel import SSHTunnelForwarder
from app.tools.file_handler import get_json
from app.tools.system_handler import default_exception_handler


db_conf = {}


def init_db_conf(server):
    global db_conf
    db_conf = get_json(relative_path='config/db_conf.json', default_data={})[server]


@default_exception_handler
def create_db_connection(user):
    connection = psycopg2.connect(
        dbname=db_conf[user]['dbname'],
        user=db_conf[user]['user'],
        password=db_conf[user]['user_password'],
        host=db_conf[user]['host'])
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return connection, cursor


@default_exception_handler
def create_db_connection_tunnel(user):
    server = SSHTunnelForwarder(
        (db_conf[user]['host'], 22),
        ssh_username=db_conf[user]['ssh_username'],
        ssh_password=db_conf[user]['ssh_password'],
        remote_bind_address=('localhost', 5432))

    server.start()

    local_port = str(server.local_bind_port)
    connection = psycopg2.connect(
        dbname=db_conf[user]['dbname'],
        user=db_conf[user]['user'],
        password=db_conf[user]['user_password'],
        host=db_conf[user]['host'],
        port=local_port)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return connection, cursor


def reconnect_to_db(user, cron):
    while True:
        try:
            connection, cursor = create_db_connection(user)
            return connection, cursor
        except Exception:
            time.sleep(cron)
            continue
