sed -i "s/WEBSOCKET_SERVER/$WEBSOCKET_SERVER/" /usr/share/nginx/html/main.js
nginx -g 'daemon off;'