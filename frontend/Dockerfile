# docker build -t :frontend .
# docker run -v ${PWD}:/app -v /app/node_modules -p 8081:8080 --rm my-app:dev

FROM  node:10 as build-stage

WORKDIR /vue-app

COPY package*.json ./

RUN npm install 

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]

