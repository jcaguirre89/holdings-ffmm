import boto3
s3 = boto3.resource('s3')
s3.Object('mmff-holdings-chile', 'holdings-2008-2019.zip').upload_file('holdings-2008-2019.zip')
