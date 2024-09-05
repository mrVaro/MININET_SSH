#!/bin/bash

# Deleting existing qdisc
tc qdisc del dev s1-eth1 root

sudo tc qdisc replace dev s1-eth1 parent root handle 100 taprio \
    num_tc 3 \
    map 0 0 0 0 1 1 2 2 \
    queues 1@0 1@0 1@0 \
    base-time 1000000000 \
    sched-entry S 04 800000 \
    sched-entry S 02 400000 \
    sched-entry S 01 200000 \
    flags 0x1 \
    clockid CLOCK_TAI

# Verifying the qdisc
tc qdisc show dev s1-eth1