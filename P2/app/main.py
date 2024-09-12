import os
import uvicorn
from fastapi import FastAPI, Request
import requests
import redis

redis_host = "redis-service"
redis_port = 6379

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# redisCli = redis.Redis(
#     host='localhost',
#     port=6379,
#     charset="utf-8",
#     decode_responses=True
#     )
#
# connection = redisCli.ping()
# print(connection)

app = FastAPI()

port = os.getenv("PORT")
cache_duration = int(os.getenv("DURATION"))
api_key = os.getenv("APIKEY")
city_env = os.getenv("CITY")


@app.get("/")
def root(request: Request, city: str = city_env):
    # all_keys = r.keys('*')
    #
    # # Get information about each key, including TTL
    # for key in all_keys:
    #     ttl = r.ttl(key)
    #     print(f"Key: {key}, TTL: {ttl} seconds") 

    hostname = request.client.host

    if r.exists(city):
        print(f"Reading {city} response from cache. hostname: {hostname}")
        return r.get(city)
    api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        r.setex(city, cache_duration, response.text)
        print(response.text)
        return response.text + f"\nhostname: {hostname}"
    else:
        print("Error:", response.status_code, response.text)
        return {"Error": response.status_code}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=port)
