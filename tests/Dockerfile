FROM  python:3.7
WORKDIR /test-app


COPY requirements.txt /test-app
RUN pip install -r requirements.txt 
COPY . /test-app

EXPOSE 3000
CMD ["./entrypoint.sh"]
