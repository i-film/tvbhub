$(function(){
    var pathname = window.location.pathname;
    console.log(pathname);
    if(pathname.indexOf("users/profile/") >= 0 ) {
        $("#id_profile").addClass("active");
    }
    if(pathname.indexOf("users/change_password/") >= 0 ) {
        $("#id_password").addClass("active");
    }
});