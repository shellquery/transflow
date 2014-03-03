UWSGI_HOME=$VIRTUAL_HOME/etc/uwsgi
UWSGI_CONFIG=$UWSGI_HOME/$PROJECT_NAME.json
RUN_DIR=$VIRTUAL_HOME/var/run
UWSGI_PID=$RUN_DIR/$PROJECT_NAME.pid
UWSGI_LOG=$VIRTUAL_HOME/var/log/uwsgi.log
UWSGI_SOCK=$RUN_DIR/$PROJECT_NAME.sock

function uwsgi_mkdirs() {
    mkdir -p $UWSGI_HOME
    mkdir -p $RUN_DIR
}

function uwsgi() {
    subcommand=$1
    uwsgi_mkdirs
    case $subcommand in
        start)
            uwsgi --json $UWSGI_CONFIG
            ;;
        stop)
            uwsgi --stop $UWSGI_PID
            ;;
        reload)
            uwsgi --reload $UWSGI_PID
            ;;
        init)
            read -d '' content <<EOF
{"uwsgi": {
  "vhost": "true",
  "venv": "$VIRTUAL_HOME",
  "chdir": "$WORK_HOME",
  "socket": ["$UWSGI_SOCK", "localhost:88888"],
  "module": "transflow".
  "callable": "app",
  "pid": "$UWSGI_PID",
  "logto": "$UWSGI_LOG",
  "master": true,
  "workers": 3
}}
EOF
            echo $content > $UWSGI_CONFIG
            ;;
    esac
}
