import json
from jose import jwt, JWTError
import boto3
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    jwt_code = event['headers']['Authorization']
    token = jwt_code.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded['sub']
    
        json_string = event['body']
        data = json.loads(json_string)
        original_url = data['originalS3']
        smile_url = original_url.replace("original", "smile")

        response = dynamodb.scan(
            TableName='capstone-test',
            FilterExpression='UserID = :userVal AND originalS3 = :s3Val',
            ExpressionAttributeValues={
                ':userVal': {'S' : username},
                ':s3Val' : {'S' : original_url}
            }
        )
        miso_point = int(response['Items'][0]['miso_point']['N'])
        
        result = {
            'original_url': original_url,
            'smile_url': smile_url,
            'miso_point': miso_point
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)  # JSON 직렬화를 추가했습니다.
        }

    except JWTError as e:
        print("JWTError:", str(e))
        return {
            'statusCode': 401,
            'body': 'Unauthorized: Token verification failed'
        }