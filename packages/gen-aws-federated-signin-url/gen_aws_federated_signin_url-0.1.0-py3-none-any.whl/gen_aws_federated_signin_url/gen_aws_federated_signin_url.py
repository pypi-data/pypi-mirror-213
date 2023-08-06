import boto3
import json
import requests
import urllib.parse


class GenAwsFederatedSigninUrl:
    def __init__(self, client):
        self.client = client

    @classmethod
    def client(cls):
        client = boto3.client("sts")
        return cls(client)

    def __fetch_signin_token(self, credentials):
        url_credentials = {}
        url_credentials["sessionId"] = credentials.get("AccessKeyId")
        url_credentials["sessionKey"] = credentials.get("SecretAccessKey")
        url_credentials["sessionToken"] = credentials.get("SessionToken")

        json_string_with_temp_credentials = json.dumps(url_credentials)
        request_parameters = f"?Action=getSigninToken&Session={urllib.parse.quote(json_string_with_temp_credentials)}"
        request_url = "https://signin.aws.amazon.com/federation" + request_parameters
        r = requests.get(request_url)
        signin_token = r.json()
        return signin_token["SigninToken"]

    def __generate_fetch_signin_url(self, signin_token, action, issuer, destination):
        request_parameters = f"?Action=login"
        request_parameters += "&Issuer=Example.org"
        request_parameters += "&Destination=" + urllib.parse.quote("https://console.aws.amazon.com/")
        request_parameters += "&SigninToken=" + signin_token
        request_url = "https://signin.aws.amazon.com/federation" + request_parameters
        return request_url

    def generate(
        self,
        role_arn: str,
        session_name: str = "AssumeRoleSession",
        duration_seconds: int = 3600,
        action: str = "login",
        issuer: str = "Example.org",
        destination: str = "https://console.aws.amazon.com/",
    ):
        assume_role_response = self.client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name,
            DurationSeconds=duration_seconds,
        )

        signin_token = self.__fetch_signin_token(assume_role_response["Credentials"])
        signin_url = self.__generate_fetch_signin_url(signin_token, action, issuer, destination)

        return signin_url
