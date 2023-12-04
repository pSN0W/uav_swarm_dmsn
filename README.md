# uav_swarm_dmsn

## Introduction
This is implementation of the paper UAV Swarm for Connectivity Enhancement of Multiple Isolated Sensor Networks for Internet of Things Application. This was built for my DMSN project. The goal here is to design a path for the UAV Swarm to enhance the communication between the MISN. The UAVs are structured in a closed loop form and the Ant Colony Optimization is used to generate the paths for the UAVs.

## Start
Open terminal and run the following commands to start the application
- Clone the repo
```
git clone https://github.com/pSN0W/uav_swarm_dmsn.git
```
- Go to the directory
```
cd uav_swarm_dmsn
```
- To start the application run
```
python3 gui.py
```
> You don't need to install anything as we use the standard python libraries

## Configs
You can modify the configs to generate different outputs. The description of the config are
- num_sink_node: Number of sink node to consider in the MISN
- max_dist_btw_sink_node: The maximum distance between two sink node. Used in random generation of MISN
- min_dist_btw_sink_node: The minimum distance between two sink node. Used in random generation of MISN
- max_communication_time: Maximum time taken by the sink node to transfer the data to UAV
- min_communication_time: Minimum time taken by the sink node to transfer the data to UAV. The time taken by the sink node is generated randomly from it
- num_uav: Number of UAV to consider
- height: Height of the UAV
- radius: Communication distance of the UAV

- num_ants: Number of ants used in ant colony optimization
- num_epochs: Number of epoch used in ant colony optimization
