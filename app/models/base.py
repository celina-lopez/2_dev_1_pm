from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute
import os
from dotenv import load_dotenv

REGION = 'us-east-1'
load_dotenv(dotenv_path='../../.env')


class ProjectModel(Model):
    """
    A DynamoDB DevProject
    """
    class Meta():
        table_name = '2_dev_1_pm-project'
        region = REGION
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
    uuid = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    logs = ListAttribute()
    html = UnicodeAttribute()
    image = UnicodeAttribute()
