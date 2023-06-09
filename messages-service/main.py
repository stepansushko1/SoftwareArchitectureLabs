from fastapi import FastAPI
import logging
import uvicorn
from get_config import get_config_from_json
import hazelcast
from threading import Thread

HTTP_HOST, FACADE_PORT, LOGGING_PORT, \
    MESSAGES_PORT, RELOAD, LOG_LEVEL = get_config_from_json("config.json")

HTTP_OK = 200


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
app = FastAPI()


hz = hazelcast.HazelcastClient(cluster_name="dev")
print("Connected to Hazelcast instance")
queue = hz.get_queue("my-queue").blocking()
queue.clear()
data = []


def getting_msg():
    while True:
        item = queue.take()
        print("Consumed :", item)
        data.append(item)

thr = Thread(target=getting_msg)
thr.start()

@app.get("/")
def handle_get():
    message_responce_template = {
        "msg": data,
    }
    return message_responce_template, HTTP_OK

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    uvicorn.run(app="messages-service.main:app",
                host=HTTP_HOST,
                port=port,
                reload=RELOAD,
                log_level=LOG_LEVEL)
    logging.info("Messages service run!")