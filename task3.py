import hazelcast

hz = hazelcast.HazelcastClient(cluster_name="dev")

map = hz.get_map("my-distributed-map").blocking()
for i in range(1000):
    print(i)
    map.put(i, "value")

hz.shutdown()
