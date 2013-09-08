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
          success: function(data){
            showFood(data);
          },
          error: errorFood(),
    });
}

function showFood(data)
{
    if(data.length == 0)
    {
        return errorFood();
    }
    
    var result = '<div class="your_order">';
    result += '<h1 class="order_restaurant">' + data[0] + '</h1>';
    result += '<img class="order_photo" src="' + data[1] + '">';
    result += '<p class="order_name">' + data[2] + '</p>';
    result += '<p class="order_price">' + data[3] + '</p>';
    result += '<div class="order_button" data-restaurant="' + data[0] + '" data-meal="' + data[2] + '" data-price="' + data[3] + '">Get Your Noms!</div>';
    result += '</div>';
    $('.page_wrapper').append(result);
    
    $('#feed_button').addClass('slideup');
    $('div.your_order').addClass('show_me_the_food');
}

function errorFood()
{
    var result = '<div class="your_order">';
    result += '<h1 class="order_restaurant">Sorry, there was an error generating your order.</h1>';
    result += '</div>';
    $('.page_wrapper').append(result);
    
    $('#feed_button').addClass('slideup');
    $('div.your_order').addClass('show_me_the_food');
}

function setLoadingButton()
{
    var loading_text = 'Loading...';
    $('#feed_button').html(loading_text);
}

