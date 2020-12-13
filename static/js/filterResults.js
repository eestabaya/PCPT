$(document).ready(function () {
    $("input:checkbox").on("change", function () {
        let a = $("input:checkbox:checked").val();
        if ($(this).prop("checked")) {
            $(".product:not(:contains(" + a + "))").hide();
        } else {
            $(".product").show();
        }
    });
});