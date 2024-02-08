import boto3
import json
import os

def lambda_handler(event, context):
    print("Function started execution")
    instance_type = 't2.micro'
    ami_id = 'ami-0d63de463e6604d0a'
    key_name = 'test'
    instance_name = "sns-test"
    region = "ap-south-1"

    sns_topic_name = 'ec2-launched'
    subscription_endpoint = 'abhishek.y@tallysolutions.com'
    
    print("Creating clients")
    ec2_client = boto3.client('ec2', region_name=region)
    sns_client = boto3.client('sns', region_name=region)
    
    existing_instances = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': [instance_name]},
            {'Name': 'instance-state-name', 'Values': ['running', 'pending']}
        ]
    )

    if existing_instances['Reservations']:
        instance_id = existing_instances['Reservations'][0]['Instances'][0]['InstanceId']
        message = f'EC2 instance with name {instance_name} already exists. Instance ID: {instance_id}'
        print("instance already exists")
        return  {
            'statusCode': 200,
            'body': json.dumps(message)
        }

    sns_topic_arn = get_or_create_sns_topic(sns_client, sns_topic_name)
    subscribe_to_sns_topic(sns_client, sns_topic_arn, subscription_endpoint)

    instance = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1
    )

    instance_id = instance['Instances'][0]['InstanceId']
    print("Created new instance:"+instance_id)

    sns_message = {
        'InstanceID': instance_id,
        'Status': 'Instance created successfully with the id: '+instance_id
    }

    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps({'default': json.dumps(sns_message)}),
        MessageStructure='json'
    )
    print("Published sns")

    return {
        'statusCode': 200,
        'body': json.dumps('EC2 instance created successfully!')
    }

def get_or_create_sns_topic(sns_client, sns_topic_name):
    topics = sns_client.list_topics()['Topics']
    
    for topic in topics:
        if topic['TopicArn'].endswith(':' + sns_topic_name):
            print("Using existing topic named: "+sns_topic_name)
            return topic['TopicArn']
    
    new_topic = sns_client.create_topic(Name=sns_topic_name)
    print("Created new sns topic named: "+sns_topic_name)
    return new_topic['TopicArn']

def subscribe_to_sns_topic(sns_client, sns_topic_arn, endpoint):
    sns_client.subscribe(
        TopicArn=sns_topic_arn,
        Protocol='email',
        Endpoint=endpoint
    )
    print("Subscribed "+endpoint+" to sns:"+sns_topic_arn)
 