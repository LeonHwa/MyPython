/**
 * Created by Leon.Hwa on 17/1/22.
 */function addPage(page_count,current_page) {
         for( i=1; i <= page_count;i++)
     {
       var pre = $('#pre');
       var li = document.createElement('li');
       var a = document.createElement("a");
       a.innerText = i.toString();

       li.appendChild(a);
       a.className += 'pageIndex';
         a.href = '/?page=' + i;
       if(i == current_page){
        li.className += ' ' +'active';
        a.style.cssText = "background: #000;";
       }
       var ul = document.getElementsByClassName("pagination")[0];
       var pre = document.getElementById("pre");
       ul.insertBefore(li,next)
     }
}

