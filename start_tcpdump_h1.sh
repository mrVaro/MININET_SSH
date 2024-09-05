#!/bin/bash
sudo ip link add link h1-eth0 name h1-eth0.5 type vlan id 5 egress-qos-map 6:2 5:1 4:1 3:0 2:0 1:0 0:0
sudo ip link set dev h1-eth0.5 up

# Start tcpdump on h1
iperf3 -s &
sudo tcpdump -i h1-eth0 -w /media/sf_MININET_SSH/RESULT/capture.pcap
