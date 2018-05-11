import boto3

# Let's use Amazon S3
#s3 = boto3.resource('s3')

# Now that you have an s3 resource, you can make requests 
# and process responses from the service. The following uses 
# the buckets collection to print out all bucket names:

# Print out bucket names
#for bucket in s3.buckets.all():
#    print(bucket.name)

conn = boto.connect_s3()

mybucket = conn.get_bucket('nthu-moodsic')
mybucket.list()
#...listing of keys in the bucket...

nonexistent = conn.get_bucket('i-dont-exist-at-all', validate=False)


#Before this, get the http request from sqsd first
#
bucket_name = "nthu-moodsic"
key = "upload-file"

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.upload_file("upload.txt", key)
location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)




