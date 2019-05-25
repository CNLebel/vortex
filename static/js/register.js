
$(function () {

  // 验证正则
  var regPhone = /^1[34578]\d{9}$/;      //验证手机号格式正则
  var regUser = /^\w{3,16}$/;        //验证用户名格式正则
  var regPwd = /^[\w!@#$%^&*()]{4,16}$/;     //验证密码格式正则

  // 登录框对象
  var userName = $('#user_name');
  var password = $('#password');
  var userNameError = $('#username_error');
  var passwordError = $('#password_error');

  var idUsername = $('#id_username');
  var idMobile = $('#id_mobile');
  var idPassword1 = $('#id_password1');
  var idPassword2 = $('#id_password2');
  var registerUsernameError = $('#register_username_error');
  var registerMobileError = $('#register_mobile_error');
  var registerPassword1Error = $('#register_password1_error');
  var registerPassword2Error = $('#register_password2_error');


  userName.on('blur', function () {
    detect(regUser, $(this).val(), '请输入正确的用户名或手机号','请输入用户名或手机号',userNameError);
  });

  password.on('blur', function () {
     detect(regPwd, $(this).val(), '密码必须是4-16位字母数字或符号', '请输入密码', passwordError);
  });

  idUsername.on('blur', function () {
    detect(regUser, $(this).val(), '请输入正确的用户名或手机号','请输入用户名或手机号', registerUsernameError);
  });

  idMobile.on('blur', function () {
     detect(regPhone, $(this).val(), '用户名必须是有效的手机号', '请输入用户名', registerMobileError);
  });

  idPassword1.on('blur', function () {
      detect(regPwd, $(this).val(), '密码必须是4-16位字母数字或符号', '请输入密码', registerPassword1Error);
  });

  idPassword2.on('blur', function () {
      if($(this).val() != idPassword1.val()){
        registerPassword2Error.text('两次输入的密码必须一致').show();
      }else {
        registerPassword2Error.empty().hide();
      }
  });

  // 检测输入内容
  function detect(regexp,val,text,air,tip){
    if(val.trim() == ''){
      tip.text(air).show();
      return false;
    }else if(!regexp.test(val)){
      tip.text(text).show();
      return false;
    }else{
      tip.hide();
      return true;//user_login?userid=xxx&pwd=xx&remember_me=T
    }
  }

});


