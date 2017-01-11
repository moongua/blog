$(document).ready(function() {
    $('.decode-btn').click(function() {
        $.ajax({
            type: 'post',
            url: '/api/tool/url_decode',
            data: JSON.stringify({
                input: $('#input-textarea').val()
            }),
            contentType: "application/json; charset=utf-8",
            "dataType" : "json",
            success: function(response) {
                if(response.status == 'OK') {
                    $('#output-textarea').val(response.data);
                }
                else if(response.status == 'BIZ_ERROR')  {
                    notify.bizError(response.msg);
                } else {
                    notify.error(response.msg);
                }
            }
        });
    });

    $('.encode-btn').click(function() {
        $.ajax({
            type: 'post',
            url: '/api/tool/url_encode',
            data: JSON.stringify({
                input: $('#input-textarea').val()
            }),
            contentType: "application/json; charset=utf-8",
            "dataType" : "json",
            success: function(response) {
                if(response.status == 'OK') {
                    $('#output-textarea').val(response.data);
                }
                else if(response.status == 'BIZ_ERROR')  {
                    notify.bizError(response.msg);
                } else {
                    notify.error(response.msg);
                }
            }
        });
    });
});