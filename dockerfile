FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV TOKENIZERS_PARALLELISM=false

ENV HF_HOME=/data/hf_cache
ENV HF_HUB_CACHE=/data/hf_cache/hub
ENV TRANSFORMERS_CACHE=/data/hf_cache

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    git-lfs \
    tmux \
    htop \
    wget \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/local/bin/python
RUN ln -sf /usr/bin/pip3 /usr/local/bin/pip

RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install \
    torch \
    torchvision \
    --index-url https://download.pytorch.org/whl/cu128

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN pip install jupyterlab

WORKDIR /workspace/air_vast_experiments

COPY . /workspace/air_vast_experiments

RUN mkdir -p \
    /data/hf_cache \
    /data/datasets \
    /data/outputs \
    /data/results

EXPOSE 8888
EXPOSE 6006

CMD ["bash"]