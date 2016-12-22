/**
 * Created by user on 22.12.2016.
 */
var currentState = '';

function ajaxLoadUsers(state){

    $.ajax({
        url: location.href,
        type: 'POST',
        data: {state : state},
        dataType: 'text',
        timeout: 60000,
        success: function(response){

             // console.log('response***' + response + '****');
            $('#list_of_users').html(response);

            if (currentState == 'True') {
                $('#bt_load_users').text('Не приду');
            }else{
                $('#bt_load_users').text('Приду');
            }

        },
        error: function(){
            alert('Упс... Что то пошло не так, обновите страницу и повторите попытку.');
            if (currentState == 'True') {
                currentState = 'False';
            }else{
                currentState = 'True';
            }
        }
    });
}

$('#bt_load_users').click(function(){
    if (currentState == 'True') {
        currentState = 'False';
    }else{
        currentState = 'True';
    }

    ajaxLoadUsers(currentState);
})

$(document).ready(function () {
    // текущий статус
    currentState = $('#list_of_users').attr('user_state');

    console.log(currentState);

    // юзвери
    ajaxLoadUsers(currentState);
})

