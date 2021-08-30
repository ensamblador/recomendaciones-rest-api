#%%
import boto3
import time
import uuid
import json
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
personalize_events = boto3.client(service_name='personalize-events', region_name=REGION)

# %%
EVENT_TRACKERS
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

#%%

event = {
"itemId": '16300',
}
event_json = json.dumps(event)


put_event_response = personalize_events.put_events(
trackingId = EVENT_TRACKERS['eventtracker']['TRACKING_ID'],
userId= '10000',
sessionId = str(uuid.uuid1()),
eventList = [{
    'sentAt': int(time.time()),
    'eventType': 'RATING',
    'eventValue': 9,
    'properties': event_json
    }]
)

put_event_response
#%%
str(uuid.uuid1())
# %%
str(uuid.uuid4())
# %%
import json
json.loads('{"itemId": "16300",\n    "eventType: "RATING",\n    "eventValue": "1",\n    "sessionId": "10000"\n}')
# %%
