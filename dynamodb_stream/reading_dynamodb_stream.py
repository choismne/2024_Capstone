import json
import pymysql
import os

host = "capstone-mysql.cleikgoaszdk.ap-northeast-2.rds.amazonaws.com"
user = os.getenv('db_user_id')
password = os.getenv('db_user_password')
db_name = "fastapi"
conn = pymysql.connect(host=host, user=user, passwd=password, db=db_name, connect_timeout=5)

def get_db_connection():
    try:
        return pymysql.connect(host=host, user=user, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(f"ERROR: Could not connect to MySQL instance : {e}")
        raise

def lambda_handler(event, context):
    record = event
    if record['Records'][0]['eventName'] == 'INSERT':
        username = record["Records"][0]['dynamodb']['NewImage']['UserID']['S']
        detected_mood = record['Records'][0]['dynamodb']['NewImage']['detected_mood']['SS']
        detected_pose = record['Records'][0]['dynamodb']['NewImage']['detected_pose']['SS']
        miso_point = record["Records"][0]['dynamodb']['NewImage']['miso_point']['N']
        
        allowed_moods_columns = {
            'lovely': 'lovely_count',
            'cheerful': 'cheerful_count',
            'cute': 'cute_count',
            'playful': 'playful_count',
            'harmonious': 'harmonious_count',
            'scary': 'scary_count'
        }
        
        allowed_poses_columns = {
            'v_pose': 'v_pose_count',
            'flower_pose': 'flower_pose_count',
            'heart_pose': 'heart_pose_count',
            'arms_crossed': 'arms_crossed_count',
            'kiss_pose': 'kiss_pose_count',
            'thumbs_up': 'thumbs_up_count',
            'wink': 'wink_count'
        }
                
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                #moods 테이블 업데이트
                for mood in detected_mood:
                    if mood in allowed_moods_columns:
                        target = allowed_moods_columns[mood]
                        query = f"UPDATE moods SET {target} = {target} + 1 WHERE username = %s"
                        cur.execute(query, (username,))
                    else:
                        print("Invalid mood type")
                #poses 테이블 업데이트    
                for pose in detected_pose:
                    if pose in allowed_poses_columns:
                        target = allowed_poses_columns[pose]
                        query = f"UPDATE poses SET {target} = {target} + 1 WHERE username = %s"
                        cur.execute(query, (username,))
                    else:
                        print("Invalid mood type")
                #users 테이블 업데이트
                query = f"UPDATE users SET total_miso = total_miso + {miso_point} WHERE username = %s"
                cur.execute(query, (username,))
                
                
        except pymysql.MySQLError as e:
                print(f"ERROR: Unexpected error: Could not connect to MySQL instance. {e}")
                return {
                    'statusCode': 500,
                    'body': 'Connection failed.'
                }
        finally:
            conn.close()
            print("Successfully update!")
        