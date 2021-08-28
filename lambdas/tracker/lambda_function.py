import json
import os
import boto3

def lambda_handler(event, context):
    
    # ** --------------------------------
    # ** OBTENER LOS USUARIOS DE LA BBDD
    # ** --------------------------------

    region =os.environ.get('REGION')


    nombre_tabla =os.environ.get('TABLE_NAME')

    statement = { "Statement": 'select *  from "{}" '.format(nombre_tabla)}
    print (statement)

    usuarios_tabla = execute_query(dynamo, statement)
    
    return build_response(200, usuarios_tabla[0])



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
