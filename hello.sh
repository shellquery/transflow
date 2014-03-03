VIRTUAL_HOME=~/.transflow
WORK_HOME=`pwd`
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

enter
install
