require.config({
    paths: {
        'lib/jquery': '../bower_components/jquery/jquery',
        'lib/bootstrap/affix': '../bower_components/sass-bootstrap/js/affix',
        'lib/bootstrap/alert': '../bower_components/sass-bootstrap/js/alert',
        'lib/bootstrap/button': '../bower_components/sass-bootstrap/js/button',
        'lib/bootstrap/carousel': '../bower_components/sass-bootstrap/js/carousel',
        'lib/bootstrap/collapse': '../bower_components/sass-bootstrap/js/collapse',
        'lib/bootstrap/dropdown': '../bower_components/sass-bootstrap/js/dropdown',
        'lib/bootstrap/modal': '../bower_components/sass-bootstrap/js/modal',
        'lib/bootstrap/popover': '../bower_components/sass-bootstrap/js/popover',
        'lib/bootstrap/scrollspy': '../bower_components/sass-bootstrap/js/scrollspy',
        'lib/bootstrap/tab': '../bower_components/sass-bootstrap/js/tab',
        'lib/bootstrap/tooltip': '../bower_components/sass-bootstrap/js/tooltip',
        'lib/bootstrap/transition': '../bower_components/sass-bootstrap/js/transition'
    },
    shim: {
        'lib/bootstrap/affix': {
            deps: ['lib/jquery']
        },
        'lib/bootstrap/alert': {
            deps: ['lib/jquery', 'lib/bootstrap/transition']
        },
        'lib/bootstrap/button': {
            deps: ['lib/jquery']
        },
        'lib/bootstrap/carousel': {
            deps: ['lib/jquery', 'lib/bootstrap/transition']
        },
        'lib/bootstrap/collapse': {
            deps: ['lib/jquery', 'lib/bootstrap/transition']
        },
        'lib/bootstrap/dropdown': {
            deps: ['lib/jquery']
        },
        'lib/bootstrap/modal':{
            deps: ['lib/jquery', 'lib/bootstrap/transition']
        },
        'lib/bootstrap/popover': {
            deps: ['lib/jquery', 'lib/bootstrap/tooltip']
        },
        'lib/bootstrap/scrollspy': {
            deps: ['lib/jquery']
        },
        'lib/bootstrap/tab': {
            deps: ['lib/jquery', 'lib/bootstrap/transition']
        },
        'lib/bootstrap/tooltip': {
            deps: ['lib/jquery', 'lib/bootstrap/transition']
        },
        'lib/bootstrap/transition': {
            deps: ['lib/jquery']
        }
    }
});
