from fastapi import FastAPI, Request
import logging
from get_config import get_config_from_json
import json
import uvicorn
import hazelcast
import sys

HTTP_HOST, FACADE_PORT, LOGGING_PORT, \
    MESSAGES_PORT, RELOAD, LOG_LEVEL = get_config_from_json("config.json")

HTTP_OK = 200
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

app = FastAPI()

hz = hazelcast.HazelcastClient(cluster_name="dev") # тут має бути айпішки тих нод які hz-start для логів
print("Connected to Hazelcast instance")

messages = hz.get_map("my-map").blocking()

@app.post("/")
async def handle_post(request: Request):

    req = await request.json()

    logging.info(f"Message: {req['msg']}")

    messages.lock(req["UUID"])
    try:
        messages.put(req["UUID"], req["msg"])
    finally:
        messages.unlock(req["UUID"])

    return "", HTTP_OK


@app.get("/")
def handle_get():
    response_body = {
        "data_base_return_msg": " ".join(messages.values())
    }
    return response_body, HTTP_OK

if __name__ == "__main__":
    port = int(sys.argv[1])
    uvicorn.run("log.main:app", 
                host=HTTP_HOST, 
                port=port, 
                reload=RELOAD, 
                log_level=LOG_LEVEL)
    logging.info(f"Logging service run on port {port}!")