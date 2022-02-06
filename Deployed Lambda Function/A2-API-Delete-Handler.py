import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# Function for 3.2.4 (Delete an image)

def lambda_handler(event, context):
    if event['httpMethod'] == 'DELETE':
        """
        Delete items in S3 and DynamoDB, using the url as the primary key
        :param event: The url that we want to delete
        :param context: I dont know, you google yourself
        :return: The stringify version of the [response] variable
        """

        # Defining the variables for connecting to the database
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('assignment2tags')  # The name of the DynamoDB table
        s3 = boto3.resource('s3')

        try:
            # Delete item from DynamoDB
            # responseDB = table.delete_item(Key={'s3-url': event['s3-url']})
            # table.delete_item(Key={'s3-url': event['s3-url']})

            # x = responseDB
            x = event['queryStringParameters']['s3-url']

            table.delete_item(Key=event['queryStringParameters'])

            # # Delete the item from S3 Bucket || The event['id'][38:] is used to remove the first 38 char of the url
            # # This is because when deleting item from S3, we just need the object name, and not the full url as key
            responseS3 = s3.Object('my-a2-bucket', event['queryStringParameters']['s3-url']).delete()

            # # Printing the response out (for debugging)
            # print("DynamoDB Response: ", responseDB)
            # print("S3 Response", responseS3)

            # # This is currently responding a string
            # # return str(responseS3)
            return {
                'statusCode': 200,
                'body': json.dumps(event['queryStringParameters'])

            }
            # return

        # Error handling
        except ClientError as e:
            print(e)
            return responseDB
