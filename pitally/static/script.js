var results = [];
if (localStorage.results) {
try{
    results = JSON.parse(localStorage.getItem("results"));
    }
    catch(e){
    console.log(e);
    results =[];
    }
    }
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
    e.preventDefault();
    var now = new Date();
    time_str = now.format("yyyy-mm-dd'T'HH:MM:ss");
    console.log(time_str);

    $.ajax({
        url:'/capture/1',
        type:'post',
        data:$('#capture_form').serialize(),
        success:function(data){
            data.filename = data.prefix + "_" + time_str + ".jpg"
            data.selected = true;
            $("#captured_image").attr('src', data.image);
             results.push(data);
        },
        error:function(){
            console.log("error");
            //whatever you wanna do after the form is successfully submitted
            },
        complete:function(){
            $('#capture_button').removeAttr("disabled");
            $table.bootstrapTable('load', results);
            localStorage.setItem("results",JSON.stringify(results));
            }
        });
    });
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
                o = saveAs(content, "ZipFileName.zip");
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

$(document).ready(function() {
           console.log("ready");
});

window.onbeforeunload = function() {
  return "Are you sure you want to navigate away?";
}