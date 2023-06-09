from fastapi import FastAPI, Request
import uvicorn
import uuid
import json
import requests
import hazelcast
from get_config import get_config_from_json
from random import choice

HTTP_HOST, FACADE_PORT, LOGGING_PORT, \
    MESSAGES_PORT, RELOAD, LOG_LEVEL = get_config_from_json("config.json")

LOGGING_URL = [f"http://{HTTP_HOST}:{x}" for x in LOGGING_PORT]
MESSAGES_URL = [f"http://{HTTP_HOST}:{x}" for x in MESSAGES_PORT]
HTTP_OK = 200

app = FastAPI()

hz = hazelcast.HazelcastClient(cluster_name="dev")
print("Connected to Hazelcast instance")
queue = hz.get_queue("my-queue").blocking()


@app.get('/')
def handle_get():
    try:
        curr_logging_addr = choice(LOGGING_URL)
        logging_response = requests.get(choice(LOGGING_URL)).json()
        messages_response = requests.get(choice(MESSAGES_URL)).json()

        message_responce_template = {
            "data_base_return_msg": " ".join([logging_response[0]["data_base_return_msg"], messages_response[0]["msg"]]),
        }

        return message_responce_template, HTTP_OK
    except Exception:
        print(f"Log on {curr_logging_addr} not working")


@app.post('/')
async def get_body(request: Request):
    try:
        uid = str(uuid.uuid4())
        msg = await request.json()
        message_template = {
            "UUID": uid,
            "msg": msg['msg']
        }
        queue.put(message_template)
        
        logging_response = requests.post(choice(LOGGING_URL), json=message_template)
        return "", logging_response.status_code
    except Exception:
        print(f"currently not working")


if __name__ == "__main__":
    
    uvicorn.run(app="facade-service.main:app",
                host=HTTP_HOST,
                port=FACADE_PORT,
                reload=RELOAD,
                log_level=LOG_LEVEL)