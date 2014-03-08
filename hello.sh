PROJECT_NAME=transflow
VIRTUAL_HOME=~/.$PROJECT_NAME
WORK_HOME=`pwd`
export PROJECT_NAME
export VIRTUAL_HOME
export WORK_HOME

virtualenv $VIRTUAL_HOME

function enter() {
    source $VIRTUAL_HOME/bin/activate
}

function bye() {
    deactivate
}

function install() {
    pip install flask
    pip install psycopg2
    pip install flexmock
    pip install flask-wtf
    pip install flask-redis
    pip install flask-mail
    pip install flask-sqlalchemy
    pip install flask-testing
    pip install flask-rq
    pip install alembic
    pip install nose
    pip install uwsgi
    easy_install readline
    pip install ipython
    pip install anyjson
    pip install iptools
    pip install sqlalchemy-compiler
}

function cdvirtual() {
    cd $VIRTUAL_HOME
}

function cdwork() {
    cd $WORK_HOME
}

function cdlib() {
    cd $VIRTUAL_HOME/lib/python2.7/site-packages
}

source $WORK_HOME/tools/functions.sh

enter
install
