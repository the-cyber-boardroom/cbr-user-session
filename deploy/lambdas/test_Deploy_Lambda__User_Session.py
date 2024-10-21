from unittest                                   import TestCase
from cbr_user_session.utils.Version             import version__cbr_user_session
from deploy.lambdas.Deploy_Lambda__User_Session import Deploy_Lambda__User_Session


class test_Deploy_Lambda__OSBot_LLMs(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deploy_lambda = Deploy_Lambda__User_Session()

    def test_deploy_lambda(self):
        with self.deploy_lambda as _:
            result = _.lambda_deploy()
            assert result == {'body': 'Hello from Docker Lambda!', 'statusCode': 200}

    def test_ecr_image_uri(self):
        with self.deploy_lambda as _:
            ecr_image_uri = _.ecr_image_uri()                               # todo: change values below to aws_config.account_id() and aws_config.region_name()
            assert ecr_image_uri == f'654654216424.dkr.ecr.eu-west-1.amazonaws.com/osbot_flows:{version__cbr_user_session}'
