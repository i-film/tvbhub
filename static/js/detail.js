$(function () {

    // 写入csrf
    $.getScript("/static/js/csrftoken.js");

    // 点赞
    $("#like").click(function(){
      var video_id = $("#like").attr("video-id");
      $.ajax({
            url: '/videos/like/',
            data: {
                video_id: video_id,
                'csrf_token': csrftoken
            },
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                var code = data.code
                if(code == 0){
                    var likes = data.likes
                    var user_liked = data.user_liked
                    $('#like-count').text(likes)
                    if(user_liked == 0){
                        $('#like').removeClass("grey").addClass("red")
                    }else{
                        $('#like').removeClass("red").addClass("grey")
                    }
                }else{
                    var msg = data.msg
                    alert(msg)
                }

            },
            error: function(data){
              alert("点赞失败")
            }
        });
    });

    // 提交评论
    var frm = $('#comment_form')
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            dataType:'json',
            data: frm.serialize(),
            success: function (data) {
                var code = data.code
                var msg = data.msg
                if(code == 0){
                    $('#id_content').val("")
                    $('.comment-list').prepend(data.html);
                    $('#comment-result').text("评论成功")
                    $('.info').show().delay(2000).fadeOut(800)
                }else{
                    $('#comment-result').text(msg)
                    $('.info').show().delay(2000).fadeOut(800);
                }
            },
            error: function(data) {
            }
        });
        return false;
    });

})





