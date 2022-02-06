import json

import boto3

# Function for 3.2.1 ( Find images based on the tags)

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
TABLE_NAME = 'assignment2tags'
image_bucket = 'my-a2-bucket'
yolo_bucket = 'detectyoloconfigs'


def handle_postimage(event):
    parameters = event.get('queryStringParameters')
    search_tags = parameters.get('tags')
    # return list(search_tags)
    response = dynamodb.scan(TableName=TABLE_NAME)
    items = response.get('Items')
    urls = []
    for i in items:
        item_tags = i.get('tags').get('L')
        for d in item_tags or []:
            tag = d.get('S')
            if tag in search_tags:
                url = i.get('s3-url').get('S')
                new_url = 'https://my-a2-bucket.s3.amazonaws.com/' + url
                urls.append(new_url)

    return {"links": urls}


def lambda_handler(event, context):
    # TODO implement
    httpMethod = event.get('httpMethod')
    print(httpMethod)
    response_image = handle_postimage(event)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*"
        },
        'body': json.dumps(response_image)
    }
