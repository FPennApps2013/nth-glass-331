$('body').on('click', '#feed_button', function(){
    if($(this).data('state') != 'disabled')
    {
        $(this).attr('data-state', 'disabled');
        $('.blackout_background').addClass('blackout');
        
        setLoadingButton();
        getLocation();
    }
});


function getLocation()
{
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(getFood);
    }
    else 
    {
        errorFood();
    }
}

function getFood(position)
{
    var latitude = position.coords.latitude; 
    var longitude = position.coords.longitude; 
    
    $.ajax({
          url: "/getFood",
          type: "POST",
          data: {latitude: latitude,
                 longitude: longitude},
          dataType: "json",
          success: showFood(data),
          error: errorFood();
    });
}

function showFood(data)
{
    var result = '<div class="your_order">';
    result += '<h1>' + data[0] + '</h1>';
    result += '<img class="order_photo" src="' + data[1] + '">';
    result += '<p class="order_name">' + data[2] + '</p>';
    result += '<p class="order_price">' + data[3] + '</p>';
    result += '<div class="order_button" data-restaurant="' + data[0] + '" data-meal="' + data[2] + '" data-price="' + data[3] + '">Get Your Noms!</div>';
    $('.pagewidth').append(result);
    slideResult();
}

function errorFood()
{
    slideResult();
}

function setLoadingButton()
{
    var loading_text = 'Loading';
    loading_text += '<img class="loading_gif" src="../static/media/ajax-loading.gif" />';
    $('#feed_button').html(loading_text);
}

function slideResult()
{
    $('#feed_button').addClass('slideup');
    $('div.your_order').addClass('show_me_the_food');
}
