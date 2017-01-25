/**
 * Created by Leon.Hwa on 17/1/24.
 */
function addPage(page_count,current_page) {
         for( i=1; i <= page_count;i++)
     {
       var pre = $('#pre');
       var li = document.createElement('li');
       var a = document.createElement("a");
       a.innerText = i.toString();

       li.appendChild(a);
       a.className += 'pageIndex';
         a.href = '/archives/?page=' + i;
       if(i == current_page){
        li.className += ' ' +'active';
        a.style.cssText = "background: #000;";
       }
       var ul = document.getElementsByClassName("pagination")[0];
       var pre = document.getElementById("pre");
       ul.insertBefore(li,next)
     }
}

function init() {
     $('.nav-collapse ul li').each(function () {
            $(this).removeClass('active');
            $('.circle').remove();
        });
     $('#nav ul li').eq(1).addClass('active');
      addCircle('active');
     // $('.list').hover(function () {
     //    $(this).css("background","red");
     // });
}
 function addCircle (name) {
      var act = document.getElementsByClassName(name)[0];
      var para = document.createElement("div");
      para.style.cssText = "border-radius: 50%; width: 6px;height: 6px; background: #c8c8c8;  display: inline-block; ";
      para.className = "circle";
      act.appendChild(para);
    }
