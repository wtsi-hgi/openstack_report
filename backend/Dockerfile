FROM  python:3.7
WORKDIR /app


COPY requirements.txt /app
RUN pip install -r requirements.txt 
COPY . /app

EXPOSE 3000
CMD ["./entrypoint.sh"]


