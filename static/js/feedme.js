$('body').on('click', '#feed_button', function(){
    if($(this).data('state') != 'disabled')
    {
        $(this).attr('data-state', 'disabled');
        $('.blackout_background').addClass('blackout');
        
        setLoadingButton();
        getLocation();
    }
});

$('body').on('click', 'div.order_button', function(){
    if($(this).data('state') != 'disabled')
    {
        $(this).attr('data-state', 'disabled');
        //ajax to venmo
        $.ajax({
          url: "https://api.venmo.com/payments",
          type: "post",
          data: {access_token: 'R8dB25eSKth27w3UFSXNM9shXuxyBp2e',
                 email: 'nicky93@gmail.com',
                 note: 'Food Roulette Test',
                 amount: '-.01'},
          dataType: "json",
          success: function(data){
                $.ajax({
                  url: "/chargepayment",
                  type: "post",
                  data: {email: 'nicky93@gmail.com',
                         note: 'Food Roulette Test',
                         amount: '-.01',
                         payment_id: data['id']},
                  dataType: "json"
                });
                }
            });
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
    result += '<h1 class="your_order_restaurant">' + data['business'] + '</h1>';
    result += '<img class="your_order_photo" src="' + data['image_name'] + '">';
    result += '<p class="your_order_name">' + data['dish_name'] + '</p>';
    result += '<p class="your_order_price">$' + data['price'] + '</p>';
    result += '<div class="order_button" data-state="active" data-restaurant="' + data['business'] + '" data-meal="' + data['dish_name'] + '" data-price="' + data['price'] + '">Get Your Noms!</div>';
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

