/**
 * Created by OPS on 2017/9/6.
 */


$(function(){
    timestamp = 0;   //初始时间
    update();
});

/* flash the service's status */
function dosuccess(data){

    // $('i').addClass('animated rotateIn');
    //
    // setTimeout(function(){
    //     $('i').removeClass('animated rotateIn');
    // }, 10000);
    for( var o in data){
       if(data[o] == '1' ) {

           //改变颜色
           $("#"+ o).toggleClass("danger",false);
           $("#"+ o).toggleClass("warn",false);
           $("#"+ o).toggleClass("navy",true);

           //改变旋转

           $("#i" + o).toggleClass("mymove", true);
           $("#i" + o).css('color','snow')

       }
       else if(data[o] == '0'){

           //停止动画
           // $("#b"+ o).stop()
           //颜色改变
           $("#"+ o).toggleClass("navy",false);
           $("#"+ o).toggleClass("warn",false);
           $("#"+ o).toggleClass("danger",true);

           $("#i" + o).toggleClass("mymove", false);
       }
       // else if(data[o] == '3'){
       //
       //     //颜色改变
       //     $("#"+ o).toggleClass("navy",false);
       //     $("#"+ o).toggleClass("danger",false);
       //     $("#"+ o).toggleClass("warn",true);
       //
       //     $("#i" + o).toggleClass("mymove", false);
       //     $("#i" + o).css('color','#3a4459')
       //
       // }
    }

    function aniDiv() {
        $(".try").animate({width: 0, opacity: "1"}, 0);
        $(".try").animate({width: 700, opacity: "0.7"}, 2000);
        $(".try").animate({width: 1500, opacity: "0.3"}, 1000);
    }
    aniDiv();
}

/* ajax */
function update() {
    $.ajax({
        url:'/api/dashboard',
        type: "GET",
        dataType: "json",
        success: dosuccess,
        error:function (xhr,ajaxOptions,thrownError) {
            console.info(ajaxOptions);
            console.info(thrownError);
            statu = xhr.status;
        }
    });
    setTimeout('update()',10000)
}

/* time */
setInterval("jnkc.innerHTML=new Date().toLocaleString()+' 星期'+'日一二三四五六'.charAt(new Date().getDay());",1000);
