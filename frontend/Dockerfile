FROM node:20-alpine AS base

WORKDIR /app
COPY package*.json ./
RUN npm install --only=production

FROM base AS build
RUN npm install
COPY . .

# Build arguments for environment variables
ARG PUBLIC_BACKEND_URL
ARG PUBLIC_TURNSTILE_SITE_KEY
ARG PUBLIC_STRIPE_CUSTOMER_PORTAL_URL

# Set environment variables for build
ENV PUBLIC_BACKEND_URL=$PUBLIC_BACKEND_URL
ENV PUBLIC_TURNSTILE_SITE_KEY=$PUBLIC_TURNSTILE_SITE_KEY
ENV PUBLIC_STRIPE_CUSTOMER_PORTAL_URL=$PUBLIC_STRIPE_CUSTOMER_PORTAL_URL

RUN npm run build

FROM nginx:alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]