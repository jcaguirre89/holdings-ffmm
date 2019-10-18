import boto3
import pandas as pd
s3 = boto3.resource('s3')

obj = s3.Object('mmff-holdings-chile', key='holdings-2008-2019.zip')
obj.download_file('data/holdings-2008-2019.zip')
