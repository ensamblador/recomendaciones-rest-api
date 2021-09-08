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
import boto3
client = boto3.client('sts')
# %%
client.get_caller_identity()
# %%
personalize_client = boto3.client('personalize', region_name='us-west-2')
# %%
personalize_client.list_campaigns()['campaigns']
# %%
#personalize_client.list_event_trackers(datasetGroupArn='arn:aws:personalize:us-west-2:625806755153:dataset-group/personalize-anime')['eventTrackers']
personalize_client.describe_event_tracker(
    eventTrackerArn='arn:aws:personalize:us-west-2:625806755153:event-tracker/d2e0162e'
)['eventTracker']
# %%
personalize_client.list_dataset_groups()
# %%
def get_personalize_event_trackers(client):
    dsgs = client.list_dataset_groups()['datasetGroups']
    dsg_arns = []
    for dsg in dsgs:
        if dsg['status'] == 'ACTIVE':
            dsg_arns.append(dsg['datasetGroupArn'])
    
    event_trackers = []
    for dsg_arn in dsg_arns:
        e_trackers = client.list_event_trackers(datasetGroupArn=dsg_arn)['eventTrackers']
        for et in e_trackers:
            if et['status'] == 'ACTIVE':
                details = client.describe_event_tracker(eventTrackerArn=et['eventTrackerArn'])['eventTracker']
                event_trackers.append({
                    'name': et['name'], 
                    'arn':et['eventTrackerArn'],
                    'trackingId': details['trackingId']
                    })

    return event_trackers

get_personalize_event_trackers(personalize_client)
# %%
def get_personalize_filters(client):
    dsgs = client.list_dataset_groups()['datasetGroups']
    dsg_arns = []
    for dsg in dsgs:
        if dsg['status'] == 'ACTIVE':
            dsg_arns.append(dsg['datasetGroupArn'])
    
    filters = []
    for dsg_arn in dsg_arns:
        ffilters = client.list_filters(datasetGroupArn=dsg_arn)['Filters']
        for ffilter in ffilters:
            if ffilter['status'] == 'ACTIVE':
                filters.append({'name': ffilter['name'], 'arn':ffilter['filterArn']})

    return filters

get_personalize_filters(personalize_client)

#%%
personalize_client.list_recipes()['recipes']

# %%
personalize_client.describe_campaign(campaignArn='arn:aws:personalize:us-west-2:625806755153:campaign/personalize-anime-SIMS')['campaign']
# %%
personalize_client.describe_solution_version(solutionVersionArn='arn:aws:personalize:us-west-2:625806755153:solution/personalize-anime-sims/4a25f136')['solutionVersion']
# %%
def get_personalize_campains(client):
    campaigns = client.list_campaigns()['campaigns']
    camps = []
    for c in campaigns:
        if c['status'] == 'ACTIVE':
            details = client.describe_campaign(campaignArn=c['campaignArn'])['campaign']
            solution_version_arn = details['solutionVersionArn']
            solution_details = client.describe_solution_version(solutionVersionArn=solution_version_arn)['solutionVersion']
            recipe_arn = solution_details['recipeArn']
            camps.append({
                'name': c['name'],
                'arn': c['campaignArn'],
                'recipe': recipe_arn.split('/')[-1]
            })
    return camps
# %%
campanas = get_personalize_campains(personalize_client)
# %%
campanas
# %%
APIS = []
for c in campanas:
    if 'sims' in c['recipe']:
        c['type'] = 'sims'
    elif 'ranking' in c['recipe']:
        c['type'] = 'rerank'
    elif ('user-personalization' in c['recipe']) or ('hrnn' in c['recipe']) or ('popularity-count' in c['recipe']):
        c['type'] = 'recommend'

    APIS.append({
        'CAMPAIGN_ARN': c['arn'],
        'API_NAME': c['name'].lower(),
        'CAMPAIGN_TYPE': c['type']
    })
APIS
# %%
import boto3
account_id = boto3.client('sts').get_caller_identity()['Account']
account_id_anonymized = '******'+str(account_id)[6:]
# %%
#account_id_anonymized[:6] = '******'


# %%
account_id, account_id_anonymized
# %%
