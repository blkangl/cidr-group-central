import json
import boto3
from .settings import GROUP_BUCKET_NAME

def list_groups(event, context) -> dict:
    '''List all CIDR groups
    
    Args:
        event (dict): API Gateway event
        context (object): Lambda context 

    Returns:
        dict: API Gateway response
    '''
    
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "List of CIDR groups",
            "data": [
                {"name": "group1", "cidr": "", "description": "Group 1"},
                {"name": "group2", "cidr": "", "description": "Group 2"}
            ]
        })
    }

def create_new_group(event, context) -> dict:
    '''Create a new CIDR group
    
    Args:
        event (dict): API Gateway event
        context (object): Lambda context 

    Returns:
        dict: API Gateway response
    '''
    body = event.get("body", None)
    
    if body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing request body"
            })
        }

    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid request body"
            })
        }
    
    name = body.get("name", None)
    description = body.get("description", None)
    
    if name is None or description is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing required fields"
            })
        }
    
    # Create new CIDR group in S3 bucket
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.put_object(
        Bucket=GROUP_BUCKET_NAME,
        Key=f"{name}.json",
        Body=json.dumps({
            "name": name,
            "description": description,
        })
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "New CIDR group created"
        })
    }
