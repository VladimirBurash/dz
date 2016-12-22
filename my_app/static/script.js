
var infinityList = {};
infinityList.updateGeneral = function(){
    var obj = this;
    obj.pageHeight = parseInt($(document).height());
    obj.winHeight = parseInt($(window).height());
}
infinityList.init = function(){

    var obj = this;
    obj.container = $('#containers_block');

    obj.updateGeneral();

    obj.scrollIndex = 0;
    obj.eror_lock = false;
    obj.load_lock = false;
    obj.end_of_list  = false;

    obj.check_point = 100;

    // ловим событие скрола
    $(document).scroll(function () {
        var pos = parseInt($(document).scrollTop());

        if ((pos + obj.winHeight >= obj.pageHeight - obj.check_point) &&
            (!obj.load_lock) &&
            (!obj.end_of_list))
        {
            obj.scrollIndex++;
            obj.load_lock = true;
            $.ajax({
                url: '/ajax_list/' + obj.scrollIndex,
                type: 'GET',
                data: {},
                dataType: 'text',
                timeout: 60000,
                success: function(response){
                    if (response.trim() == 'N/A') {
                        obj.end_of_list = true;
                    }else{
                        obj.container.append(response);
                    }

                    obj.updateGeneral();
                    obj.load_lock = false;
                },
                error: function(){
                    if (!obj.eror_lock) {
                        obj.scrollIndex--;
                        obj.eror_lock = true;
                        $(document).scrollTop(0);
                        alert('Упс... Что то пошло не так, обновите страницу и повторите попытку.');
                        setTimeout(function() {
                            location.reload();
                        }, 5);
                    }
                }
            });
        }
    });

    // ресайз
    $(window).resize(function () {
        obj.updateGeneral();
    });
}
$(document).ready(function () {
    infinityList.init();
})