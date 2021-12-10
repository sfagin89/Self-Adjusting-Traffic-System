# SmartTraffic
A System to improve traffic congestion using 'smart' traffic lights

## MVP
A smart traffic light system that is able to recognize, count, and determine the directionality of vehicles at its intersection to create a better traffic route.

## Layout of System
* Each intersection acts as a single 'node'
* Each node is comprised of a controller that connects with 4 cameras
* The 4 cameras are positioned to face each point of ingress to the intersection
* Each node will directly connect to it's neighboring nodes in a mesh network

## A successful finished product should include the following:
1. The individual nodes (1 per intersection), should recognized the presence of vehicles, be able to count them, and determine their direction relative to the current intersection.
2. The nodes should be able to communicate between each other, passing and receiving intersection traffic information.
3. An algorithm that the nodes can use to determine how traffic lights should be adjusted to improve traffic flow in areas of congested traffic, based on the traffic information at their node, as well as all other nodes they hold traffic information for.

## If the above is finished, a reach goal will be attempted:
* Securing the individual nodes and the communication between them to prevent compromised nodes. While security will be taken into account during the main project, additional, redundant security will be considered here.

## Expanding on the above goals
### Phase 1 - Vehicle Recognition
* How will the Intersection node recognize vehicles at its intersection?
  * Google Maps API, or another source of live traffic data was considered. However after looking into how this information is collected and used, and possible ways to abuse the system[^1], we determined to not go with this route.
  * The current plan is to implement Real-Time Object Detection to observe and recognize individual vehicles at each intersection. A set of fisheye lens cameras will be placed at each ingress point of the intersection. Using the feed from these cameras, the individual vehicles will be detected and recognized using the machine learning platform **TensorFlow**[^2].
  * Were considering either the TensorFlow Object Detection API[^3], an open-source framework build on top of TensorFlow, or YOLO TensorFlow ++[^4], a TensorFlow implementation of the YOLO: Real-Time Object Detection algorithm.
* How will the Intersection node determine the directionality of the vehicles?
  * This will be achieved simply by determining which camera is observing the traffic. This becomes more complicated if a single central camera were used.
* Phase 1 Implementation update:
  * Due to using Raspberry Pis as our traffic nodes, the full TensorFlow platform may be too powerful to run effectively. Taking that into account, we have instead gone with **TensorFlow Lite**[^8], an open-source framework built to run on mobile and IoT devices.
  * Using a guide created by **Edje Electronics**[^9][^10] guide, TensorFlow Lite was installed on a Raspberry Pi, along with a simple webcam, and tested on a local street view.
  ![Result of Initial TFLite Test 1](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Object_Detection_Test_1.png?raw=true)
  ![Result of Initial TFLite Test 2](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Object_Detection_Test_2.png?raw=true)
  * A sample TFLite model provided by Google was used as the Detection Model for this test, pulled using the following command:
  ```
  wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
  ```
  * Some work needs to be done to improve the accuracy. May look into using an accelerator of some kind, as mentioned in the Edje Electronics guide. The above test was run using a Raspberry Pi 3. Further implementations will be done on a Raspberry Pi 4, which during benchmark chests has displayed CPU performance improvements of as much as +36%, and GPU performance improvements ranging from +34% - 70% depending on the function being tested[^11]. This increase in CPU and GPU performance should provide significant improvement in the speed and accuracy of the TensorFlow Object Detection.
  * The data produced by the script still needs to be stored and ready to transmit to other nodes.
* Phase 1 Implementation update 11/16/21:
  * Updated the TFLite Webcam script to output the results to a file as well, to allow for the nodes to send this information to other nodes.
  * After testing the new webcams running TFLite to identify hot-wheel cars, the accuracy was very poor. At no point were the cars recognized as cars. Most of the time the model was unable to identify them as objects, and when it did, it thought they were suitcases.
  ![Result of Initial TFLite Test 3](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Object_Detection_Test_3_111621.png?raw=true)
  * After some additional research, we're strongly considering training our own model.
    * https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10
