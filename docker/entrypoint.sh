init(){
  echo "init Flask-Migrate migrations"
  flask db migrate
  flask db upgrade
  echo "Flask-Migrate migrations finished"


  python3 /app/inventoryhero/backend/db/create_admin.py

  exit_code=$?
  if [ $exit_code -eq 1 ]; then
      echo "The script ended with an error."
      exit $exit_code
  fi


}


echo "creating user $PUID:$PGID"
addgroup -g "$PGID" inventoryhero
adduser -u "$PUID" -D inventoryhero -G inventoryhero
chown -R inventoryhero:inventoryhero /app/inventoryhero
echo "starting nginx"
nginx -g "daemon on;"
init
exec su inventoryhero -c "gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 backend.app:app"