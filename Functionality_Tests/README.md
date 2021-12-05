# Troubleshooting with Functionality Tests
Included in this directory are a series of test scripts that can be used to confirm each part of the main script is behaving as expected.

### Included Tests:
* Socket Communication between Client-Server Nodes
* USB Cameras Connected and Reachable
* LED Setup
* Multiprocessing Functionality

## Verify Socket Communication between Client-Server Nodes
IMPORTANT: The following test should be run on both nodes. In this example the first test uses node01 as the server and node02 as the client.

### This test uses the following scripts:
* client_1to2com_test.py
* client_2to1com_test.py
* server_test.py

If this test does not behave as detailed below, refer back to the section on **Setting up Ad-Hoc Network between Nodes** in the [Main README](https://github.com/sfagin89/SmartTraffic/blob/main/README.md#setting-up-ad-hoc-network-between-nodes).

### Test Instructions
* On the server node run the following command:
  * ````
    pi@tnode01:~/Downloads $ python server_test.py
    Socket successfully created
    socket bound to <listening port>
    socket is listening
    ````
* On the client node run the following command:
  * ````
    pi@tnode02:~/Downloads $ python client_2to1com_test.py
    Socket successfully created
    The socket has successfully connected to node01
    Thank you for connecting
    ````
* On the server node, you should see the following response once the client node has connected and then close.
  * ````
    Got connection from ('192.168.0.20', <source port>)
    ````
