#!/bin/bash
timeout -s 9 $1 python temp/flowgraph.py > $2
