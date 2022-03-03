## To create virtual environment: ##
```
python3 -m venv venv
source venv/bin/activate
```

## To run the app in the virtual environment: ##
```
pip install -r requirements.txt
flask run
```

## To populate the database for the first time: ##
```
flask db migrate
flask db upgrade
```