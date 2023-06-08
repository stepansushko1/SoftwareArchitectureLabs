import hazelcast
from time import sleep

client = hazelcast.HazelcastClient(cluster_name="dev")

queue = client.get_queue("queue").blocking()

for i in range(1000):
    queue.put(i)
    print(f"Written {i}")
    sleep(0.01)

queue.put(-1)
print("Writting finished")

client.shutdown()