FROM python:3.9.12-slim
WORKDIR /modularlab/src
RUN apt-get -y update && apt-get install -y python3-dev python3-setuptools wget unzip
COPY ./requirements.txt /modularlab/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /modularlab/requirements.txt 
RUN pip3 install Pillow torch torchvision
ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONBUFFERED \
    PYTHONPATH "${PYTHONPATH}:/modularlab/src" 
COPY ./src .
CMD uvicorn app:app --reload --host=0.0.0.0 --port=3001