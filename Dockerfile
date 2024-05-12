# Stage 1: Use ARM-compatible base image for Raspberry Pi 4
FROM --platform=linux/arm/v8 dtcooper/raspberrypi-os:python3.12-bookworm AS base

# Set timezone
ARG CONTAINER_TIMEZONE=UTC
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

# Update package lists and install necessary packages
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        python3-pip \
        libjpeg-dev \
        zlib1g-dev \
        libssl-dev \
        libgtk2.0-dev \
        pkg-config \
        libhdf5-dev \
        ffmpeg \
        libsm6 \
        libxext6 \
        cmake \
        python3-opencv \
        python3-h5py \
        libportaudio2 \
        libatlas-base-dev \
        openjdk-17-jdk \
        curl \
        git \
        unzip \
        zip \
        wget \
        python3-picamera2 \
        python3-libcamera \
        libcamera-apps \
        gfortran \
        libopenblas-dev && \
    pip3 install --upgrade pip

# Install Python packages individually for better caching
RUN pip3 install dlib -vvv
RUN pip3 install Pillow numpy opencv-contrib-python -vvv
RUN pip3 install ultralytics facenet-pytorch tensorflow-aarch64 deepface -vvv

# Install Gradle
ENV GRADLE_VERSION=8.7
RUN wget https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip \
    && mkdir /opt/gradle \
    && unzip -d /opt/gradle gradle-${GRADLE_VERSION}-bin.zip \
    && rm gradle-${GRADLE_VERSION}-bin.zip
ENV PATH=$PATH:/opt/gradle/gradle-${GRADLE_VERSION}/bin

# Stage 2: Clone repositories and build
FROM base AS builder

WORKDIR /usr/local/
RUN git clone https://github.com/squirrel-official/polestar.git && \
    git clone https://github.com/squirrel-official/polestar-konnect.git && \
    cd polestar-konnect && \
    gradle clean build

# Stage 3: Final image
FROM base AS final

COPY --from=builder /usr/local/polestar /usr/local/polestar

# Cleanup unnecessary packages and caches
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8087

# Set entrypoint
#ENTRYPOINT ["python3", "/usr/local/polestar/service/motionDetection.py"]
