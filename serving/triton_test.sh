MODEL_REPOSITORY_PATH=`pwd`/model_repository

TRITON_MODEL_REPOSITORY_PATH=/models

docker run \
    --gpus '"device=0"' -it --rm \
    --ipc=host \
    -p 8000:8000 \
    -p 8001:8001 \
    -p 8002:8002 \
    --name triton_test \
    -v $MODEL_REPOSITORY_PATH:$TRITON_MODEL_REPOSITORY_PATH \
    triton_dev:24.05 tritonserver \
    --model-repository=/models \
    --strict-model-config=false \
    --model-control-mode=poll \
    --repository-poll-secs=10 \
    --backend-config=tensorflow,version=2 \
    --log-verbose=0