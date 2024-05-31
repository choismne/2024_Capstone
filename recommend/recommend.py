import json
from jose import jwt, JWTError
import pymysql
import os
import boto3

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
host = "capstone-mysql.cleikgoaszdk.ap-northeast-2.rds.amazonaws.com"
user = os.getenv('db_user_id')
password = os.getenv('db_user_password')
db_name = "fastapi"
conn = pymysql.connect(host=host, user=user, passwd=password, db=db_name, connect_timeout=5)
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    jwt_token = event['headers']['Authorization']
    token = jwt_token.split(" ")[1]
    try: 
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded['sub']
        try:
            # poses테이블에서 제일 적게 한 포즈를 횟수와, 포즈 이름을 잡아옵니다. 
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM poses WHERE username = %s;", (username,))
                pose_status = list(cur.fetchone())[1:]
                
                pose_keys = [
                    "v_pose",
                    "flower_pose",
                    "heart_pose",
                    "arms_crossed",
                    "kiss_pose",
                    "thumbs_up",
                    "wink"
                ]
                pose_dict = {key: value for key, value in zip(pose_keys, pose_status)}
                
                cur.execute("SELECT * FROM moods WHERE username = %s;", (username,))
                mood_status = list(cur.fetchone())[1:]
                
                mood_keys = [
                    "lovely",
                    "cheerful",
                    "cute",
                    "playful",
                    "harmonious",
                    "scary"
                ]
                
                mood_dict = {key: value for key, value in zip(mood_keys, mood_status)}
                
                cur.execute("""
                SELECT 
                    LEAST(v_pose_count, flower_pose_count, heart_pose_count, arms_crossed_count, kiss_pose_count, thumbs_up_count, wink_count) AS smallest_value,
                    CASE LEAST(v_pose_count, flower_pose_count, heart_pose_count, arms_crossed_count, kiss_pose_count, thumbs_up_count, wink_count)
                        WHEN v_pose_count THEN 'v_pose_count'
                        WHEN flower_pose_count THEN 'flower_pose_count'
                        WHEN heart_pose_count THEN 'heart_pose_count'
                        WHEN arms_crossed_count THEN 'arms_crossed_count'
                        WHEN kiss_pose_count THEN 'kiss_pose_count'
                        WHEN thumbs_up_count THEN 'thumbs_up_count'
                        WHEN wink_count THEN 'wink_count'
                        ELSE 'Unknown'
                    END AS smallest_column_name
                FROM 
                    poses
                WHERE
                    username = %s;""", (username,))
                minimum_pose = cur.fetchone()
                
                #moods테이블에서 제일 적게한 무드를 횟수와, 무드 이름으로 잡아옵니다. 
                cur.execute("""
                SELECT 
                    LEAST(lovely_count, cheerful_count, cute_count, playful_count, harmonious_count, scary_count) AS smallest_value,
                    CASE LEAST(lovely_count, cheerful_count, cute_count, playful_count, harmonious_count, scary_count)
                        WHEN lovely_count THEN 'lovely_count'
                        WHEN cheerful_count THEN 'cheerful_count'
                        WHEN cute_count THEN 'cute_count'
                        WHEN playful_count THEN 'playful_count'
                        WHEN harmonious_count THEN 'harmonious_count'
                        WHEN scary_count THEN 'scary_count'
                        ELSE 'Unknown'
                    END AS smallest_column_name
                FROM 
                    moods
                WHERE 
                    username = %s;""", (username,))
                minimum_mood = cur.fetchone()

            conn.close()
            
            minimum_pose_name = str(minimum_pose[1])[:-6]
            minimum_mood_name = str(minimum_mood[1])[:-6]
            
            response = dynamodb.scan(
                TableName='capstone-test',
                FilterExpression='contains(detected_mood, :mood) AND contains(detected_pose, :pose)',
                ExpressionAttributeValues={
                    ':mood': {'S': minimum_mood_name},
                    ':pose': {'S': minimum_pose_name}
                },
                ProjectionExpression='originalS3'
                )
                
            result_address = []
            for item in response['Items']:
                diffusion_address = item['originalS3']['S'].replace("original", "diffusion")
                result_address.append(diffusion_address)
            
            
            result = {
                'pose_status':pose_dict,
                'mood_status':mood_dict,
                'minimum_pose':{
                    'pose_count':minimum_pose[0],
                    'pose_name':minimum_pose_name
                    },
                'minimum_mood':{
                    'mood_count':minimum_mood[0],
                    'mood_name':minimum_mood_name
                    },
                'recommend_images': result_address
            }
            
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        except pymysql.MySQLError as e:
            print("ERROR: Unexpected error: Could not connect to MySQL instance.")
            print(e)
            return {
                'statusCode': 500,
                'body': 'Connection failed.'
            }
            
    except JWTError as e:
        print("JWTError:", str(e))
        return {
            'statusCode': 401,
            'body': 'Unauthorized: Token verification failed'
        }
    


    