* Phase 1 Implementation update 11/28/21:
  * Adjusted viewing angle of cameras from front to side view. This, in addition to reducing 'clutter' appears to have improved the accuracy of the detection model.
  ![Result of Initial TFLite Test 4](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Object_Detection_Test_4_113021.png?raw=true)
  * Additionally, a new custom model based on images of the toy cars used in our demo has been trained. Currently in the process of converting it work with TensorFlow Lite.
  * Pre-trained Model: ssd_mobilenet_v2, Train images: 248 (80%), Test images: 62 (20%)
  ![Result of Custom Model 1](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Custom_model_output1.png?raw=true)
  ![Result of Custom Model 2](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Custom_model_output2.png?raw=true)
    * A Custom model was trained on Google Colab Pro. The Tensorflow model Github repository was cloned directly to Google Colab Pro and the output saved to Google Drive. The notebook [trainmodel.ipynb](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Custom_model/trainmodel.ipynb) contains steps on how to train Smart Traffic's custom model, however, some steps are omitted inside the notebook. A [readme](https://github.com/sfagin89/SmartTraffic/blob/main/Custom_model/README.md) has been provided with detailed instructions on how to train Smart Traffic's custom model.


### Phase 2 - Node Communication
* How will the Nodes communicate and share traffic information with each other?
  * Considered whether a star topology or a mesh topology would work better. A star topology with a central device that communicated with all nodes would allow for a more resource/computationally heavy algorithm. However, this may introduce issues with speed of response times, as traffic information would have to be sent from each node to the central unit, run through an algorithm on that unit, and then sent back to all of the nodes.
  * The current plan is use a partial mesh topology, allowing direct communication between the nodes, as well as providing link redundancy.
* How will Nodes store traffic information received from other nodes?
  * We are treating this similar to how network routers behave, where a routing table is formed based on route information received from other routers, and the best route is determined using a set of metrics dependent on the routing protocol in use. Similarly, the traffic information sent from other nodes will be stored, and the information later used by our Traffic Algorithm to determine the best way to route traffic by adjusting timing of traffic lights.
* Phase 2 Implementation update 11/16/21:
  * Set up an Ad-Hoc network between the 2 nodes over ethernet.
  * Wrote a pair of scripts to set up the nodes as a TCP/IP Server or Client, to allow communication over a specified port.
  * Tested sending messages between the nodes, as well as sending the contents of a file from one node to another.
