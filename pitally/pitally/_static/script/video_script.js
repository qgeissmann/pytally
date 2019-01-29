

var resolutions = ["640x480 (VGA)",
                   "1640x1232",
                    "3280x2464"
];
var capture_res = "";


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

            var error = check_error(data);

            if(error ==false & !jQuery.isEmptyObject(data)){

                $("#video_preview_image").attr('xlink:href', data.image);

                $("#video_name").text(data.video_name);
                var now = new Date();
                t = now.format("HH:MM:ss");
                $("#video_preview_stamp").text("Preview at "+ t);
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

    var now = new Date();
    //time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
    time_str = now.getTime().toString();
    var form = retrieve_form("#recording_form");
    form = form + "&time=" + time_str
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






$(function() {
    $('#stop_recording_button').on('click', function (e) {
    e.preventDefault();



     $.ajax({
        url:'/stop_video',
        type:'post',
        data: "",
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
    for (var i in resolutions){
        $("#resolution_select").append(
            "<option>" +resolutions[i] + "</option>"
        );
    }
    session_time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
    setInterval(video_preview, 1000);
});
