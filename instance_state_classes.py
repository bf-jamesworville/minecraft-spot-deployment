import boto3
import botocore
import json
import logging
import os

ASG_NAME = os.environ['ASG_NAME']

def lambda_handler(event, context):
    group_name = ASG_NAME
    asg_controller = AutoScalingGroupController(group_name)
    if event['rawPath'] == '/on':
        return asg_controller.turn_on()
    elif event['rawPath'] == '/off':
        return asg_controller.turn_off()
    elif event['rawPath'] == '/status':
        return asg_controller.get_status()
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Invalid URL",
            }),
            "isBase64Encoded": False
        }

class AutoScaler:
    def __init__(self, group_name):
        self.client = boto3.client('autoscaling')
        self.ec2_client = boto3.client('ec2')
        self.group_name = group_name
        
    def set_desired_capacity(self, capacity):
        try:
            response = self.client.set_desired_capacity(
                AutoScalingGroupName=self.group_name,
                DesiredCapacity=capacity,
                HonorCooldown=True
            )
        except botocore.exceptions.ClientError as e:
            logging.error(e)
            raise
        return response
    
    def describe_auto_scaling_group(self):
        try:
            response = self.client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[self.group_name]
            )
        except botocore.exceptions.ClientError as e:
            raise # This should raise an error to the caller
        return response['AutoScalingGroups'][0]['DesiredCapacity']
    
    def get_status(self):
        # Check the current state of the Auto Scaling Group - i.e. desired capacity and any instance ID as well as its launch time
        try:
            response = self.client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[self.group_name]
            )

            # Get the launch time of the instance
            try:
                instance_id = response['AutoScalingGroups'][0]['Instances'][0]['InstanceId']
                instance_response = self.ec2_client.describe_instances(
                    InstanceIds=[instance_id]
                )
                launch_time = instance_response['Reservations'][0]['Instances'][0]['LaunchTime']
            except IndexError:
                launch_time = "No instances currently in the Auto Scaling Group"
                raise

        except botocore.exceptions.ClientError as e:
            raise

        # Return dictionary of the desired capacity and the instance IDs and launch times
        return {
            "desired_capacity": response['AutoScalingGroups'][0]['DesiredCapacity'],
            "instance_id": instance_id,
            "launch_time": str(launch_time)
        }
    
class AutoScalingGroupController:
    def __init__(self, group_name):
        self.autoscaler = AutoScaler(group_name)
        
    def turn_on(self):
        if self.autoscaler.describe_auto_scaling_group() == 1:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Desired Capacity is already 1",
                }),
                "isBase64Encoded": False
            }
        else:
            self.autoscaler.set_desired_capacity(1)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Desired Capacity set to 1",
                }),
                "isBase64Encoded": False
            }
        # The error handling is not implemented here as it is handled by the AutoScaler class
        
    def turn_off(self):
        if self.autoscaler.describe_auto_scaling_group() == 0:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Desired Capacity is already 0",
                }),
                "isBase64Encoded": False
            }
        else:
            self.autoscaler.set_desired_capacity(0)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Desired Capacity set to 0",
                }),
                "isBase64Encoded": False
            }
        
    def get_status(self):
        status = self.autoscaler.get_status()
        return {
            "statusCode": 200,
            "body": json.dumps(status),
            "isBase64Encoded": False
        }