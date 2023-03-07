from fastapi import FastAPI, Request
import logging
from get_config import get_config_from_json
import json
import uvicorn

HTTP_HOST, FACADE_PORT, LOGGING_PORT, \
    MESSAGES_PORT, RELOAD, LOG_LEVEL = get_config_from_json("config.json")

HTTP_OK = 200
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

app = FastAPI()

data_base = {}


@app.post("/")
async def handle_post(request: Request):

    req = await request.json()

    data_base[req["UUID"]] = req["msg"]
    logging.info(f"Message: {req['msg']}")

    return "", HTTP_OK


@app.get("/")
def handle_get():
    response_body = {
        "data_base_return_msg": " ".join(data_base.values())
    }
    return response_body, HTTP_OK


if __name__ == "__main__":
    uvicorn.run(app="logging_service.main:app",
                host=HTTP_HOST,
                port=LOGGING_PORT,
                reload=RELOAD,
                log_level=LOG_LEVEL)
    
    logging.info("Logging service run!")
    