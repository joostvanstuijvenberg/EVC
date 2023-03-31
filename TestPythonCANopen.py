import canopen
import time

if __name__ == '__main__':
    network = canopen.Network()
    network.connect(bustype='vector', channel=0, bitrate=500000)

    # This will attempt to read an SDO from nodes 1 - 127
    network.scanner.search()
    # We may need to wait a short while here to allow all nodes to respond
    time.sleep(0.05)
    for node_id in network.scanner.nodes:
        print("Found node %d!" % node_id)

    # node = network.add_node(48, '/path/to/v2g.eds')

    network.disconnect()
