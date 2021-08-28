#%%
import boto3
from configure import ( 
    APIS, 
    REGION,
    EVENT_TRACKERS, 
    PYTHON_LAMBDA_CONFIG, 
    BASE_ENV_VARIABLES, 
    BASE_INTEGRATION_CONFIG,
    BASE_METHOD_RESPONSE)

# %%
personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime', region_name=REGION)

# Establish a connection to Personalize's event streaming
personalize_events = boto3.client(service_name='personalize-events')

# %%
EVENT_TRACKER, APIS
# %%

get_recommendations_response = personalize_runtime.get_recommendations(
    campaignArn = APIS['sims']['CAMPAIN_ARN'],
    itemId = '300',
    filterArn = 'arn:aws:personalize:us-west-2:625806755153:filter/Drama'

)
get_recommendations_response
# %%
get_recommendations_response = personalize_runtime.get_recommendations(
    campaignArn = APIS['recommend']['CAMPAIN_ARN'],
    userId = '300',
    filterArn = 'arn:aws:personalize:us-west-2:625806755153:filter/Shounen'
)
get_recommendations_response
# %%
get_recommendations_response = personalize_runtime.get_personalized_ranking(
    campaignArn = APIS['rerank']['CAMPAIN_ARN'],
    userId = '300',    
    filterArn = 'arn:aws:personalize:us-west-2:625806755153:filter/Comedy',

    inputList= ['3000', '3001', '2500']
)
get_recommendations_response
# %%
BASE_ENV_VARIABLES
# %%
R = APIS['recommend']['CAMPAIN_ARN'].split(':')
R.pop()
# %%
':'.join(R) + ':filter/*'
# %%
