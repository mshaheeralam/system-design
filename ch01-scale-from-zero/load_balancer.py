class LoadBalancer:
    """Spreads requests across web servers using round-robin.

    Servers that are marked down are skipped, like a real load balancer
    that stops routing to a server once its health check fails.
    """

    def __init__(self, servers):
        self.servers = servers  # list of WebServer objects
        self.down = set()       # servers currently marked down
        self.index = 0          # position of the next server to try

    def mark_down(self, server):
        self.down.add(server)

    def mark_up(self, server):
        self.down.discard(server)

    def next_server(self):
        for _ in range(len(self.servers)):
            server = self.servers[self.index % len(self.servers)]
            self.index += 1
            if server not in self.down:
                return server

        # if we get here, all servers are down
        raise RuntimeError("no healthy servers")

if __name__ == "__main__":
    # Self-check: run `python load_balancer.py`. Every line should print True.
    # Plain strings stand in for WebServer objects: the load balancer doesn't care what they are.
    lb = LoadBalancer(["A", "B", "C"])
    print([lb.next_server() for _ in range(6)] == ["A", "B", "C", "A", "B", "C"])

    lb.mark_down("B")
    print([lb.next_server() for _ in range(4)] == ["A", "C", "A", "C"])

    lb.mark_up("B")
    lb.mark_up("B")  # must not crash
    print(set(lb.next_server() for _ in range(3)) == {"A", "B", "C"})

    for s in ["A", "B", "C"]:
        lb.mark_down(s)
    try:
        lb.next_server()
        print(False)  # should not get here
    except RuntimeError:
        print(True)   # all servers down -> exception
