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
    console.log(latitude, longitude); 
    
    $.ajax({
          url: "/locate",
          type: "post",
          data: {lat: latitude,
                 long: longitude},
          dataType: "json",
          success: function(data){
            showFood(data);
          }
    });
}

function showFood(data)
{
    if(data.length == 0)
    {
        return errorFood();
    }
    
    console.log(data);
    
    var result = '<div class="your_order">';
    result += '<h1 class="order_restaurant">' + data['business'] + '</h1>';
    result += '<img class="order_photo" src="' + data['image_name'] + '">';
    result += '<p class="order_name">' + data['dish_name'] + '</p>';
    result += '<p class="order_price">' + data['price'] + '</p>';
    result += '<div class="order_button" data-restaurant="' + data['business'] + '" data-meal="' + data['dish_name'] + '" data-price="' + data['price'] + '">Get Your Noms!</div>';
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

