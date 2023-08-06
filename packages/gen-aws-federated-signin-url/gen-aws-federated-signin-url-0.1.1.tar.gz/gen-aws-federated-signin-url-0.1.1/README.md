# gen_aws_federated_signin_url

Generate AWS Federated Signin URL

## Install

```
pip install gen_aws_federated_signin_url
```

## Usage

```python
from gen_aws_federated_signin_url import GenAwsFederatedSigninUrl

url = GenAwsFederatedSigninUrl.client()
signin_url = url.genrate(
    role_arn='arn:aws:iam::123456789012:role/role-name',
)
print(signin_url)
```
