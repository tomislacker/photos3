"""
photos3.lambda
==============

"""
from __future__ import print_function
import boto3
import json
import os
import sys
import tempfile
import traceback
import urllib

from photos3.imgprocess import create_thumbnail
from photos3.imgprocess import ingest_image


##############################
# Amazon Service Definitions #
##############################
s3  = boto3.resource('s3')
sqs = boto3.resource('sqs')


def process_new_image_queue(event, context):
    """
    Invoked by a schedule to see if there are queued items

    This implicitly takes advantage of the LACK OF long polling to reduce
    runtime given that image uploads are typically few-and-far-between.
    """
    print("Reading from {}".format(os.environ.get('TASK_QUEUE')))
    new_image_queue = sqs.get_queue_by_name(QueueName=os.environ.get('TASK_QUEUE'))

    has_messages = True
    while has_messages:
        # Assume there are no messages in the queue, letting the Lambda
        # conclude, unless a message is received
        has_messages = False

        for msg_obj in new_image_queue.receive_messages(WaitTimeSeconds=5):
            # Indicate that a message was received during this iteration
            has_messages = True

            # Decode S3 Event Notification received by SQS
            s3_msg = json.loads(msg_obj.body)

            # Iterate through each record of the S3 Event Notifications
            # There's likely only one record per event, but we should still
            # iterate through the list.
            failed_objects = 0

            for record in s3_msg['Records']:
                # Fetch the S3 bucket and object
                s3_bucket = s3.Bucket(record['s3']['bucket']['name'])
                s3_object = s3_bucket.Object(urllib.parse.unquote_plus(record['s3']['object']['key']))
                s3_object_size = record['s3']['object']['size']

                # TODO Do not process objects over a certain size

                print("Processing s3://{b}/{k} ({s} bytes)".format(
                    b=s3_object.bucket_name,
                    k=s3_object.key,
                    s=s3_object_size,
                ))

                # Ingest the image
                try:
                    ingest_image(s3_object)

                except Exception as e:
                    # Report the failure
                    failed_objects += 1
                    traceback.print_exception(*sys.exc_info())

            if not failed_objects:
                print("Removing queue message")
                msg_obj.delete()


def process_thumbnail(event, context):
    """
    Invoked by the initial image processing Lambda
    """
    for record in event['Records']:
        # Read in the SNS message and determine the source S3 object
        sns_data = json.loads(record['Sns']['Message'])
        s3_object = s3.Object(sns_data['s3_bucket'], sns_data['s3_key'])
        width = int(sns_data['width'])
        height = int(sns_data['height'])

        print("Generating {w}x{h} for s3://{b}/{k}".format(
            w=width,
            h=height,
            b=s3_object.bucket_name,
            k=s3_object.key))

        # Generate the thumbnail
        try:
            create_thumbnail(s3_object, width, height)

        except Exception as e:
            # Report the failure
            failed_objects += 1
            traceback.print_exception(*sys.exc_info())


if __name__ == '__main__':
    process_new_image_queue(None, None)
