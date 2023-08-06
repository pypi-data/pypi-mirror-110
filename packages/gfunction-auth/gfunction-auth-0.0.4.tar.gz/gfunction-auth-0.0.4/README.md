# GFunction Auth

Make authorized, lightweight calls to Cloud Functions in Python.

## Install

`pip install gfunction-auth`

## Usage

To make a simple post request to a Cloud Function with url `fn_url`

```
from gfunction_auth import gfunction_post
data = {'example': 42}
response = gfunction_post(fn_url, data)
```

Note, the caller of the function must be registered by GCP. 