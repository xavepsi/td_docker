# Étape 1: Builder Node
FROM node:18-alpine AS builder
WORKDIR /app
COPY index.html app.js ./
RUN mkdir -p /dist && cp index.html app.js /dist/

# Étape 2: Nginx
FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=builder /dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
