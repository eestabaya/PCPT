

$(document).ready(function () {
    $('.product').show();

    $('.filter').find('input:checkbox').on('click', function() {
       let $prod = $('.product').hide();
       let $elem = $('.filter').find('input:checked');

       $prod
           .filter(function() {
               let $pr = $(this);
               return $elem.toArray().every(function(element) {
                   return $pr.hasClass($(element).attr('id'));
               });
           }).show();
    });
});