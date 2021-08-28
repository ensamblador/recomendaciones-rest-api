import json
import os
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    REGION =os.environ.get('REGION')
    CAMPAIN_ARN = os.environ.get('CAMPAIN_ARN')

    # ** --------------------------------
    # ** RERANK ITEMS
    # ** --------------------------------

    pathParameters = event['pathParameters']

    if not 'userId' in pathParameters:
        return build_response(400, 'Falta userId')

    userId = pathParameters['userId']
    body = json.loads(event['body'])

    keys = body.keys()

    filter_arn = None
    if 'filterArn' in body:
        filter_arn = body['filterArn']


    if not len(keys):
        return build_response(400, 'se requiere listado de items inputList[l1,l2...')

    if not ('inputList' in body):
        return build_response(400, 'se requiere listado de items inputList[l1,l2...')
    input_list = body['inputList']

    if len(input_list) == 0:
        return build_response(400, 'se requiere listado de items inputList[l1,l2...')
    
    print (event)

    personalize_runtime = boto3.client('personalize-runtime', region_name=REGION)

    try:
        args = dict(
            campaignArn = CAMPAIN_ARN,
            userId = str(userId),
            inputList = input_list
        )
        if filter_arn:
            args = dict(
                campaignArn = CAMPAIN_ARN,
                userId = str(userId),
                inputList = input_list,
                filterArn = filter_arn)
        get_recommendations_response = personalize_runtime.get_personalized_ranking(
            **args
        )
        print (get_recommendations_response)
        return build_response(200, get_recommendations_response)
    except ClientError as error:
        print (error.response['Error']['Code'], error.response['Error'])
        return build_response(error.response['Error']['Code'], error.response['Error'])
    except BaseException as error:
        print("Unknown error while executing: " + error.response['Error']['Message'])
        build_response(500, error.response['Error'])



def build_response(status_code, json_content):
        return {
        'statusCode': status_code,
        "headers": {
            "Access-Control-Allow-Origin":"*",
			"Content-Type": "application/json",
			"Access-Control-Allow-Methods" : "GET, OPTIONS, POST, DELETE",
        },
        'body': json.dumps({'data':json_content})
    }
