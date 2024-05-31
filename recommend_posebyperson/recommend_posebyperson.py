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
        # 경로 매개변수 읽기
        num = event['pathParameters']['num']
        response = dynamodb.scan(
            TableName = 'capstone-test',
            FilterExpression = 'detected_count = :value',
            ExpressionAttributeValues = {':value' : {'N' : num }},
            ProjectionExpression = 'originalS3'
            )
            
        result_address = []
        for item in response['Items']:
            diffusion_address = item['originalS3']['S'].replace("original", "diffusion")
            result_address.append(diffusion_address)
            
        result = {
            'images' : result_address
        }    
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except JWTError as e:
        print("JWTError:", str(e))
        return {
            'statusCode': 401,
            'body': 'Unauthorized: Token verification failed'
        }
        