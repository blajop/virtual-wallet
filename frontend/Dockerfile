# syntax=docker/dockerfile:1

FROM node:18-alpine
ENV NODE_ENV=production

WORKDIR /root

COPY ["package.json", "package-lock.json*", "./"]

RUN apk update
RUN apk add nodejs npm
RUN npm install -g create-vite



RUN npm install

COPY . .

EXPOSE 3000

# CMD ["npm", "run", "dev"]