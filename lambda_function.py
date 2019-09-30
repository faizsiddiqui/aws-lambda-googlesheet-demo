import googlesheet, boto3, os

def aws_regions():
    ec2 = boto3.Session().client('ec2')
    response = ec2.describe_regions()
    return list(map(lambda region: region['RegionName'], response['Regions']))

def get_account_id():
    sts = boto3.client('sts')
    return sts.get_caller_identity()["Account"]

def lambda_handler(event, context):
    account_id = get_account_id()
    regions = aws_regions()
    instances = [['Tags_Name', 'Account', 'AZ', 'Instance', 'deployment', 'application', 'version', 'stack_version']]

    boto_session = boto3.Session()
    for region in regions:
        ec2 = boto_session.resource('ec2', region_name=region)
        for instance in ec2.instances.all():
            # Modifying tags
            tags = {}
            for tag in instance.tags:
                tags[tag['Key']] = tag['Value']

            instances.append([
                tags.get('Name', ''),
                account_id,
                instance.placement['AvailabilityZone'],
                instance.id,
                tags.get('deployment', ''),
                tags.get('application', ''),
                tags.get('version', ''),
                tags.get('stack_version', '')
            ])
    sheet_result = googlesheet.update_sheet(os.environ['SHEET_ID'], os.environ['SHEET_NAME'], os.environ['SHEET_RANGE'], instances)
    return {
        'statusCode': 200,
        'body': json.dumps(sheet_result)
    }
