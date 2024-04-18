#!/bin/sh
gnome-terminal -- bash -c "python3 client2.py client1; exec bash"
gnome-terminal -- bash -c "python3 client2.py client2; exec bash"
gnome-terminal -- bash -c "python3 client2.py client3; exec bash"
gnome-terminal -- bash -c "python3 client2.py client4; exec bash"
gnome-terminal -- bash -c "python3 client2.py client5; exec bash"

