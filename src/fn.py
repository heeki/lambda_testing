import boto3
import json
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.core import patch_all

# initialization
session = boto3.session.Session()
client = session.client('sqs')
# patch_all()

# helper functions
def build_response(code, body):
    # headers for cors
    headers = {
        # "Access-Control-Allow-Origin": "amazonaws.com",
        # "Access-Control-Allow-Credentials": True,
        "Content-Type": "application/json"
    }
    # lambda proxy integration
    response = {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": headers,
        "body": body
    }
    return response

def handler(event, context):
    output = {
        "event": event,
        "aws_request_id": context.aws_request_id,
        "function_name": context.function_name,
        "function_version": context.function_version,
        "invoked_function_arn": context.invoked_function_arn,
        "memory_limit_in_mb": context.memory_limit_in_mb,
        "log_group_name": context.log_group_name,
        "log_stream_name": context.log_stream_name
    }
    output["message"] = "hello world"
    print(json.dumps(output))
    response = build_response(200, output)
    return response
