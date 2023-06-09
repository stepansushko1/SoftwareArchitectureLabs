from fastapi import FastAPI
import logging
import uvicorn
from get_config import get_config_from_json

HTTP_HOST, FACADE_PORT, LOGGING_PORT, \
    MESSAGES_PORT, RELOAD, LOG_LEVEL = get_config_from_json("config.json")

HTTP_OK = 200

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
app = FastAPI()


@app.get("/")
def handle_get():
    message_responce_template = {
        "msg": "Not implemented yet!",
    }
    return message_responce_template, HTTP_OK


if __name__ == "__main__":
    uvicorn.run(app="messages-service.main:app",
                host=HTTP_HOST,
                port=MESSAGES_PORT,
                reload=RELOAD,
                log_level=LOG_LEVEL)
    logging.info("Messages service run!")