# Requirement
- python version >= 3.8
- database: Postgresql, Mysql

# Set up environment to run unittest

1. Set up python virtual environment
```
python3 -m venv venv

. venv/bin/activate
```
Install pipenv
```
pip install pipenv
```
Install library dependency
```
pipenv install
```

2. Set up database
Create database for test(for example with Postgresql)
```
createdb call_billing_test 
```

Update config testing env in config/settings.toml
```
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/call_billing_test'
```
Run test

```
tox tests
```

# Run this app
Build docker image
```
docker build . -t call_billing_app
```

Run with docker-compose
```
docker-compose up -d
```