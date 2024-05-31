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

        response = dynamodb.scan(
            TableName='capstone-test',
            FilterExpression='UserID = :val',
            ExpressionAttributeValues={':val': {'S' : username}}
        )
        result = []
        for item in response['Items']:
            result.append(item['originalS3']['S'])

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