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
})