* Phase 2 Implementation update 11/30/21:
  * Incorporated Socket Communication into main Object Detection Script.
  * Client and Server traffic nodes now sum the total count of cars at an intersection (by cycling through each camera connected to the node) then send that information to the neighboring node, as well as receives that information from the neighboring node.
  ![Current Result of Node Communication between Client and Server Nodes](https://github.com/sfagin89/SmartTraffic/blob/main/Images/Code_Output_ServerClient.png?raw=true)
### Phase 3 - Traffic Adjustment Algorithm
* What algorithm will be used to determine how individual nodes should adjust their traffic light speeds to improve traffic conditions at their own and other intersections?
  * Currently researching existing Traffic Congestion Models, as well as previous research into this topic.[^5][^6][^7][^15]
* Phase 3 Implementation update 11/30/21:
  * Researched Typical Traffic Signal behavior, Methods for Signal Coordination and Detection Systems.[^14]
    * Cycle Length:
      * A full Cycle Length (the amount of time required to display all phases for each direction of an intersection before returning to the starting point) typically range from 1-3 minutes, and are based on traffic volume and conditions of intersections.
      * The goal of signal timing is to find an optimum cycle length for the most efficiency.
      * Clearance interval times (when changing from one signal phase to the next) are calculated based on speed limit, intersection widths, intersection grades, perception or start-up time, and acceleration rates.
    * Pre-Timed vs Actuated Signal Timings:
      * Traffic Signal Behavior is typically Pre-Timed, Semi-Actuated, or Fully-Actuated.
      * Based on traffic trends, various signal timing plans can be set up in the signal controller.
    * Detection:
      * Detection systems are critical to actuated signals, using various methods to detect a vehicle’s approach.
      * Currently the most reliable form of vehicle detection in use are Inductance loops
    * Software (Traffic Signal Controller):
      * The 'brains' of the traffic signal.
      * Tells the signal what to run, how long to run, when to run, etc.
      * Collects information from the intersection through the detection system, decides how to respond, and then tells the traffic signal lights how to operate.
      * CALTRANS 2070 traffic signal controller standards
  * Paper: Real-time traffic signal optimization model based on average delay time per person.[^15]
    * Focused on the interrelations between signal parameters (cycle length, split, etc) and evaluation indices (delay time, queue length, number of stops, etc)
      * Delay Time
        * Fixed time signals have been proposed as a method to achieve minimum average delay time.
      * Queue Length constraints
      * Spillback phenomenon
    * Australian Road Research Board method (ARRB)
      * Considers both number of stops and delay time
    * New models have been proposed, introducing changes in signal models and objectives
      * Cedar & Reshetnik proposed two signal models for under-saturated and over-saturated intersections, using minimization of maximum queue length and accumulative queue length as two objective functions.[^16]
      * Fuzzy Logic
    * In both mathematical programming approaches and simulation-based systems, minimum delay time at intersection is a very important objective.
* Current Planned Approach:
  * Proof of Concept: Reduce Signals from 3 to 2 when the difference in vehicles per intersection exceeds a predetermined threshold.
* Phase 3 Implementation update 12/6/21:
  * Determined that multiprocessing would be required to run both the light controller and the main script that sends update signals to it.
  * Successfully implemented multiprocessing in the main script.
    * A Function called traffic_control, used to cycle traffic lights through a set of phases depending on the current traffic mode. Mode is taken from a shared queue that is added to by a separate function called mode_set.
    * traffic_control loops indefinitely once it's called as a separate process from within the main script. Each loop of the main script determines whether the traffic mode needs to change, then sends the new mode to mode_set, which adds the value to the queue for the traffic_control to read.
      * The traffic mode is determined based on the difference in vehicles between the two intersections. If the local node has a higher number of cars then the remote node, the local node will set the traffic mode to the Altered State. Otherwise the mode is set to Normal State.
      * This is not the intended final implementation of the traffic algorithm, just a place holder to confirm everything works.


## Physical Prototype for Testing Setup
![General Plan for Layout of SmartTraffic System Test](https://github.com/sfagin89/SmartTraffic/blob/main/Images/TrafficIntersectionModel.png?raw=true)
* A minimum of 2 nodes will be needed in order to demonstrate the ability of the nodes to communicate with each other, as well as show how the speeds of the lights will adjust at an intersection based on traffic at another intersection.

## Setting Up the Raspberry Pi as a Traffic Node
Instructions to configure a raspberry pi as a Traffic Node, as well as physically setting up the pi, have been provided in the Setup_Instructions directory, [HERE](https://github.com/sfagin89/SmartTraffic/blob/main/Setup_Instructions/README.md)

## Troubleshooting The Raspberry Pi Traffic Node
Functionality Testing Scripts to help with troubleshooting and setup of a Raspberry Pi Traffic Node have been provided in the Functionality_Tests directory, [HERE](https://github.com/sfagin89/SmartTraffic/blob/main/Functionality_Tests/README.md)

## Begin Smart Traffic Application
### Running TensorFlow Lite:
* Activate the tflite environment setup previously.
  * ```source tflite1-env/bin/activate```

* Run the following command to start Tensorflow Lite:
  * ```python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model```

* You will then be prompted to run the node in Server or Client mode. Assuming the nodes were setup using the [Setup_Instructions](https://github.com/sfagin89/SmartTraffic/blob/main/Setup_Instructions/README.md#setting-up-ad-hoc-network-between-nodes), Node02 should be run as the Server, and Node01 as the client
  * ````
    (tflite1-env) pi@tnode01:~/tflite1 $ python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model
    Successfully Created Global Socket
    Run this Node in (S)erver or (C)lient mode?: C
    ````
  * ````
    (tflite1-env) pi@tnode02:~/tflite1 $ python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model
    Successfully Created Global Socket
    Run this Node in (S)erver or (C)lient mode?: S
    ````

* To exit the program, enter Ctrl + C

[^1]: https://www.theguardian.com/technology/2020/feb/03/berlin-artist-uses-99-phones-trick-google-maps-traffic-jam-alert
[^2]: https://www.tensorflow.org/
[^3]: https://github.com/tensorflow/models/tree/master/research/object_detection
[^4]: https://modelzoo.co/model/yolo-tensorflow
[^5]: https://iopscience.iop.org/article/10.1088/1742-6596/801/1/012048/pdf
[^6]: https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-30440-3_559#howtocite
[^7]: https://en.wikipedia.org/wiki/Traffic_model
[^8]: https://www.tensorflow.org/lite
[^9]: https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Raspberry_Pi_Guide.md
[^10]: https://www.youtube.com/watch?v=aimSGOAUI8Y&ab_channel=EdjeElectronics
[^11]: https://www.geeks3d.com/20190930/raspberry-pi-4-vs-raspberry-pi-3-cpu-and-gpu-benchmarks/
[^14]: https://www.foresitegroup.net/a-beginners-guide-to-signal-timing/
[^15]: https://journals.sagepub.com/doi/full/10.1177/1687814015613500
[^16]: https://link.springer.com/article/10.1057/palgrave.jors.2601138
[^17]: https://www.geeksforgeeks.org/socket-programming-python/
[^18]: https://zetcode.com/python/multiprocessing/
