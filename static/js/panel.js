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
            command: command,
            token: TOKEN
        })
    }).done(function(data){
        if (data["result"]) {
            $("#command").val("");
            console_add("] " + command + "\n");
        } else {
            console.log("Couldn't send command! Reloading...");
            location.reload();
        }
    }).fail(function(jqXHR, textStatus){
        console.log("Couldn't send command! Reloading...");
        location.reload();
    });
}

$("document").ready(function(){

    $("#send").on("click", function(){
        send_command();
    });

    $(document).on('keypress', function(e) {
        if(e.which == 13) {
            send_command();
        }
    });

    let updateInterval = setInterval(function(){
        $.ajax({
            url: ajax_update_console_url,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                token: TOKEN
            })
        }).done(function(data){
            if (data["result"]) {
                if (data["text"]) {
                    console_add(data["text"]);
                    $("#console").scrollTop($("#console")[0].scrollHeight);
                }
            } else {
                console.log("Couldn't update console! Reloading...");
                location.reload();
            }
        }).fail(function(){
            console.log("Couldn't update console! Reloading...");
            location.reload()
        });
    }, 1000);

})