$("document").ready(function(){

    $("#login").on("click", function(){

        $.ajax({
            url: login_ajax_url,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                username: $("#username").val(),
                password: $("#password").val()
            })
        }).done(function(data){
            if (data["result"]) {
                location.href = panel_url;
            } else {
                console.log(data["message"])
            }
        });

    });

})