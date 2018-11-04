
var results = [];
$(document).ready(function() {
           console.log("ready");
});
//
//function capture(e) {
//    console.log("form");
//    e.preventDefault();
//    $.ajax({
//        url:'/capture/1',
//        type:'post',
//        data:$('#capture_form').serialize(),
//        success:function(data){
//        console.log("receives");
//            $("#captured_image").attr('src', data);
//        },
//        error:function(){
//        console.log("error");
//            //whatever you wanna do after the form is successfully submitted
//        },
//    });
//});
 function addAllColumnHeaders(myList)
 {
     var columnSet = [];
     var headerTr$ = $('<tr/>');

     for (var i = 0 ; i < myList.length ; i++) {
         var rowHash = myList[i];
         for (var key in rowHash) {
             if ($.inArray(key, columnSet) == -1){
                 columnSet.push(key);
                 headerTr$.append($('<th/>').html(key));
             }
         }
     }
     $("#excelDataTable").append(headerTr$);

     return columnSet;
 }


function update_result_table(){
    if(results.length < 1)
        return;
     var columns = Object.keys(results[0]);

     for (var i = results.length -1 ; i < results.length ; i++) {
         var row$ = $('<tr/>');
         for (var col in columns) {
             value = results[i][columns[col]]
             var cellValue = value;

             if (cellValue == null) { cellValue = ""; }
             console.log(columns[col]);

             if (columns[col] == "image") {

                cellValue = "<img src='" + value +"' width='120px' height='auto'>";
                console.log(cellValue);
                 }

             row$.append($('<td/>').html(cellValue));
         }
         $("#result_table").append(row$);
     }
}

$(function() {
    $('#capture_button').on('click', function (e) {

    $('#capture_button').attr("disabled", "disabled");
    e.preventDefault();
    $.ajax({
        url:'/capture/1',
        type:'post',
        data:$('#capture_form').serialize(),
        success:function(data){
            console.log(data)
            $("#captured_image").attr('src', data.image);
             results.push(data)
        },
        error:function(){
            console.log("error");
            //whatever you wanna do after the form is successfully submitted
            },
        complete:function(){
            $('#capture_button').removeAttr("disabled");
            update_result_table();
        }
        });
    });
})