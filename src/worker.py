import boto3

# Create SQS client
sqs = boto3.client('sqs')

#The URL of queue which stores the message sent from front-end
queue_url = 'https://sqs.us-east-1.amazonaws.com/064295655087/inputMoodsic'

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

#Connecting to S3 
conn = boto.connect_s3()

#access to the bucket
mybucket = conn.get_bucket('nthu-moodsic')
mybucket.list()
#...listing of keys in the bucket...

#Catch error
nonexistent = conn.get_bucket('i-dont-exist-at-all', validate=False)


bucket_name = "nthu-moodsic"
#Music name
key = "upload-file"

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.upload_file("upload.txt", key)
location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)

musicURL = ""

sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/064295655087/outputMoodsic'


# Send message to SQS queue
response = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=10,
    MessageAttributes={},
    MessageBody=(
        musicURL
    )
)

print(response['MessageId'])

