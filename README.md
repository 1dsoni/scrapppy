# Scrapppy
Scrappy can scrape pages and save in the database. By default it uses a file to store the json but postgres or any other database can be easily used as the backend.
Similarly it uses a dictionary to cache items, a redis implementation exists with capability to extend to any other choice of cache backend


## how to run scrapppy

dockerized [requires docker to be installed on host]
1. goto root directory
2. docker build -t scrapy .
3. docker run -p8000:8000 scrapy

non dockerized [requires python 3.12]
1. goto root directory
2. python3.12 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. chmod +x web_server.sh
6. sh web_server.sh


## api documentation can be found @ localhost:8000/_docs


## for testing purposes use 
```
jwt = `this is for test`
project = `dental_stall`
```

## usages 
1. call `/execute` to start scraping items
2. call `/data` to fetch scraped items
