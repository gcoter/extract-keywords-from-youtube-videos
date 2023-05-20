FROM nvidia/cuda:11.3.1-base-ubuntu20.04

ARG USERNAME=gcoter
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG PROJECT_FOLDER=/workspaces/youtube-whisper-chatgpt

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=$PROJECT_FOLDER
ENV PATH=$PATH:/home/$USERNAME/.local/bin
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update \
    # Install Python
    && apt-get install -y python3.8 python3-pip python3-setuptools python3-distutils \
    # Install the system requirements of the project
    && apt-get install -y git nano libsndfile1 ffmpeg \
    # Cleaning
    && apt clean && rm -rf /var/lib/apt/lists/*

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

COPY requirements.txt $PROJECT_FOLDER/requirements.txt
WORKDIR $PROJECT_FOLDER

RUN python3 -m pip install -U pip pip-tools \
    && python3 -m pip install -r requirements.txt
