import json

# JSON_PATH = "config.json"

def get_config_from_json(json_path):
    """
    Reads json file and returns necessary information
    for microservices (host, ports, log_level)
    """
    try:

        config_file = open(json_path, mode="r", encoding="UTF-8")
        config = json.load(config_file)

    except Exception:

        return "Incorrect json path"

    return config["HOST"], config["PORTS"]["FACADE_PORT"], config["PORTS"]["LOGGING_PORT"], \
        config["PORTS"]["MESSAGES_PORT"], config["RELOAD"], config["LOG_LEVEL"]
    