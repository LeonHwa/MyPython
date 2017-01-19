/**
 * Created by fander on 2017/1/17.
 */



$(function () {
    function addCircle (name) {
      var act = document.getElementsByClassName(name)[0];
      var para = document.createElement("div");
      para.style.cssText = "border-radius: 50%; width: 6px;height: 6px; background: #c8c8c8;  display: inline-block; ";
      para.className = "circle";
      act.appendChild(para);
    }
    addCircle('active');
    $('.nav-collapse ul li').click(function () {
        $('.circle').remove();
        $('.nav-collapse ul li').each(function () {
            $(this).removeClass('active');
        })
        $(this).addClass('active');
         addCircle('active');
    })
})