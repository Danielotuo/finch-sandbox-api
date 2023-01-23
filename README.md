# How to run this web app

This web app calls Finch’s Sandbox API to get an access token depending on which provider they choose (gusto, bamboohr, justworks, paychex_flex, or workday). It uses the access token to get the employer’s full employee directory employee personal and employment data.

macOS/Linux
```bash
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

Windows
```bash
> mkdir myproject
> cd myproject
> py -3 -m venv venv
```
Activate the corresponding environment
```bash
$ . venv/bin/activate
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install flask.

```bash
pip install flask
pip install requests
pip install secrets
```

## Run

Generate a secret key

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

```bash
export SECRET_KEY='your_secret_key'
export FLASK_APP=app.py
export FLASK_DEBUG = 1
flask run
```

