import mysql.connector
import redis

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="task_manager"
)

r = redis.Redis(
    host = "localhost",
    port = 6379,
    db = 0,
    decode_responses = True
)


cursor = conn.cursor()