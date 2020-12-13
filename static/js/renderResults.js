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

function stars(rate, prod) {
    switch (rate) {
        case "5":
            $('#' + prod + 'stars5').toggleClass('blue');
        case "4":
            $('#' + prod + 'stars4').toggleClass('blue');
        case "3":
            $('#' + prod + 'stars3').toggleClass('blue');
        case "2":
            $('#' + prod + 'stars2').toggleClass('blue');
        case "1":
            $('#' + prod + 'stars1').toggleClass('blue');
    }
}

/*
$(document).ready(function () {
    $('.products').show();

    $('.filter').find('input:checkbox').on('click', function() {
       let $prod = $('.product').hide();
       let $elem = $('.filter').find('input:checked');

       $prod
           .filter(function() {
               let $pr = $(this);
               return $elem.toArray().every(function(element) {
                   return $pr.hasClass($(element).attr('value'));
               });
           }).show();
    });
});*/