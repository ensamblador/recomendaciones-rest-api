import json
import os
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    REGION =os.environ.get('REGION')
    CAMPAIN_ARN = os.environ.get('CAMPAIN_ARN')
    FILTERS_STR = os.environ.get('FILTERS')
    FILTERS = []
    if FILTERS_STR is not None:
        FILTERS = json.loads(FILTERS_STR)

    # ** --------------------------------
    # ** OBTENER ITEMS SIMILARES
    # ** --------------------------------

    pathParameters = event['pathParameters']

    if not 'itemId' in pathParameters:
        return build_response(500, 'Falta itemId')

    itemId = pathParameters['itemId']
    
    filter_arn = None

    qs_params = event['queryStringParameters']

    if (qs_params is not None) and ('filter' in qs_params):
        filter_arn =  get_filter_arn(FILTERS, qs_params['filter'])
        if filter_arn is None: 
            return build_response(400, 'Invalid Filter Name')

    numResults = 25
    if (qs_params is not None) and ('numResults' in qs_params):
        numResults = int(qs_params['numResults'])

    personalize_runtime = boto3.client('personalize-runtime', region_name=REGION)

    try:
        args = dict(
            campaignArn = CAMPAIN_ARN,
            numResults = numResults,
            itemId = str(itemId),
        )
        if filter_arn:
            args = dict(
            campaignArn = CAMPAIN_ARN,
            itemId = str(itemId),
            numResults = numResults,
            filterArn = filter_arn
        )
        get_recommendations_response = personalize_runtime.get_recommendations(
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

def get_filter_arn(filter_list, filter_name):
    for f in filter_list:
        if f['name'] == filter_name:
            return f['filterArn']
    return None

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
