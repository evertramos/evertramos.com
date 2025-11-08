FROM node:20-alpine AS base

WORKDIR /app
COPY package*.json ./
RUN npm install --only=production

FROM base AS build
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]