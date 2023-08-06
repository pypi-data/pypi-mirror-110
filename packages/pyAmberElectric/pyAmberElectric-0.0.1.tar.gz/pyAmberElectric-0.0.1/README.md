# AmberElectric

Make it easier to use Amber's newer API that uses AWS for authentication.

Specify your login creds, and optionally how long to leave between refeshing the data in seconds. The default is equal to 5 minutes.

You can get the entire response from Amber with the json property, or cut out the middleman and get specific values like currentPrice. Data is stored locally so feel free to grab

# How-to

```python
from pyAmberElectric import pyAmberElectric
Amber = pyAmberElectric(username='yourEmail', password='yourPassword', updateInterval=600)

#array of your meter prices
Amber.currentPrice

#the complete raw json data
Amber.json

print("Prices are currently ", Amber.currentValue)
```

# The Deets

## Renewing auth and data
The authentication token will be automatically renewed when needed, normally lasting an hour. You can call auth() to manually renew if required.

If needed, all known data is requested at once. When the local data is older than the maxAge, the data is refreshed. You can also call update() to manually request new data. Amber's data doesn't change more often than every 5 minutes at most so no need to hammer it.

## Avaliable Props

#### json
Returns the full json object returned by Amber. Contains all info avaliable in the app/website.

#### currentPrice
Returns an array of your current prices in cents.

#### currentRenewable
Returns an array of the current percentage of renewables in the grid.

#### currentValue
Returns an array of the current qualative value of the price. Can be 'BAD', 'NEUTRAL' or 'GOOD'.

#### periodCost
Returns the total cost for the last 30 days in cents.

#### periodUsage
Returns the total usage for the last 30 days in Kwh.

#### periodRenewable
Returns the average percentage of renewables in the grid for the last 30 days.

# Secret Methods
You shouldn't need to call these methods but they are there if you really want/need them.

#### auth()
Renew the authentication token.

#### update()
Refresh the data from Amber.
