import boto3
def application():
    # Create SQS client

    sqs = boto3.client('sqs',region_name='us-east-1')

    #The URL of queue which stores the message sent from front-end
    queue_url = 'https://sqs.us-east-1.amazonaws.com/064295655087/inputMoodsic'

    message=[]

    # Receive message from SQS queue
    response = sqs.receive_message(
       QueueUrl=queue_url,
        AttributeNames=[
        ],
        MaxNumberOfMessages=1,
       MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    #The message should be the name of music
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)

    bucket_name = "nthu-moodsic"
    #Music name
    key=message


    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']

    musicURL = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)
    print(musicURL)

    send_to_sqs = boto3.client('sqs', region_name='us-east-1')

    queue_url = 'https://sqs.us-east-1.amazonaws.com/064295655087/outputMoodsic'


    # Send message to SQS queue
    response = send_to_sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={},
        MessageBody=(
            musicURL
        )
    )

    print(response['MessageId'])

# if __name__ == "__main__":
#     application.debug = True
#     application.run
#fuck

