/**
 * Created by fander on 2017/1/17.
 */

$(function () {
    var down = 0;
    $('.toggle').click(function () {
        if(down == 0){
            $('#nav').slideDown("fast");
            down = 1;
        }else{
            $('#nav').slideUp("fast");
            down = 0;
        }
    });
});