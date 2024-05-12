#!/bin/bash

# Update package lists
sudo apt update
sudo apt upgrade -y
# Install system-wide dependencies
sudo apt install -y python3-pip libjpeg-dev zlib1g-dev libssl-dev libgtk2.0-dev pkg-config ffmpeg libsm6 libxext6 cmake python3-opencv libportaudio2 libatlas-base-dev v4l2loopback-dkms avahi-dnsconfd openjdk-17-jdk libhdf5-dev

# Install Python packages
sudo -H pip3 install Pillow dlib face_recognition numpy opencv-contrib-python tflite-support tensorflow-aarch64 h5py deepface tf-keras mediapipe facenet-pytorch ultralytics

# Set permissions (if necessary)
# sudo chmod -R 777 .

# Install SDKMAN and Gradle
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install gradle
