# A lambda function to turn on or off an instance - run from a function URL

import boto3
import json



def lambda_handler(event, context):
    # Check if rawpath is set to /on or /off
    if event['rawPath'] == '/on':
        # turn instance on
        if check_state():
            # instance is already on
            return {
                    "statusCode": 304,
                        "body": json.dumps({
                            "message": "Instance is already on",
                        }),
                        "isBase64Encoded": False
            }
        else:
            turn_on()
            return {
                    "statusCode": 200,
                        "body": json.dumps({
                            "message": "Instance turned on",
                        }),
                        "isBase64Encoded": False
            }
    elif event['rawPath'] == '/off':
        # turn instance off
        if check_state():
            turn_off()
            return {
                    "statusCode": 200,
                        "body": json.dumps({
                            "message": "Instance turned off",
                        }),
                        "isBase64Encoded": False
            }
        else:
            # instance is already off
            return {
                    "statusCode": 304,
                        "body": json.dumps({
                            "message": "Instance is already off",
                        }),
                        "isBase64Encoded": False
            }
    else:
        # invalid path
        return {
                "statusCode": 404,
                    "body": json.dumps({
                        "message": "Invalid URL",
                    }),
                    "isBase64Encoded": False
        }
    
def turn_on():
    # turn on instance
    instance.start()
    return

def turn_off():
    # turn off instance
    instance.stop()
    return

def check_state():
    # check if instance is running
    if instance.state['Name'] == 'running':
        return True
    else:
        return False