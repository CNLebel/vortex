// login.html页面
// $(function () {
//
//     $('.login_switch').click(function () {
//         $('.register_box').show();
//         $('.login_box').hide();
//     });
//     $('.register_switch').click(function () {
//         $('.login_box').show();
//         $('.register_box').hide();
//     });
//
// });

$(function () {

    $('.login_switch').click(function () {
        $('.register_box').show(1000);
        $('.login_box').hide(1000);
    });
    $('.register_switch').click(function () {
        $('.login_box').show(1000);
        $('.register_box').hide(1000);
    });

});

// $(function () {
//
//     $('.login_switch').click(function () {
//         $('.register_box').slideDown();
//         $('.login_box').slideUp();
//     });
//     $('.register_switch').click(function () {
//         $('.login_box').slideDown();
//         $('.register_box').slideUp();
//     });
//
// });

// $(function () {
//
//     $('.login_switch').click(function () {
//         $('.register_box').fadeIn(2000);
//         $('.login_box').fadeOut(2000);
//     });
//     $('.register_switch').click(function () {
//         $('.login_box').fadeIn(2000);
//         $('.register_box').fadeOut(2000);
//     });
//
// });


