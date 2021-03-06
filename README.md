## Crypto-Tracker ##
<img src="https://user-images.githubusercontent.com/30131788/156815456-87c8de61-c582-4802-93b6-fb19bc8dffcc.png" width="800" alt="cryptotracker">

## Goals: ##
The website will be designed for uses to understand the historic cryptocurrency changes. It will allow for users to select in real time current cryptocurrency and review their historic performance. It will also allow for a user to save multiple cryptocurrency to their of their portfolio. Users are able to create an account or login onto an existing account.


## Target Users: ##

It is anticipated that the application will be used for anyone who has an interest in cryptocurrency performance.


## Link to Deployment: ##
```
https://crypto-tracker-irene.herokuapp.com/
```

## External API: ##
```
https://www.coingecko.com/en/api
```


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