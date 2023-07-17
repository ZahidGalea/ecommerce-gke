# Use the official Docker Hub Nginx image
FROM nginx

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the build web folder to the nginx container
COPY build/web/ /usr/share/nginx/html

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf
