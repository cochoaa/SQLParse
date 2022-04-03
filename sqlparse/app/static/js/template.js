jQuery["postJSON"] = function( url, data, callback ) {
    // shift arguments if data argument was omitted
    if ( jQuery.isFunction( data ) ) {
        callback = data;
        data = undefined;
    }
    return jQuery.ajax({
        url: url,
        type: "POST",
        contentType:"application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(data),
        success: callback
    });
};

$("#button_converter" ).click(function() {
    let string_stataments_input=$("#queries_input").val()
    data_input={ querys_input: string_stataments_input}
    var posting =$.postJSON("/api/converter",data_input,
    function( data_output ) {
        let string_stataments_output=data_output.queries_output.join("\n");
        $("#queries_output").val(string_stataments_output);
    })

//    posting.done(function( data_output ) {
//        console.log(data_output)
//    });
});