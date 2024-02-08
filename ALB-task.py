# VPC ID IS NEEDED

import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('elbv2')

    try:
        response = client.describe_load_balancers(Names=['my-load-balancer'])
        load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    except client.exceptions.LoadBalancerNotFoundException:
        try:
            response = client.create_load_balancer(
                Name='my-load-balancer',
                Subnets=[
                    'subnet-0597290e716fb5dbd',
                    'subnet-04a078863285426d1',
                ],
            )
            load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        except:
            print("Could not create load balancer")
            return {
                'statusCode': 500,
                'body': json.dumps('Could not create load balancer')
            }

    try:
        response = client.describe_target_groups(Names=['my-target-group'])
        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
    except client.exceptions.TargetGroupNotFoundException:
        try:
            response = client.create_target_group(
                Name='my-target-group',
                Protocol='HTTP',
                Port=80,
                VpcId='vpc-0c902e56be9a0bf7f', # default vpc
            )
            target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
        except:
            print("Could not create target group")
            return {
                'statusCode': 500,
                'body': json.dumps('Could not create target group')
            }

    try:
        listener_response = client.create_listener(
            DefaultActions=[
                {
                    'TargetGroupArn': target_group_arn,
                    'Type': 'forward',
                },
            ],
            LoadBalancerArn=load_balancer_arn,
            Port=80,
            Protocol='HTTP',
        )
        print(listener_response)
    except:
        print("Could not attach TG to ALB")
        return {
            'statusCode': 500,
            'body': json.dumps('Could not attach TG to ALB')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
