<h1 align="center"><strong>Scramjet Manager client</strong></h1>

<p align="center">
    <a href="https://github.com/scramjetorg/transform-hub/blob/HEAD/LICENSE"><img src="https://img.shields.io/github/license/scramjetorg/transform-hub?color=green&style=plastic" alt="GitHub license" /></a>
    <a href="https://scr.je/join-community-mg1"><img alt="Discord" src="https://img.shields.io/discord/925384545342201896?label=discord&style=plastic"></a>
</p>

## About:

This package provides a **Manager client** which manages [Transform Hub](https://github.com/scramjetorg/transform-hub) clients.

## Usage:

> ❗NOTE: You need to provide your middleware [access token](https://docs.scramjet.org/platform/quick-start#step-1-set-up-the-environment) if you are not hosting STH locally.

```python
import asyncio
from manager_client.manager_client import ManagerClient
from client_utils.base_client import BaseClient

# your middleware token
token = ''

# set the token
BaseClient.setDefaultHeaders({'Authorization': f'Bearer {token}'})

# middleware url
api_base ='https://api.scramjet.cloud/api/v1' 

# url = {middlewareURL}/space/{manager_id}/api/v1
manager = ManagerClient(f'{api_base}/space/org-aa5bu150-9o5c-489b-83e3-b1yf7e086f3h-manager/api/v1')

res = asyncio.run(manager.get_hosts())
print(res)
```
