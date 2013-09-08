$('body').on('click', '.register_button', function(){
    $(this).closest('.black_box').addClass('slideup');
    if($(this).data('type') == 'customer')
    {
        $('div.add_form.customer').addClass('register');
    } else {
        $('div.add_form.business').addClass('register');
    }
});


$('body').on('click', '.accept', function(){
    $(this).html('Accepted');
    $(this).siblings('.deny').remove();
});


$('body').on('click', '.deny', function(){
    $(this).closest('menu_item').remove();
});


$( "#dietrestrictions" ).buttonset();

