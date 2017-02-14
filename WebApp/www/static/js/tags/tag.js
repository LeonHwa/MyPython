/**
 * Created by Leon.Hwa on 17/2/14.
 */
function init() {
     $('.nav-collapse ul li').each(function () {
            $(this).removeClass('active');
            $('.circle').remove();
        });
     $('#nav ul li').eq(2).addClass('active');
      addCircle('active');
     // $('.list').hover(function () {
     //    $(this).css("background","red");
     // });
}