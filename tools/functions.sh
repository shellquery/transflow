TOOLS_HOME=$WORK_HOME/tools
export TOOLS_HOME

source $TOOLS_HOME/uwsgi.sh
source $TOOLS_HOME/nginx.sh

function manage() {
    command=$1
    shift
    case $command in
        uwsgi)
            uwsgi $*
            ;;
        nginx)
            nginx $*
            ;;
    esac
}
