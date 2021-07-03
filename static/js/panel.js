function console_add(text){
    let console = $("#console").val() + text;
    $("#console").val(console);
}

function send_command() {
    let command = $("#command").val();
    $.ajax({
        url: ajax_command_send_url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            command: command
        })
    }).done(function(data){
        if (data["result"]) {
            $("#command").val("");
            console_add("] " + command + "\n");
        }
    }).fail(function(jqXHR, textStatus){
        console.log("Fail to send command: " + textStatus);
    });
}

$("document").ready(function(){

    $("#send").on("click", function(){
        send_command()
    });

    $(document).on('keypress', function(e) {
        if(e.which == 13) {
            send_command()
        }
    });

    setInterval(function(){

        $.ajax({
            url: ajax_update_console_url,
            type: "GET"
        }).done(function(data){
            if (data["text"]) {
                console_add(data["text"]);
                $("#console").scrollTop($("#console")[0].scrollHeight);
            }
        }).fail(function(){
            console.log("Couldn't update console!");
        });

    }, 1000);
})