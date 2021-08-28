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

                #"personalize:GetRecommendations",
                #"personalize:GetPersonalizedRanking"

        base_api = aws_apigateway.RestApi( self, 'personalize')


        if "recommend" in APIS:
            if (APIS['recommend'] !={}) and (APIS['recommend'] is not None):

            # ** --------------------------------
            # ** RECOMENDADOR DE PRODUCTOS
            # ** --------------------------------

                REC_CAMPAIN_ARN = APIS['recommend']['CAMPAIN_ARN']
                parts = REC_CAMPAIN_ARN.split(':')
                parts.pop()
                FILTERS_ARN = ':'.join(parts) + ':filter/*'


                recommend_lambda = aws_lambda.Function(
                    self, "recommend",handler="lambda_function.lambda_handler",
                    code=aws_lambda.Code.asset("./lambdas/recommend"),**PYTHON_LAMBDA_CONFIG, 
                    environment=json.loads(json.dumps(dict(
                        CAMPAIN_ARN =REC_CAMPAIN_ARN,
                        **BASE_ENV_VARIABLES)))
                )

                recommend_lambda.add_to_role_policy(
                    aws_iam.PolicyStatement(
                        actions=["personalize:GetRecommendations"], 
                        resources=[REC_CAMPAIN_ARN, FILTERS_ARN]))
                
                
                recommend_api = base_api.root.add_resource(APIS['recommend']['API_NAME'])

                resource_recommend = recommend_api.add_resource('{clientId}')
                resource_recommend.add_method(
                    'GET', aws_apigateway.LambdaIntegration(recommend_lambda,**BASE_INTEGRATION_CONFIG), 
                    **BASE_METHOD_RESPONSE
                )                
                resource_recommend.add_method(
                    'POST', aws_apigateway.LambdaIntegration(recommend_lambda,**BASE_INTEGRATION_CONFIG), 
                    **BASE_METHOD_RESPONSE
                )
                
                self.add_cors_options(resource_recommend)

                core.CfnOutput(self, 'recommendations',value=resource_recommend.url)


        if "sims" in APIS:
            if (APIS['sims'] !={}) and (APIS['sims'] is not None):

            # ** --------------------------------
            # ** SIMILAR ITEMS
            # ** --------------------------------

                SIMS_CAMPAIN_ARN = APIS['sims']['CAMPAIN_ARN']
                parts = SIMS_CAMPAIN_ARN.split(':')
                parts.pop()
                FILTERS_ARN = ':'.join(parts) + ':filter/*'

                sims_lambda = aws_lambda.Function(
                    self, "sims_lambda",handler="lambda_function.lambda_handler",
                    code=aws_lambda.Code.asset("./lambdas/sims"),**PYTHON_LAMBDA_CONFIG, 
                    environment=json.loads(json.dumps(dict(
                        CAMPAIN_ARN =SIMS_CAMPAIN_ARN,
                        **BASE_ENV_VARIABLES)))
                )

                sims_lambda.add_to_role_policy(
                    aws_iam.PolicyStatement(
                        actions=["personalize:GetRecommendations"], 
                        resources=[SIMS_CAMPAIN_ARN, FILTERS_ARN]))
                
                
                sims_api = base_api.root.add_resource(APIS['sims']['API_NAME'])

                resource_sims = sims_api.add_resource('{itemId}')
                resource_sims.add_method(
                    'GET', aws_apigateway.LambdaIntegration(sims_lambda,**BASE_INTEGRATION_CONFIG), 
                    **BASE_METHOD_RESPONSE
                )
                resource_sims.add_method(
                    'POST', aws_apigateway.LambdaIntegration(sims_lambda,**BASE_INTEGRATION_CONFIG), 
                    **BASE_METHOD_RESPONSE
                )
                
                self.add_cors_options(resource_sims)

                core.CfnOutput(self, 'sims',value=resource_sims.url)


        if "rerank" in APIS:
            if (APIS['rerank'] !={}) and (APIS['rerank'] is not None):

            # ** --------------------------------
            # ** RERANKING
            # ** --------------------------------

                RERANK_CAMPAIN_ARN = APIS['rerank']['CAMPAIN_ARN']
                parts = RERANK_CAMPAIN_ARN.split(':')
                parts.pop()
                FILTERS_ARN = ':'.join(parts) + ':filter/*'


                rerank_lambda = aws_lambda.Function(
                    self, "rerank_lambda",handler="lambda_function.lambda_handler",
                    code=aws_lambda.Code.asset("./lambdas/rerank"),**PYTHON_LAMBDA_CONFIG, 
                    environment=json.loads(json.dumps(dict(
                        CAMPAIN_ARN =RERANK_CAMPAIN_ARN,
                        **BASE_ENV_VARIABLES)))
                )

                rerank_lambda.add_to_role_policy(
                    aws_iam.PolicyStatement(
                        actions=["personalize:GetPersonalizedRanking"], 
                        resources=[RERANK_CAMPAIN_ARN, FILTERS_ARN]))
                
                
                rerank_api = base_api.root.add_resource(APIS['rerank']['API_NAME'])
                resource_rerank = rerank_api.add_resource('{userId}')

                resource_rerank.add_method(
                    'POST', aws_apigateway.LambdaIntegration(rerank_lambda,**BASE_INTEGRATION_CONFIG), 
                    **BASE_METHOD_RESPONSE
                )
                
                self.add_cors_options(resource_rerank)

                core.CfnOutput(self, 'rerank',value=resource_rerank.url)

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