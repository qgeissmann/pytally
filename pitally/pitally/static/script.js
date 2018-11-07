var preview_w = 640;
var preview_h = 480;

var capture_w = 640;
var capture_h = 480;

var results = [];
var session_time_str= "";
var $table = $('#table');

function image_formatter(value){
      return "<img width='50px' src= '" + value +"'>";
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
            title: 'Name'
        }];

$table.bootstrapTable({
    columns: columns,
    data: results
});



$(function() {
    $('#capture_button').on('click', function (e) {

    $('#capture_button').attr("disabled", "disabled");
    $('.show_during_capture').show();
    $('.hide_during_capture').hide();
    $('#preview_toggle').attr("disabled", "disabled");

    e.preventDefault();
    var now = new Date();
    time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
    console.log(time_str);
    var form = $('#capture_form').serialize()
    $('input[disabled]').each( function() {
      form = form + '&' + $(this).attr('name') + '=' + $(this).val();
    });

    $.ajax({
        url:'/capture/1',
        type:'post',
        data: form,
        success:function(data){
            data.filename = data.prefix + "_" + time_str + ".jpg"
            data.selected = true;
            $("#captured_image").attr('xlink:href', data.image);
            results.push(data);
            localStorage.setItem("last_form",form) ;
        },
        error:function(){
            console.log("error");
            //whatever you wanna do after the form is successfully submitted
            },
        complete:function(){
            $('#capture_button').removeAttr("disabled");
            $('#preview_toggle').removeAttr("disabled");

            $('.show_during_capture').hide();
            $('.hide_during_capture').show();

            $table.bootstrapTable('load', results);
            }
        });
    });
})

function preview(){

    $.ajax({
        url:'/capture/1',
        type:'post',
        data:$('#capture_form').serialize(),
        success:function(data){
        //todo replace by #preview_image
            console.log("preview")
            $("#preview_image").attr('xlink:href', data.image);
            if($('#preview_toggle').prop("checked") == true){
                preview();
            }
            },
        error:function(){
            console.log("error");
            //whatever you wanna do after the form is successfully submitted
            },
        complete:function(){
            }
        });

}

$(function() {
    $('#preview_toggle').change(function (e) {
    if($(this).prop("checked") == true){
        $('#captured_image').hide();
        $('#preview_image').show();
        $('#table_div').hide();

        capture_w = $('#w_input').val();
        capture_h = $('#h_input').val();

        $('#h_input').val(preview_h);
        $('#w_input').val(preview_w);
        $('.non_preview_input').attr('readonly', true);
        $('#capture_button').attr("disabled", true);
        preview();
        }
    else{
        $('.non_preview_input').removeAttr("readonly");
        $('#capture_button').removeAttr("disabled");

        $('#captured_image').show();
        $('#preview_image').hide();
        $('#table_div').show();

        $('#h_input').val(capture_h);
        $('#w_input').val(capture_w);

  }
});


//        console.log("toggle off");
//    });
})



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

function populate(frm, data) {
    $.each(data, function(key, value) {
        var ctrl = $('[name='+key+']', frm);
        switch(ctrl.prop("type")) {
            case "radio": case "checkbox":
                ctrl.each(function() {
                    if($(this).attr('value') == value) $(this).attr("checked",value);
                });
                break;
            default:
                ctrl.val(value);
        }
    });
}


$(document).ready(function() {

    var now = new Date();
    session_time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");

    console.log(localStorage.getItem("last_form"));
    if (localStorage.results) {
    try{
        var last_form = JSON.parse(localStorage.getItem("last_form"));
        console.log(last_form);
        populate(capture_form, last_form);
        }
    catch(e){
        console.log(e);
        }
}

});

window.onbeforeunload = function() {
  return "Are you sure you want to navigate away?";
}