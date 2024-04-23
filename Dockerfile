# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Set the working directory to /usr/local
WORKDIR /usr/local

# Update package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    libjpeg-dev \
    zlib1g-dev \
    libssl-dev \
    libgtk2.0-dev \
    pkg-config \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    libportaudio2 \
    libatlas-base-dev \
    v4l2loopback-dkms \
    avahi-dnsconfd \
    openjdk-17-jdk \
    curl \
    git

# Add Coral Edge TPU repository and install TFLite runtime
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y python3-tflite-runtime

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install Pillow dlib face_recognition numpy opencv-contrib-python tflite-support tensorflow-aarch64 python3-h5py deepface tf-keras ultralytics

# Install HDF5 development library
RUN apt-get install -y pkg-config libhdf5-dev

# Install SDKMAN and Gradle
RUN curl -s "https://get.sdkman.io" | bash && \
    bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install gradle"

RUN git clone https://github.com/squirrel-official/polestar.git

# Clone the repository and build the project
RUN git clone https://github.com/squirrel-official/polestar-konnect.git && \
    cd polestar-konnect && \
    gradle clean build

# Set permissions
RUN chmod -R 777 /usr/local

# Clear package cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set entrypoint or default command if needed

# Example entrypoint:
# ENTRYPOINT ["python3", "app.py"]

# Example default command:
# CMD ["python3", "app.py"]
