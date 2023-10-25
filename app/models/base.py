from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute
import os
from dotenv import load_dotenv

REGION = 'us-east-1'
load_dotenv(dotenv_path='../../.env')


class Credentials:
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
    aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

# Example model for a basic user class


class ProjectModel(Model):
    """
    A DynamoDB DevProject
    """
    class Meta(Credentials):
        table_name = '2_dev_1_pm-project'
        region = REGION
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
    uuid = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    logs = ListAttribute()
    code = UnicodeAttribute()


# # Create a new user
# user = UserModel("John", "Denver")
# user.email = "djohn@company.org"
# user.save()

# # Query for the user
# for user in UserModel.query("John", UserModel.first_name.startswith("J")):
#    print(user.first_name)
