# SoftwareArchitectureLabs
Labs for UCU course

## Run instruction

<code> cd SoftwareArchitectureLabs </code>, 
<code> python3 -m facade.main </code>, 
<code> python3 -m logging_service.main </code>, 
<code> python3 -m messages_service.main </code>


## Curl Requests

For POST: <code> curl -X POST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"msg": "your_message"}' </code>


For GET: <code> curl http://127.0.0.1:8000 </code>