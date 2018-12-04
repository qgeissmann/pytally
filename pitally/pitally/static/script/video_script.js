

function video_preview(){

    //form = retrieve_form();
    form = "";
    $.ajax({
        url:'/video_preview',
        type:'post',
        data:form,
        success:function(data){
        //todo replace by #preview_image
            console.log("video_preview")
            $("#video_preview_image").attr('xlink:href', data.image);
            var error = check_error(data);
            if(error ==false){
                var now = new Date();
                t = now.format("HH:MM:ss");
                $("#preview_stamp").text("Preview at "+ t);
            }
            },
        error:function(){
            console.log("error");
            },
        complete:function(){

            }
        });
}





$(function() {
    $('#record_button').on('click', function (e) {
    e.preventDefault();
    var form = $('#recording_form').serialize();
    console.log(form);
     $.ajax({
        url:'/start_video',
        type:'post',
        data: form,
        success:function(data){
                var error = check_error(data);
            if(error == false){

                }
        },
        error:function(){
            console.log("error");
            //whatever you wanna do after the form is successfully submitted
            },
        complete:function(){
            }
        });
    });
})




$(document).ready(function() {
    var now = new Date();
    session_time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
     setInterval(video_preview, 1000);
});
