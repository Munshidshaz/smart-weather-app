# smart-weather-app
API Endpoint call -> Open Weather App
Server in-memory -> Redis
Error Handling -> API Key, Server error, Connectivity error, input validation

The algorithm of the app 

1. Start
2. Input the City_Name
3. Check if City_Name exists as a key in Redis:
    a. If found, retrieve and return the cached data
4. Else:
    a. Call the weather API with City_Name
    b. If the API response code is 200:
        i. Parse the JSON response
        ii. Extract the required weather data
        iii. Optionally store the result in Redis for caching
        iv. Return the extracted data
    c. Else if the response code is 401:
        i. Return an "Authentication error"
    d. Else if the response code is 500:
        i. Return a "Server-side error"
    e. Else:
        i. Return "Unknown error with response code: <code>"
5. Display the returned result (whether data or error message)
6. End

