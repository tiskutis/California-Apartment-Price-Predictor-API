📦 Flask API 
============

This repository contains basic API created with Flask, containing linear regression model, trained on custom-scraped
California houses dataset, and connection to the database, hosted on Heroku.

Available endpoints: 
- main page ("/")
- predictions ("/predict") 
- selections ("/select")

"/predict" (POST method) accepts json type inputs with features and returns predicted prices, e.g. 
input
```
{
	"features": [{
		"Year Built": 1919,
		"Parking Spaces": 2,
		"Area population": 73401,
		"Median age": 31.0,
		"Total households": 22240,
		"Median year built": 1976,
		"Median household income": 53254,
		"Bedrooms": 3,
		"Baths": 2,
		"Square Meters": 117.24
	},
	{
		"Year Built": 1976,
		"Parking Spaces": 2,
		"Area population": 73401,
		"Median age": 31.0,
		"Total households": 22240,
		"Median year built": 1976,
		"Median household income": 80000,
		"Bedrooms": 4,
		"Baths": 3,
		"Square Meters": 150.24
	}
]
}
```
would return 
```
{"Predicted values": [473616.1131588465, 318816.1463000081]}
```

All requests and their responses are put into the database.

"/select" (GET method) selects from the database and returns last 10 requests with their responses.

Heroku app: https://capstone24.herokuapp.com/