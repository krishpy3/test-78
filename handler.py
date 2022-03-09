"""
This funtion will collect the stream arn and
save the arn in ssm paramter store

Need to pass DynamoDB table name as input
"""

import boto3


def lambda_handler(events, context):
    stages = ['uat']
    # stages = ['uat', 'dev', 'qa', 'prod']
    table_name = "workflow-{}-answers"
    dynamodb = boto3.client('dynamodb')
    for stage in stages:
        res = dynamodb.describe_table(TableName=table_name.format(stage))
        arn = res['Table'].get('LatestStreamArn')

        ssm = boto3.client('ssm')
        res = ssm.put_parameter(
            Name=f'/dynamodb/us-east-1/stream/Dynamodb-stream-arn-entry-{stage}',
            Value=arn,
            Type='String')
    return {'message': "Arn updated in parameter store"}
