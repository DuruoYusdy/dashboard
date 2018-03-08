/**
 * Created by OPS on 2017/9/25.
 */

    function  change(id) {
        var point =  document.getElementById(id);
        console.log(point);
        if(point.checked == true){
            var data = {
                "servername": id,
                "alarm_statu": "true"
            };
            console.log('checked');
            $.post('/api/alarmstatu',JSON.stringify(data))
        }else {
            var data = {
                "servername": id,
                "alarm_statu": "false"
            };
            console.log(id);
            console.log('unchecked');
            $.post('/api/alarmstatu',JSON.stringify(data))
        }
    }

    window.onload = loadAlarm();

    function loadAlarm() {
        var p = 1;
        $.get('/api/alarmstatu',
            function (data){
                for(var i in data){
                    if(data[i] == 'true'){
                        if(point = document.getElementById("b"+ i)) {
                            point.checked = true;
                        }
                    }else if(data[i] == 'false'){
                        if(point = document.getElementById("b"+ i)){
                            point.checked = false;
                        }
                    }else {
                        console.log('something wrong');
                    }
                    p++;

                }
            });
        $.get('/api/cx_activemq').done(update_mychart);
        $.get('/api/yc_activemq').done(update_mychart2);
        $.get('/api/ychcallback').done(update_mychart3);
    }