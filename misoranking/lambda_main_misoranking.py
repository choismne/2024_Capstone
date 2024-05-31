import json
from jose import jwt, JWTError
import pymysql
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
host = "capstone-mysql.cleikgoaszdk.ap-northeast-2.rds.amazonaws.com"
user = os.getenv('db_user_id')
password = os.getenv('db_user_password')
db_name = "fastapi"
conn = pymysql.connect(host=host, user=user, passwd=password, db=db_name, connect_timeout=5)

def lambda_handler(event, context):
    jwt_token = event['headers']['Authorization']
    token = jwt_token.split(" ")[1]
    try: 
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded['sub']
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT total_miso FROM users WHERE username = %s;", (username,))
                total_miso = cur.fetchone()
                
                cur.execute("SELECT username, total_miso FROM users ORDER BY total_miso")
                ranking = cur.fetchmany(10)
            conn.close()
            
            result = {
                'username' : username,
                'total_miso': total_miso[0],
                'ranking' : ranking
                }
            return {
                'statusCode':200,
                'body':json.dumps(result)
                }
        except pymysql.MySQLError as e:
            print("ERROR: Unexpected error: Could not connect to MySQL instance.")
            print(e)
            return {
                'statusCode' : 500,
                'body':'Connection failed.'
                }
            
    except JWTError as e:
        print("JWTError:", str(e))
        return {
            'statusCode': 401,
            'body': 'Unauthorized: Token verification failed'
        }