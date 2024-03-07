echo "creating user $PUID:$PGID"
addgroup -g "$PGID" inventoryhero
adduser -u "$PUID" -D inventoryhero -G inventoryhero
chown -R inventoryhero:inventoryhero /app

chown -R inventoryhero:inventoryhero /db
echo "nginxing"
nginx -g "daemon on;"
exec su inventoryhero -c "gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app"