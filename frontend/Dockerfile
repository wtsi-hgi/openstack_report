FROM  node:10

WORKDIR /vue-app


COPY package*.json ./

RUN npm install 

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]

