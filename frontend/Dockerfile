FROM  node:8.7.0-alpine
RUN mkdir -p /vue-app
WORKDIR /vue-app


COPY . /vue-app

RUN npm install 


EXPOSE 8080

CMD ["npm", "run", "serve"]

