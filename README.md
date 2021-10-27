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
1. The individual nodes (1 per intersection), should recognized the presense of vehicles, be able to count them, and determine their direction relative to the current intersection.
2. The nodes should be able to communicate between each other, passing and receiving intersection traffic information.
3. An algorithm that the nodes can use to determine how traffic lights should be adjusted to improve traffic flow in areas of congested traffic, based on the traffic information at their node, as well as all other nodes they hold traffic information for.

## If the above is finished, a reach goal will be attempted:
* Securing the individual nodes and the communication between them to prevent compromised nodes. While security will be taken into account during the main project, additional, redundant security will be considered here.

## Expanding on the above goals
### Vehicle Recognition
* How will the Intersection node recognize vehicles at its intersection?
* How will the Intersection node determine the directionality of the vehicles?
### Node Communication
* How will the Nodes communicate and share traffic information with each other?
* How will Nodes store traffic information received from other nodes?
### Traffic Adjustment Algorithm
* What algorithm will be used to determine how individual nodes should adjust their traffic light speeds to improve traffic conditions at their own and other intersections?

## Planned Testing Setup
* A minimum of 2 nodes will be needed in order to demonstrate the ability of the nodes to communicate with each other, as well as show how the speeds of the lights will adjust at an intersection based on traffic at another intersection.
