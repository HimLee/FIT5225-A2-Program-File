import json
import base64
import boto3

from detectfolder import detect

# Function for 3.2.2 (Find images based on the tags of an image)

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
TABLE_NAME = 'assignment2tags'
image_bucket = 'my-a2-bucket'
yolo_bucket = 'detectyoloconfigs'


def handle_postimage(event):
    imagedata = event['body']
    image_data = imagedata.split(',')[1]
    image = base64.b64decode(image_data)
    tags = detect.detect_image(image)
    print(tags)
    targetTags = "Upload image's tags: ", tags
    response = dynamodb.scan(TableName=TABLE_NAME)
    items = response.get('Items')
    result = []
    for i in items:
        item_tags = i.get('tags').get('L')
        for d in item_tags or []:
            tag = d.get('S')

            if tag in tags:
                url = i.get('s3-url')
                corresponding_tags = i.get('tags')
                url.update(corresponding_tags)
                result.append(url)

    return targetTags, {'Result': result}


def lambda_handler(event, context):
    # TODO implement
    response_image = handle_postimage(event)
    return {
        'statusCode': 200,
        'body': json.dumps(response_image)
    }
