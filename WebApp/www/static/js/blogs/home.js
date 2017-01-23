/**
 * Created by Leon.Hwa on 17/1/22.
 */

function addPage(page) {
         for( i=1; i <= page.page_count;i++)
     {
       var pre = $('#pre');
       var li = document.createElement('li');
       var span = document.createElement("span");
       span.innerText = i.toString();
       li.appendChild(span);
       span.className += 'pageIndex';
       if(i == this.page.current_page){
        li.className += ' ' +'active';
       }
       var ul = document.getElementsByClassName("pagination")[0];
       var pre = document.getElementById("pre");
       ul.insertBefore(li,next)
     }
}