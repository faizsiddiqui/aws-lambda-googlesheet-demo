import googlesheet, boto3, os, json

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

    instances = [['Tags_Name', 'Account', 'AZ', 'Instance']]
    user_tags = list(filter(None, os.environ['CUSTOM_TAGS'].strip().replace(' ', '').split(',')))
    instances[0].extend(user_tags)

    boto_session = boto3.Session()
    for region in regions:
        ec2 = boto_session.resource('ec2', region_name=region)
        for instance in ec2.instances.all():
            # Modifying tags
            tags = {}
            for tag in instance.tags:
                tags[tag['Key']] = tag['Value']

            # Fixed tags
            instance_tag = [
                tags.get('Name', ''),
                account_id,
                instance.placement['AvailabilityZone'],
                instance.id
            ]

            # User defined tags
            for tag in user_tags:
                instance_tag.append(tags.get(tag, ''))

            instances.append(instance_tag)

    sheet_result = googlesheet.update_sheet(os.environ['SHEET_ID'], os.environ['SHEET_NAME'], os.environ['SHEET_RANGE'], instances)
    return {
        'statusCode': 200,
        'body': json.dumps(sheet_result)
    }
