$(document).ready(function () {
    $.ajax({
        url: "/api/mongo",
        method: 'GET',
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("#csrf-token").val());
        },
        dataType: "json",
        contentType: "application/json;charset=utf-8",

        success: function (data) {
            let success = data.success;

            if (success) {
                let items = data["items"]

                const _something = $("#something")
                items.forEach(function(item){
                    _something.append("<b>" + item["_id"] + "</b><br />")
                })
            }

        }

    });
})