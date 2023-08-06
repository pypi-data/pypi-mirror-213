import boto3
import json
from uuid import uuid4

sqs_client = boto3.client("sqs", region_name="eu-central-1")
s3_client = boto3.client("s3", region_name="eu-central-1")
bucket_name = "lambda-testing-fatima-de-serverlessdeploymentbuck-g76sanrcmrse"
bucket_path = "notifications-email"


def push_to_sqs(data: dict, sqs_url: str):
    send_to_s3 = False
    sqs_params = {
        "MessageBody": json.dumps(data),
        "QueueUrl": sqs_url,
        "DelaySeconds": 3
    }

    rough_obj_size = len(json.dumps(data))
    if rough_obj_size > 200000:
        send_to_s3 = True
        object_key = str(uuid4())
        sqs_params["MessageBody"] = f"s3://{bucket_name}/{bucket_path}/{object_key}"

    sqs_response = sqs_client.send_message(**sqs_params)

    if send_to_s3:
        s3_params = {
            "Bucket": bucket_name,
            "Key": f"{bucket_path}/{object_key}",
            "Body": json.dumps(data)
        }
        s3_client.put_object(**s3_params)

    if sqs_response.get("MessageId"):
        print("Notification Sent")
