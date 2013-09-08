$('body').on('click', '#feed_button', function(){
    if($(this).data('state') != 'disabled')
    {
        $(this).attr('data-state', 'disabled');
        $('.blackout_background').addClass('blackout');
        
        setLoadingButton();
        getLocation();
    }
});

$(document).ready(function () {

    //set the background image
    var bg_images = [
        "http://farm4.staticflickr.com/3362/4593964455_89a56d91e9.jpg", //pizza
        "http://farm2.staticflickr.com/1410/543330359_ddc3295035.jpg", //taco
//        "http://farm1.staticflickr.com/62/155903230_afbc19f646.jpg", //cookie
        "http://farm4.staticflickr.com/3524/3902076445_7a2213f6ae.jpg", //gyro 
        "http://farm1.staticflickr.com/228/478715579_ebe8db8d25.jpg" //hamburger
    ];

    var rand_index = Math.floor((Math.random()*bg_images.length));
    var new_bg = 'url('+bg_images[rand_index]+') no-repeat center center fixed';
    $(".background_photos").css({
        'background': new_bg,
        '-webkit-background-size': 'cover',
        'moz-background-size': 'cover',
        '-o-background-size': 'cover', 
        'background-size': 'cover' 
    });
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

