
function parse_resolution(res){
    var regex = /^(\d+)x(\d+).*$/;
    var match = regex.exec(res);
    return  {w:match[1], h:match[2]};
}

function retrieve_form(){
    var form = $('#capture_form').serialize();
    $('input[disabled]').each( function() {
      form = form + '&' + $(this).attr('name') + '=' + $(this).val();
    });
    var resolution_txt = $("#resolution_select option:selected").text();
    resolution = parse_resolution(resolution_txt);
    resolution["resolution"] = resolution_txt
    for (var key in resolution) {
        form = form + '&' + key + '=' + resolution[key];
    }
    return form;

}

function check_error(data){
    if('error' in data){
        $("#error").show();
        $("#error > code").text("ERROR:\n\n" + data.error);
        console.log("capture error")
        return true;
    }

    $("#error").hide();
    return false;
}