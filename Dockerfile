FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt
COPY ./test.py .
CMD [ "python", "./test.py" ]