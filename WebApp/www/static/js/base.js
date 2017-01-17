/**
 * Created by fander on 2017/1/17.
 */



$(function () {
    
    $('.nav-collapse ul li').click(function () {
        
        $('.nav-collapse ul li').each(function () {
             $(this).removeClass('active');
        })
        $(this).addClass('active');
    })
})