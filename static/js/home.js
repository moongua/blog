var start = 0;
var length = 50;

$(document).ready(function(){
    getArticleList(start, length);
    $(window).bind("scroll", function (event) {
        //滚动条到网页头部的 高度，兼容ie,ff,chrome
        var top = document.documentElement.scrollTop + document.body.scrollTop;
        //网页的高度
        var textheight = $(document).height();
        // 网页高度-top-当前窗口高度
        if (textheight - top - $(window).height() <= 100) {
            //可以根据实际情况，获取动态数据加载 到 div1中
            start += length;
            getArticleList(start, length)
        }
    });
});



function getArticleList(start, length) {
     $.ajax({
            type: 'post',
            url: '/article/api/get_article_list',
            data: JSON.stringify({
                start: start,
                length: length
            }),
            contentType: "application/json; charset=utf-8",
            "dataType" : "json",
            success: function(response) {
                if(response.status == 'OK') {
                    var template =
                            '<div>' +
                                '<div class="article" style="overflow: hidden;">' +
                                    '<div class="article-title">{{ title }}</div>' +
                                    '<div class="article-meta"><span>{{ author }}创建于{{ ctime }}</span><span>浏览{{ pv }}次</span></div>' +
                                    '<div class="article-content">{{ html }}</div>' +
                                    '<a class="view-" href="/article/detail/{{ id }}">阅读全文</a>' +
                                '</div>' +

                            '</div>';
                    response.data.map(function(e) {
                        if(e.pv == null || e.pv == undefined) {
                            e.pv = 0;
                        }
                        var articleInfo = template.replace(/\{\{ ctime \}\}/g, e.ctime)
                            .replace(/\{\{ title \}\}/g, e.title)
                            .replace(/\{\{ id \}\}/g, e.id)
                            .replace(/\{\{ pv \}\}/g, e.pv)
                            .replace(/\{\{ stat \}\}/g, e.stat == '1' ? '草稿':'')
                            .replace(/\{\{ author \}\}/g, e.author)
                            .replace(/\{\{ html \}\}/g, e.html)
                        $('.waterfall').append(articleInfo);
                    });
                }
                else {
                    notify.error(response.msg);
                }
            }
        });
}


