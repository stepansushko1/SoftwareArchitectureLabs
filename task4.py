import timeit
import hazelcast
from time import sleep


def setup_client():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    my_map = client.get_map("my-distributed-map").blocking()


def no_lock():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    my_map = client.get_map("my-distributed-map").blocking()
    key = "1"
    my_map.put(key, 0)

    for _ in range(1000):
        val = my_map.get(key)
        sleep(0.01)
        val += 1
        my_map.put(key, val)

    print(f"Result no locking = {my_map.get(key)}")
    client.shutdown()


def pessimistic_locking():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    my_map = client.get_map("my-distributed-map").blocking()
    key = "1"
    my_map.put(key, 0)

    for _ in range(1000):
        my_map.lock(key)
        try:
            val = my_map.get(key)
            sleep(0.01)
            val += 1
            my_map.put(key, val)
        finally:
            my_map.unlock(key)

    print(f"Result pessimistic = {my_map.get(key)}")
    client.shutdown()


def optimistic_locking():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    my_map = client.get_map("my-distributed-map").blocking()
    key = "1"
    my_map.put(key, 0)

    for _ in range(1000):
        while True:
            new_val = old_val = my_map.get(key)
            sleep(0.01)
            new_val += 1
            if my_map.replace_if_same(key, old_val, new_val):
                break

    print(f"Result optimistic = {my_map.get(key)}")
    client.shutdown()


setup_client()
print("No locks execution time:",
      timeit.timeit(setup=setup_client, stmt=no_lock, number=1))

print("Pessimistic locks execution time:",
      timeit.timeit(setup=setup_client, stmt=pessimistic_locking, number=1))

print("Optimistic locks execution time:",
      timeit.timeit(setup=setup_client, stmt=optimistic_locking, number=1))
