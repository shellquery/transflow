require(['lib/RSA'], function(RSA) {
    $('#register-form').submit(function() {
        if($('#realname').val().trim().length <= 0) {
            return false;
        }
        if($('input:radio[name=gender]:checked').val() === undefined) {
            return false
        }
        var first_pwd = $('#first_password').val(),
            second_pwd = $('#second_password').val();
        if(!first_pwd || ! second_pwd) {
            return false;
        }
        if(first_pwd != second_pwd) {
            $('#second_password').parent().append('<p class="text-danger">密码不一致，请重新输入</p>');
            return false;
        } else {
            $('#second_password').siblings().remove();
        }
        var en = $('#public_key').val().split('-'),
            e = parseInt(en[0]).toString(16), n = en[1];
        var rsa = new RSA(e, "", n);
        var encrypted_pwd = rsa.encrypt(first_pwd);
        $('#password_encrypted').val(encrypted_pwd);
        return true;
    });
});
