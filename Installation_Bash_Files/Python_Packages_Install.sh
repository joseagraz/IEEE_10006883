#!/bin/bash
echo "--------------------------------------------"
echo "Name:         Applications and Packages Installer"
echo "Author:       Jose L. Agraz, PhD"
echo "Description:  Installing Applications and Packages for Normalization scripts,"
echo "Note:         Verify Installation is in the appropriate"
echo "              environment (ex. conda activate Normalization_Libraries_2021)"
echo "Date:         10/25/2021"
echo "Usage: sudo ./PythonPackagesInstall"
echo "--------------------------------------------"
echo "Updating Ubuntu software and patches"
apt-get update   -y
apt-get upgrade  -y
echo "--------------------------------------------"
echo "Libcanberra, necesary to execute Komodo IDE"
apt-get install libcanberra-gtk-module -y
echo "--------------------------------------------"
echo "Installing Pip"
apt-get install python3-pip
#echo "--------------------------------------------"
#echo "Installing OpenSlide"
#apt-get install python3-openslide
echo "--------------------------------------------"
echo "Installing tkinter. Enables matlablib plotting"
apt-get install python3-tk
echo "--------------------------------------------"
echo "Invalidating user's cached credentials"
sudo -k
echo "Done"
