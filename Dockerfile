# Use Ubuntu 20.04 as base image
# Use ARM-compatible base image for Raspberry Pi 4
FROM arm64v8/ubuntu:20.04


RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
ARG DEBIAN_FRONTEND=noninteractive


# Update package lists and install necessary packages
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
    python3-opencv \
    python3-h5py \
    libportaudio2 \
    libatlas-base-dev \
    v4l2loopback-dkms \
    avahi-dnsconfd \
    openjdk-17-jdk \
    curl \
    git

# Install additional Python packages
RUN pip3 install Pillow dlib face_recognition numpy opencv-contrib-python tflite-support tensorflow-aarch64 deepface tf-keras mediapipe facenet-pytorch ultralytics

# Install TFLite runtime
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y python3-tflite-runtime

# Install SDKMAN for managing Java dependencies
RUN curl -s "https://get.sdkman.io" | bash && \
    source "$HOME/.sdkman/bin/sdkman-init.sh" && \
    sdk install gradle

# Set working directory
WORKDIR /usr/local/

# Clone repository and build with Gradle
RUN chmod -R 777 . && \
    git clone https://github.com/squirrel-official/polestar-konnect.git && \
    cd polestar-konnect && \
    gradle clean build

# Expose any required ports here if needed

# Define any startup commands or entrypoints here if needed

# Cleanup unnecessary packages and caches
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions
RUN chmod -R 777 /usr/local/polestar-konnect

# Set entrypoint if needed
ENTRYPOINT ["python3", "/usr/local/polestar/service/motionDetection.py"]

