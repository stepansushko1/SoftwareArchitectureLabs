import hazelcast
from time import sleep

client = hazelcast.HazelcastClient(cluster_name="dev")
queue = client.get_queue("queue").blocking()

for _ in range(1000):
    val = queue.take()
    print(f"Readed: {val}")
    sleep(0.01)
    if val == -1:
        queue.put(val)
        break

print("Consumer finished")

client.shutdown()