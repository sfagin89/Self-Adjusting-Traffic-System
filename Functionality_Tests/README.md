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

## Verify All Connected USB Cameras are Reachable
IMPORTANT: The following test requires the python cv2 module. Unless done so outside of this project, the cv2 module has only been installed within the tflite virtual environment, so this test should be run within that environment.

### This test uses the following script:
* cam_test.py

### Test Instructions
* On both nodes from within the activated tflite environment, run the following command:
  * ````
    python cam_test.py
    ````

## Verify Traffic Light LEDs are connected correctly

### This test uses the following script:
* led_ctrl_test.py

### Test Instructions:
* On both nodes, run the following command:
  * ````
    pi@tnode02:~/Downloads $ python led_ctrl_test.py
    Enter the input:
    ````
* Entering one of the following numbers will set the LEDs to run a single cycle of a specific traffic light pattern. Each LED should stay lit for 5 seconds.
  * 1 = Normal Cycle [Red -> Yellow -> Green]
  * 2 = Altered Cycle [Red -> Green]
  * All other values = Error Cycle [Red]
* When a full cycle has completed, you will be prompted to enter another number.
  * ````
    pi@tnode02:~/Downloads $ python led_ctrl_test.py
    Enter the input: 1
    Enter the input: 2
    Enter the input: 0
    ````
* To Exit the script, enter ```Ctrl + c```
  * ````
    pi@tnode02:~/Downloads $ python led_ctrl_test.py
    Enter the input: ^C

    pi@tnode02:~/Downloads $
    ````

## Verify Python Multiprocessing is Behaving as Expected

### This test uses the following script:
* multiproc_test.py

### Test Instructions:
* On both nodes, run the following command:
  * ````
    pi@tnode02:~/Downloads $ python multiproc_test.py
    ````
* If the script is functioning as expected, and the LEDs are connected correctly, the following LED pattern should be displayed:
  * Red On/Off -> Yellow On/Off -> Green On/Off -> Red On/Off -> Yellow On/Off -> Red On/Off -> Green On/Off -> Red On/Off -> Green On/Off -> Red On/Off -> Red On/Off -> Red On/Off -> Red On/Off -> Red On/Off -> Red On/Off
  * The above pattern represents 10 seconds of Flashing Normal Cycle, then 10 seconds of Flashing Altered Cycle, and finally 10 seconds of Flashing Error Cycle until starting from the beginning.
* To Exit the script, enter ```Ctrl + c```
  * ````
    pi@tnode02:~/Downloads $ python multiproc_test.py
    ^C
    script exiting

    pi@tnode02:~/Downloads $
    ````
