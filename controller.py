import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from swagger_server import models

sys.path.append(OPENAPI_STUB_DIR)
pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)
def get_all_weather():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, temp, humid, pm2_5
            FROM data_collection
        """)
        result = [models.Items(*row) for row in cs.fetchall()]
        return result

def get_game_name(game_name):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, name, player
            FROM Steam_game
            WHERE name=%s
        """, [game_name])
        result = [models.Games(*row) for row in cs.fetchall()]
        return result

def get_weather_day(day):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, temp, humid, pm2_5
            FROM data_collection
            WHERE DATE(ts) = %s
        """, (str(day),))
        result = [models.Items(*row) for row in cs.fetchall()]
        return result

def get_game_day(day):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, name, player
            FROM Steam_game
            WHERE DATE(ts) = %s
        """, (str(day),))
        result = [models.Games(*row) for row in cs.fetchall()]
        return result

def get_game_time(time):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, name, player
            FROM Steam_game
            WHERE TIME(ts) = %s
        """, (str(time),))
        result = [models.Games(*row) for row in cs.fetchall()]
        return result

def get_weather_time(time):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, temp, humid, pm2_5
            FROM data_collection
            WHERE TIME(ts) = %s
        """, (str(time),))
        result = [models.Items(*row) for row in cs.fetchall()]
        return result

def get_all_games():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, name, player
            FROM Steam_game
        """)
        result = [models.Games(*row) for row in cs.fetchall()]
        return result
