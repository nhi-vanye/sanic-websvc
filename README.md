Simple tax calculator service
=============================

This is a simple sanic-based (https://sanicframework.org/en/)
web-service for calculating the tax to be paid on a given salary.

Its a web-service not an application so inputs and via REST and
results are returned in JSON.

Sanic requires a modern async-based python so Python 3.7 or later.
This was tested on 3.9.2 (macOS)



Example Usage
-------------

```
 .websvc  deneb ~/S/t/websvc ] python -m websvc.main --access-log
[2021-06-04 19:52:36 +0100] [97487] [INFO] Goin' Fast @ http://127.0.0.1:8888
[2021-06-04 19:52:36 +0100] [97487] [INFO] Starting worker [97487]
```

Then in another window

```
 .websvc  deneb ~/S/O/bbrain ] curl -s 'http://127.0.0.1:8888/calc?salary=152000&details=1' | jq .
{
  "salary": 152000,
  "tax_owed": 48399.55,
  "details": [
    "Tax paid on salary above £150001 = £899.55",
    "Tax paid on salary between £50001 and £150000 = £40000.00",
    "Tax paid on salary between £12501 and £50000 = £7500.00",
    "Tax paid on salary between £0 and £12500 = £0.00"
  ]
}
```

In this I piped the response through `jq` to nicely format the
results (and handle the unicode characters for the currancy symbols)


There is an OpenAPI (swagger) endpoint at 'http://127.0.0.1:8888/swagger/`


Installing
----------

Create a virtual environment

``
% `python -m venv .websvc
```

Activate the virtual environment

```
% .websvc/bin/activate
```

Then install all the requirements

```
% pip install -r requirements.txt
```
