$('body').on('click', '#feed_button', function(){
    if($(this).data('state') != 'disabled')
    {
        $(this).attr('data-state', 'disabled');
        $('.blackout_background').addClass('blackout');
    }
});
