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
        if(!first_pwd) {
            return false;
        }
        if(first_pwd != second_pwd) {
            $('#second_password').parent().append('<p class="text-danger">密码不一致，请重新输入</p>');
            return false;
        }
        var rsa = RSA("", "", $('#public_key'));
        var encrypted_pwd = rsa.encrypt(first_pwd);
        console.log(encrypted_pwd);
        return false;
    });
});
