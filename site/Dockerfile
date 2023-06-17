FROM node:14-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY ../site/ .

RUN npm run build

FROM nginx:stable-alpine as production

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
