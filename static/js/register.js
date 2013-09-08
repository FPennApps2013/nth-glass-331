$('body').on('click', '.register_button', function(){
    $(this).closest('.black_box').addClass('slideup');
    if($(this).data('type') == 'customer')
    {
        $('div.add_form.customer').addClass('register');
    } else {
        $('div.add_form.business').addClass('register');
    }
});

        $( "#dietrestrictions" ).buttonset();

