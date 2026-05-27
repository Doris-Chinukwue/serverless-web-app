import json
import boto3
import uuid

def lambda_handler(event, context):

    # Read the data from the form submissiong
    body= json.loads(event['body'])
    name= body['name']
    message = body['message']

    # Genrate a unique ID for this submission
    submission_id = str(uuid.uuid4())

    # Connect to DynamoDB and write the data
    dynamodb =  boto3.resource('dynamodb')
    table = dynamodb.Table('FormSubmissions')  

    table.put_item(
        Item={
            'submissionId': submission_id,
            'name': name,
            'message': message
        }
    )
   
   # Return a success response
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps('Form submitted successfully')
    }
