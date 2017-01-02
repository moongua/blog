var mode = '';
var editor;
$(document).ready(function(){
    if(article_id) {
        mode = 'update_article';
        $.ajax({
            type: 'post',
            url: '/article/api/get_article',
            data: JSON.stringify({
                article_id: article_id
            }),
            contentType: "application/json; charset=utf-8",
            "dataType" : "json",
            success: function(response) {
                if(response.status == 'OK') {
                    $('#title-input').val(response.article.title);
                    editor = initEditor(response.article.content);
                }
                else if(response.status == 'BIZ_ERROR')  {
                    notify.bizError(response.msg);
                } else {
                    notify.error(response.msg);
                }
            }
        });
    } else {
        mode = 'add_article';
        editor = initEditor('');
    }

    $('.save-edit-btn').click(function () {
        submitEditor('1');  //草稿状态，不可见
    });
    $('.submit-edit-btn').click(function () {
        submitEditor('0');
    });
});

function submitEditor(stat) {
    $.ajax({
            type: 'post',
            url: '/article/api/' + mode,
            data: JSON.stringify({
                article_id: article_id,
                content: editor.getMarkdown(),
                title: $('#title-input').val(),
                // html: editor.getHTML(),
                html: editor.getPreviewedHTML(),
                stat: stat
            }),
            contentType: "application/json; charset=utf-8",
            "dataType" : "json",
            success: function(response) {
                if(response.status == 'OK') {
                    window.location.href = '/article/detail/' + response.data;
                }
                else if(response.status == 'BIZ_ERROR')  {
                    notify.bizError(response.msg);
                } else {
                    notify.error(response.msg);
                }
            }
        });
}


function initEditor(md) {
    if(!md) {
        md = '';
    }
    testEditor = editormd("editor", {
        width   : "90%",
        height  : '640px',
        syncScrolling : "single",
        saveHTMLToTextarea: true,
        path    : "/static/js/lib/editor.md/lib/",
        onload: function() {
            this.setMarkdown(md);

        }
    });
    return testEditor;
}
