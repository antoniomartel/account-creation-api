
import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('accounts')

sns = boto3.client('sns')
TOPIC_ARN = os.environ['AUDIT_SNS_TOPIC_ARN']

def publish_event(event_type, actor_id, account_id, payload):
    message = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "actor_id": actor_id,
        "account_id": account_id,
        "payload": payload
    }
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(message)
    )

def lambda_handler(event, context):
    print("Received event:", event)

    method = event.get('httpMethod')
    path = event.get('resource')
    user_id = event['headers'].get('x-user-id', 'unknown')

    if method == 'POST' and path == '/accounts':
        try:
            body = json.loads(event.get('body', '{}'))
            name = body.get('name')
            parent_id = body.get('parent_id')
            metadata = body.get('metadata', {})

            if not name:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing "name"'})
                }

            account_id = str(uuid.uuid4())
            item = {
                'account_id': account_id,
                'name': name,
                'parent_id': parent_id,
                'metadata': metadata,
                'version': 1
            }

            table.put_item(Item=item)

            publish_event(
                event_type='ACCOUNT_CREATED',
                actor_id=user_id,
                account_id=account_id,
                payload=item
            )

            return {
                'statusCode': 201,
                'body': json.dumps({'message': 'Account created', 'account': item})
            }

        except Exception as e:
            print("Error:", str(e))
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
            }

    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not found'})
    }