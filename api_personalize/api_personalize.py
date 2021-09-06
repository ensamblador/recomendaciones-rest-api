import json 

from aws_cdk import (
    aws_lambda,
    aws_iam ,
    aws_ssm as ssm,
    aws_apigateway,
    core,
)

from configure import ( 
    APIS, 
    EVENT_TRACKERS, 
    PYTHON_LAMBDA_CONFIG, 
    BASE_ENV_VARIABLES, 
    BASE_INTEGRATION_CONFIG,
    BASE_METHOD_RESPONSE)




class ApiPersonalize(core.Construct):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        base_api = aws_apigateway.RestApi( self, 'personalize')

        if "recommend" in APIS:
            if (APIS['recommend'] !={}) and (APIS['recommend'] is not None):

            # ** --------------------------------
            # ** RECOMENDADOR DE PRODUCTOS
            # ** --------------------------------
                self.make_resource(
                    base_api = base_api, 
                    api_data = APIS['recommend'], 
                    resource_name = '{userId}', 
                    methods = ['GET'], 
                    backend_code = aws_lambda.Code.asset("./lambdas/recommend")
                ) 

        if "sims" in APIS:
            if (APIS['sims'] !={}) and (APIS['sims'] is not None):

            # ** --------------------------------
            # ** SIMILAR ITEMS
            # ** --------------------------------

                self.make_resource(
                    base_api = base_api, 
                    api_data = APIS['sims'], 
                    resource_name = '{itemId}', 
                    methods = ['GET'], 
                    backend_code = aws_lambda.Code.asset("./lambdas/sims")
                ) 

        if "rerank" in APIS:
            if (APIS['rerank'] !={}) and (APIS['rerank'] is not None):

            # ** --------------------------------
            # ** RERANKING
            # ** --------------------------------

                self.make_resource(
                    base_api = base_api, 
                    api_data = APIS['rerank'], 
                    resource_name = '{userId}', 
                    methods = ['GET'], 
                    backend_code = aws_lambda.Code.asset("./lambdas/rerank")
                )    

        if len(EVENT_TRACKERS):

            # ** --------------------------------
            # ** EVENT TRACKERS
            # ** --------------------------------

            for et in EVENT_TRACKERS.keys():
                et_data = EVENT_TRACKERS[et]
                self.make_event_tracker(
                    base_api = base_api, 
                    api_data = et_data, 
                    resource_name = '{userId}',  
                    backend_code = aws_lambda.Code.asset("./lambdas/tracker")
                ) 

    def make_event_tracker(self, base_api, api_data, resource_name, backend_code):

        lambda_backend = aws_lambda.Function(
            self,api_data['API_NAME'] + "_lambda" ,handler="lambda_function.lambda_handler",
            code=backend_code,**PYTHON_LAMBDA_CONFIG, 
            environment=json.loads(json.dumps(dict(
                TRACKING_ID =api_data['TRACKING_ID'],
                DEFAULT_EVENT_TYPE = api_data['DEFAULT_EVENT_TYPE'],
                DEFAULT_EVENT_VALUE = api_data['DEFAULT_EVENT_VALUE'],
                **BASE_ENV_VARIABLES)))
        )

        lambda_backend.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["personalize:PutEvents"], 
                resources=['*']))

        new_api = base_api.root.add_resource(api_data['API_NAME'])
        new_resource = new_api.add_resource(resource_name)

        new_resource.add_method(
            'POST' , aws_apigateway.LambdaIntegration(lambda_backend,**BASE_INTEGRATION_CONFIG), 
            **BASE_METHOD_RESPONSE
        )
        
        self.add_cors_options(new_resource)

        core.CfnOutput(self, api_data['API_NAME'] + "_out",value=new_resource.url)


    def make_resource(self, base_api, api_data,resource_name, methods, backend_code):
        CAMPAIN_ARN = api_data['CAMPAIN_ARN']
        parts = CAMPAIN_ARN.split(':')
        parts.pop()
        FILTERS_ARN = ':'.join(parts) + ':filter/*'

        lambda_backend = aws_lambda.Function(
            self,api_data['API_NAME'] + "_lambda" ,handler="lambda_function.lambda_handler",
            code=backend_code,**PYTHON_LAMBDA_CONFIG, 
            environment=json.loads(json.dumps(dict(
                CAMPAIN_ARN =CAMPAIN_ARN,
                **BASE_ENV_VARIABLES)))
        )

        lambda_backend.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["personalize:GetPersonalizedRanking", "personalize:GetRecommendations"], 
                resources=[CAMPAIN_ARN, FILTERS_ARN]))

        new_api = base_api.root.add_resource(api_data['API_NAME'])
        new_resource = new_api.add_resource(resource_name)

        for m in methods:
            new_resource.add_method(
                m , aws_apigateway.LambdaIntegration(lambda_backend,**BASE_INTEGRATION_CONFIG), 
                **BASE_METHOD_RESPONSE
            )
        
        self.add_cors_options(new_resource)

        core.CfnOutput(self, api_data['API_NAME'] + "_out",value=new_resource.url)

    def add_cors_options(self, apigw_resource):
        apigw_resource.add_method(
            'OPTIONS',
            aws_apigateway.MockIntegration(integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers':
                    "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                    'method.response.header.Access-Control-Allow-Methods':
                    "'GET,POST,OPTIONS,DELETE'"
                }
            }],
                passthrough_behavior=aws_apigateway.
                PassthroughBehavior.WHEN_NO_MATCH,
                request_templates={
                "application/json":
                "{\"statusCode\":200}"
            }),
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers':
                    True,
                    'method.response.header.Access-Control-Allow-Methods':
                    True,
                    'method.response.header.Access-Control-Allow-Origin': True,
                }
            }],
        )