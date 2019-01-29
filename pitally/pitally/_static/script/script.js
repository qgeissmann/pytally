var results = [];
var session_time_str= "";
var $table = $('#table');


var resolutions = ["640x480 (VGA)",
                   "1640x1232",
                    "3280x2464"
];
var capture_res = "";


function image_formatter(value, row){
 //data-title="A random title"
//      data_options = {"caption" : "My caption", "type" : "iframe"};
//    return "<a data-fancybox='gallery' data-options='" + data_options + "' href='javascript:;' ><img class='img-fluid' width='50px' src= '" + value +"'><a>
//      console.log(row.filename);
      return "<a data-fancybox='gallery' data-caption='" + row.filename + "' href='" +
            value +"' ><img class='img-fluid' width='50px' src= '" + value +"'><a>";
}

var columns = [
            {field:"selected",
            checkbox:"true"},
            {
            field: 'image',
            title: 'Image',
            formatter: image_formatter
        }, {
            field: 'filename',
            title: 'Name',
            searchable: true
        }];

$table.bootstrapTable({
    columns: columns,
    data: results
});



$(function() {
    $('#capture_button').on('click', function (e) {
    $('.show_during_capture_only').show();
    $('.hide_during_capture_only').hide();
    $('.hide_during_capture_only').prop("disabled", true);

    $('#pitally_animation').attr("xlink:href", "static/svg/pitally_animation.svg");

    $('#capture_button').prop("disabled", true);

    e.preventDefault();
    var now = new Date();
    time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
    form = retrieve_form();

    $("#error > code").text("");
    $.ajax({
        url:'/capture/1',
        type:'post',
        data: form,
        success:function(data){
            var error = check_error(data);
            if(error == false){

                data.filename = data.prefix + "_" + time_str + ".jpg"
                data.selected = true;
                $("#captured_image").attr('xlink:href', data.image);
                results.push(data);
                localStorage.setItem("last_form",form) ;
                console.log(form);
                }
        },
        error:function(){
            console.log("error");
            //whatever you wanna do after the form is successfully submitted
            },
        complete:function(){
            $('#capture_button').removeAttr("disabled");
            $('#preview_toggle').removeAttr("disabled");

            $('.hide_during_capture_only').prop("disabled", false);
            $('.show_during_capture_only').hide();
            $('.hide_during_capture_only').show();

            $table.bootstrapTable('load', results);
            }
        });
    });
})


function preview(){

    form = retrieve_form();
    $.ajax({
        url:'/capture/1',
        type:'post',
        data:form,
        success:function(data){
        //todo replace by #preview_image
            console.log("preview")
            $("#preview_image").attr('xlink:href', data.image);
            var error = check_error(data);
            if($('#preview_toggle').prop("checked") == true){
                if(error ==false){
                    preview();
                    var now = new Date();
                    t = now.format("HH:MM:ss");
                    $("#preview_stamp").text("Preview at "+ t);

                }
                else{
                    stop_preview();
                }
            }
            },
        error:function(){
            console.log("error");
            },
        complete:function(){

            }
        });
}

function stop_preview(){
    console.log("reverting to saved res: "+ capture_res);
    $("#resolution_select").val(capture_res);
    $('.hide_during_preview_only').show();
    $('.show_during_preview_only').hide ();
    $('.hide_during_preview_only').prop('disabled', false);
}

$(function() {
    $('#preview_toggle').change(function (e) {
        console.log("preview toggled");
        if($(this).prop("checked") == true){
            $('.hide_during_preview_only').hide();
            $('.show_during_preview_only').show();
            $('.hide_during_preview_only').prop('disabled', true);
            capture_res = $("#resolution_select option:selected").text();
            console.log("saving old res: "+ capture_res);
            console.log("setting preview resolution: "+ resolutions[0]);

            $("#resolution_select").val(resolutions[0]);
            preview();
            }
        else{
        stop_preview();
        }
    })
});



$(function() {
    $('#download_button').on('click', function (e) {
        $('#download_button').attr("disabled", "disabled");
        var zip = new JSZip();
        var selected_rows = $table.bootstrapTable('getSelections');
        for(var i  =0; i < selected_rows.length; i++){
            var res = selected_rows[i];
            var base64String = res.image.replace("data:image/jpeg;base64,", "");
            zip.file(res.filename, base64String, {base64: true});
           }
        zip.generateAsync({type:"blob"}).then(function(content) {
                o = saveAs(content, "pitally_results_"+ session_time_str +".zip");
         });
         $('#download_button').removeAttr("disabled");
    });
})



$(function() {
    $('#delete_button').on('click', function (e) {;
        var selected_rows = $table.bootstrapTable('getSelections');
        var filenames = $.map($table.bootstrapTable('getSelections'), function (row) {
                return row.filename;
            });
            $table.bootstrapTable('remove', {
                field: 'filename',
                values: filenames
            });
        });
})

function populate_form(data) {
    var list = data.split("&");
    for(var i in list) {
        var s = list[i].split("=");
        $("[name=" + s[0] +"]").val(s[1]);
    }
    return 0;
}



$(document).ready(function() {
    var now = new Date();
    session_time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
    for (var i in resolutions){
        $("#resolution_select").append(
            "<option>" +resolutions[i] + "</option>"
        );
    }

    if (localStorage.last_form) {
    try{
        console.log("Loading previous form");
        var last_form = localStorage.getItem("last_form");
        populate_form(last_form);
        }
    catch(e){
        console.log(e);
        }

    }
    else{

        console.log("No previous form!");
        }

    capture_res = $("#resolution_select option:selected").text();
    $(".search").appendTo("#table_top");
    $(".show_during_capture_only").hide();
});

window.onbeforeunload = function() {
  return "Are you sure you want to navigate away?";
}
//
//$(document).on('click', '[data-toggle="lightbox"]', function(event) {
//                event.preventDefault();
//                $(this).ekkoLightbox();
//            });



$(function() {
    $('#restart_camera_button').on('click', function (e) {

    $.ajax({
        url:'/restart_camera',
        type:'post',
        data: {},
        success:function(data){
            $("#error > code").text("");

        },
        error:function(){
            console.log("error, did not restart the camera");
            },

        });
    });
})

$(function() {
    $('#restart_server_button').on('click', function (e) {

    $.ajax({
        url:'/stop_server',
        type:'post',
        data: {},
        success:function(data){
            $("#error > code").text("");

        },
        error:function(){
            console.log("error, did not restart the server");
            },

        });
    });
})





//////////////////////
