## 玄石系统Token签发 Python SDK

### Installation

```
pip install lodestone-python-sdk
```

### Usages

```
client = AuthClient(auth_host, your_app_key, your_app_secret)
token = client.get_token()
```

### Tips

```
token有效期7天！
```