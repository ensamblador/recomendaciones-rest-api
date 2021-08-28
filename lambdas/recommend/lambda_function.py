import json
import os
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    REGION =os.environ.get('REGION')
    CAMPAIN_ARN = os.environ.get('CAMPAIN_ARN')
    print (event)
    # ** --------------------------------
    # ** OBTENER RECOMENDACION
    # ** --------------------------------

    pathParameters = event['pathParameters']

    if not 'clientId' in pathParameters:
        return build_response(500, 'Falata clientId')

    clientId = pathParameters['clientId']
    
    filter_arn = None

    if ('body' in event) and (event['body'] is not None):
        body = json.loads(event['body'])
        keys = body.keys()
        if len(keys):
            if 'filterArn' in body:
                filter_arn = body['filterArn']

    print (event)

    personalize_runtime = boto3.client('personalize-runtime', region_name=REGION)

    try:
        args = dict(
            campaignArn = CAMPAIN_ARN,
            userId = str(clientId)
        )
        if filter_arn:
            args = dict(campaignArn = CAMPAIN_ARN, userId = str(clientId), filterArn = filter_arn)
        get_recommendations_response = personalize_runtime.get_recommendations(
            **args)
        print (get_recommendations_response)
        return build_response(200, get_recommendations_response)
    except ClientError as error:
        print (error.response['Error']['Code'], error.response['Error'])
        return build_response(error.response['Error']['Code'], error.response['Error'])
    except BaseException as error:
        print("Unknown error while executing: " + str(error))
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
