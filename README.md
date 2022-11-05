# MyRetail Products

## Overview
The goal for this Project is to create an end-to-end Proof-of-Concept for a products API, which will aggregate product data from multiple sources and return it as JSON to the 
caller.

## Requirements
Python 3.5.2+
docker

## Exceptions
As ap part of POC this project uses python LRU caching to cache the Results of API. This can be replaced with in memmory caching tools like Redis or Memcached

As LRU cache does is just python library for in-memmory caching, the entire cache will be cleared on price update . This can be fixed in production using memory object caching tools. 



## Usage


## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

docker-compose up

### Curl Request to Update the price

curl --location --request PUT 'http://localhost:8090/products/13860428' \
--header 'Content-Type: application/json' \
--data-raw '{
  "value": 21,
  "currency_code": "USD"
}'

### Curl Request to get the price 


curl --location --request GET 'http://localhost:8090/products/13860428'





