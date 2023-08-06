from typing import List, TypedDict
import boto3

class TokensFed(TypedDict):
    access_key: str
    secret_access_key: str
    session_token: str

class UnauthorizedException(Exception):
    """
    Exception raised when a user cannot perform an action.

    Possible reasons:
    - Name is incorrect.
    """
    pass

class ScribeAuthFederation:
    def __init__(self, name: str):
        self.client = boto3.client('sts')
        # arn:aws:sts::793767825718:assumed-role/AWSReservedSSO_SystemAdministrator_d917346fee95c304/Ailin
        # self.role_arn = 'arn:aws:sts::793767825718:assumed-role/AWSReservedSSO_SystemAdministrator_d917346fee95c304'
        self.role_arn = 'arn:aws:sts::804678412254:assumed-role/AWSReservedSSO_SystemAdministrator_22951c4ef526dd58'
        self.role_session_name = 'Ailin'
        self.name = 'Ailin'

    def get_tokens(self) -> TokensFed:
        try:
            response = self.client.get_federation_token(
                Name=self.name
            )
            return {
                'access_key': response['Credentials']['AccessKeyId'],
                'secret_access_key': response['Credentials']['SecretAccessKey'],
                'session_token': response['Credentials']['SessionToken']
          }
        except Exception:
            raise UnauthorizedException('Unauthorized: Name is incorrect.')