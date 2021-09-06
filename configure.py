import json

from  aws_cdk import (
    core,
    aws_lambda
)

from utils import load_config

config = load_config('project_config.json')

STACK_NAME = config['STACK_NAME']
TAGS = config['RESOURCE_TAGS']
REGION = config['REGION']
APIS = config['APIS']
EVENT_TRACKERS = config['EVENT_TRACKERS']
FILTERS =  config['FILTERS']

BASE_LAMBDA_CONFIG = dict (
    timeout=core.Duration.seconds(20),       
    memory_size=256,
    tracing= aws_lambda.Tracing.ACTIVE)

PYTHON_LAMBDA_CONFIG = dict (runtime=aws_lambda.Runtime.PYTHON_3_8, **BASE_LAMBDA_CONFIG)



BASE_ENV_VARIABLES = dict (REGION= REGION, FILTERS = json.dumps(FILTERS))

BASE_INTEGRATION_CONFIG =  dict(proxy=True,
    integration_responses=[{
        'statusCode': '200',
        'responseParameters': {
            'method.response.header.Access-Control-Allow-Origin': "'*'"
        }
    }])

BASE_METHOD_RESPONSE = dict(
    method_responses=[{
        'statusCode': '200',
        'responseParameters': {
            'method.response.header.Access-Control-Allow-Origin': True,
        }
    }]
)