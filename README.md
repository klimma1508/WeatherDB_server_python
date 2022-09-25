Server to store weather data in mongoDB

Purpose is to store data in database and access it later using API

Plans to the future:

- [ ] Change api to graphQL
- [ ] web page to show graph of stored data
- [ ] fetch data from weather API and compare to actual weather
- [ ] add project files for ESP

Example request:

/send
```
{
    "IO": "OUT",
    "ROOM": "North",
    "SENSORS": {
        "temp": "20",
        "hum": "65",
        "press": "123",
        "tempSet": "19",
        "humSet": "50",
        "Quality": "None"
    }
}
```