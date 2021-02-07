const player = new Plyr('#player');

$(document).ready(function(){
    $('.pointer').mask('000;000');
    $('.number').mask('0.0');

    $('input[name="end_time"]').mask('AZ:AZ', {
        translation: {
          'A': {
            pattern:  /[0-5]/, 
            optional: true
          },
          'Z': {
            pattern:  /[0-9]/, 
            optional: true
          }
        }
    });

    $('input[name="start_time"]').mask('AZ:AZ', {
        translation: {
          'A': {
            pattern:  /[0-5]/, 
            optional: true
          },
          'Z': {
            pattern:  /[0-9]/, 
            optional: true
          }
        }
    });
});

$("form").submit(function (event) {
    event.preventDefault();
     
    var comments = {}
    var form = $(this);
    var c_data = $(this).serializeArray().reduce(function (obj, item) {
        if (item.name == 'c_d1d2' || item.name == 'c_d3d4' || item.name == 'c_e1e2' || item.name == 'c_e3e6') {
            comments[item.name] = item.value
        } else {
            obj[item.name] = item.value;
        }
        return obj;
    }, {});
    c_data['comments'] = comments

    $.ajax({
        url: '/api/v1/rate_element/',
        data: JSON.stringify(c_data),
        method: 'POST',
        dataType: "json",
        statusCode: {
            500: function (e) {
                form.find('.alerts').html(
                    '<div class="alert alert-danger text-center" role="alert">Ошибка сервера</div>'
                )
                setTimeout(() => form.find('.alerts').html(""), 1500);
            },
            400: function (e) {
                form.find('.alerts').html(
                    '<div class="alert alert-danger text-center" role="alert">' + e.responseText + '</div>'
                )
                setTimeout(() => form.find('.alerts').html(""), 1500);
            },
            201: function (e) {
                form.find('.alerts').html(
                    '<div class="alert alert-success text-center" role="alert">Элемент успешно оценен</div>'
                )
                setTimeout(() => form.find('.alerts').html(""), 1500);
            }
        }
    });

});

$("#send_notif").on( "click", function() {
    var video_id = $("#send_notif").attr('video_id');
    $.ajax({
        url: '/api/v1/send_notification/',
        data: {'video_id': video_id},
        method: 'POST',
        dataType: "json",
        statusCode: {
            500: function (e) {
                $('.notif-a').html(
                    '<div class="alert alert-danger text-center" role="alert">Ошибка сервера</div>'
                )
                setTimeout(() => $('.notif-a').html(""), 1500);
            },
            400: function (e) {
                $('.notif-a').html(
                    '<div class="alert alert-danger text-center" role="alert">' + e.responseText + '</div>'
                )
                setTimeout(() => $('.notif-a').html(""), 1500);
            },
            200: function (e) {
                $('.notif-a').html(
                    '<div class="alert alert-success text-center" role="alert">Уведомление отправлено</div>'
                )
                setTimeout(() => $('.notif-a').html(""), 1500);
            }
        }
    });
});