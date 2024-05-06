# Use Ubuntu 20.04 as base image or 23.04
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
    pkg-config

RUN apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    python3-opencv \
    python3-h5py \
    libportaudio2 \
    libatlas-base-dev

RUN apt-get install -y \
    openjdk-17-jdk \
    curl \
    git
# Install additional Python packages
RUN pip3 install Pillow
RUN pip install dlib -vvv
RUN pip3 install face_recognition numpy
RUN pip3 install numpy
RUN pip3 install opencv-contrib-python
RUN pip3 install tflite-support  -vvv
RUN pip3 install --upgrade pip
RUN pip3 install deepface tf-keras facenet-pytorch ultralytics
RUN pip3 install tensorflow-aarch64  -vvv



# Install TFLite runtime
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y python3-tflite-runtime


RUN apt-get install -y unzip zip wget

ENV GRADLE_VERSION=8.7
RUN wget https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip \
    && mkdir /opt/gradle \
    && unzip -d /opt/gradle gradle-${GRADLE_VERSION}-bin.zip \
    && rm gradle-${GRADLE_VERSION}-bin.zip
# Set Gradle path
ENV PATH=$PATH:/opt/gradle/gradle-${GRADLE_VERSION}/bin


RUN pip3 install meson
RUN pip3 install ply
RUN apt install ninja-build

RUN cd /opt \
    && git clone https://github.com/raspberrypi/libcamera.git
WORKDIR /opt/libcamera
RUN meson build
#RUN ninja -C build install -j4 --prefix=/opt/libcamera
ENV export INSTALL_PREFIX=/opt/libcamera
RUN ninja -C build install -j4
RUN echo "hello"

WORKDIR /usr/local/
RUN git clone https://github.com/squirrel-official/polestar.git
#RUN git clone https://github.com/squirrel-official/polestar-konnect.git

#RUN cd polestar-konnect && gradle clean build

# Cleanup unnecessary packages and caches
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

RUN pip3 install picamera2
RUN  python3 "/usr/local/polestar/service/motionDetection.py"

EXPOSE 8087

# Set entrypoint if needed
ENTRYPOINT ["python3", "/usr/local/polestar/service/motionDetection.py"]
