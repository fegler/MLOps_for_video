FROM nvcr.io/nvidia/tritonserver:24.05-py3

RUN apt-key del 7fa2af80 \
&& apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

RUN DEBIAN_FRONTEND=noninteractive \
apt-get update && \
apt-get install -y --no-install-recommends \
libcutensor1 libcutensor-dev \
libgl1-mesa-glx \
sudo && \
rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
     && pip install \
        torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126 \
     && pip install opencv-python loguru ujson numpy albumentations \
     && pip install --upgrade pillow \
     && pip install transformers==4.38.2 \
         decord onnxruntime accelerate scikit-learn einops


WORKDIR /opt/tritonserver