import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# Defining the variables for connecting to the database
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('assignment2tags')  # The name of the DynamoDB table

# Function for 3.2.3 (Remove tags from an image)

def lambda_handler(event, context):
    """
    This function is used to delete items by using the update_item method
    :param event: The JSON variables passed in
    :param context:
    :return: Response variable
    """
    try:
        # temp = event['body']
        jsonObject = json.loads(event['body'])
        idkey = jsonObject['s3-url']
        idKeyJson = {'s3-url': "{}".format(idkey)}

        currentList = table.get_item(Key=idKeyJson)['Item']['tags']
        removeItemList = jsonObject['tags']
        newList = remove_item_from_list(removeItemList, currentList)

        response = table.update_item(
            Key=idKeyJson,

            UpdateExpression="set tags=:r",

            ExpressionAttributeValues={
                ':r': newList
            },

            ReturnValues="UPDATED_NEW"
        )

        data_set = {"current List": currentList, "remove Item List": removeItemList, "update List": newList}

        return {
            'statusCode': 200,
            'body': json.dumps(data_set)
        }

    # Error handling
    except ClientError as e:
        print(e)


def remove_item_from_list(removeItemList, currentList):
    """
    This function will remove the unwanted items from the current list
    :param removeItemList: The items that we want to remove
    :param currentList: The original list from DynamoDB
    :return: The newly updated list
    """

    updatedList = [e for e in currentList if e not in removeItemList]

    return updatedList
