FROM nginx:latest
COPY src/html /usr/share/nginx/html
WORKDIR /app
COPY start-nginx.sh .
CMD ["sh","start-nginx.sh"]