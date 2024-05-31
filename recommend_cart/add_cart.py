import json
from jose import jwt, JWTError
import boto3
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
dynamodb = boto3.client('dynamodb')

def put_item(username, url):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName='cart_list',
        Item={
            'username': {'S': username},
            'cart': {'SS': [url]}
        }
    )
    return response

def update_item(username, url):
    response = dynamodb.update_item(
        TableName='cart_list',
        Key={
            'username': {'S': username}
        },
        UpdateExpression='ADD cart :new_value',
        ExpressionAttributeValues={
            ':new_value': {'SS': [url]}
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def id_check(username):
    response = dynamodb.get_item(
        TableName='cart_list',
        Key={
            'username': {'S': username}
        }
    )
    if 'Item' in response:
        print("Found item:", response['Item'])
        return True
    else:
        print("No item found for username:", username)
        return False

def lambda_handler(event, context):
    jwt_code = event['headers']['Authorization']
    token = jwt_code.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded['sub']
        
        json_string = event['body']
        data = json.loads(json_string)
        print(data)
        url = data['url']
        
        if id_check(username):
            update_item(username, url)
        else:
            put_item(username, url)
            
        return {
            'statusCode': 200,
            'body': json.dumps('Update Success')
        }
    except JWTError as e:
        print("JWTError:", str(e))
        return {
            'statusCode': 401,
            'body': 'Unauthorized: Token verification failed'
        }
        