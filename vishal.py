import json
import boto3


def lambda_handler(event, context):
    AMI = 'ami-04b2519c83e2a7ea5'
    INSTANCE_TYPE = 't3.micro'
    KEY_NAME = 'vishal'
    REGION = 'ap-south-1'
    UserData="""#!/bin/bash
                yum update -y
                yum install -y httpd
                systemctl start httpd
                systemctl enable httpd
                yum install nginx
                systemctl start nginx
            """
    ec2 = boto3.client('ec2', region_name=REGION)
    instance = ec2.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        MaxCount=1,
        MinCount=1
    )
    print(instance)
    
    print ("New instance created:")
    instance_id = instance['Instances'][0].get('InstanceId', '')  
    return {}