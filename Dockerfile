FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt
COPY ./test.py .
ENV FLASK_ENV=development
EXPOSE 5000
CMD [ "python", "./test.py" ]