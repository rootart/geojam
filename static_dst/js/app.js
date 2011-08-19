$(window).load(function(){

     $('form').submit(function(){
         var _this = $(this);
         var form_data = _this.serialize();
         $.post(
             '/checkin/',
             form_data,
             function(){
             });
             $('textarea').val('');
             return false;
     });

       var flow = $('.messages');
       var socket = new io.Socket(window.location.hostname, {
           port: 8001,
           rememberTransport: false
       });

       socket.addEvent('connect', function(e){
           flow.prepend("<div class=\"msg not-display\" data-lonlat=\"10.00000 100.0000\"> Connecting... </div>");
              $('.not-display').fadeIn('slow');
           socket.send({
               id: Math.floor(Math.random(1000) * 1000)
           });
       });

       socket.connect();
       socket.addEvent('message', function(data) {
           var data = Object(data);
           $('.selected').removeClass('selected');
           flow.prepend("<div class=\"msg\" data-lonlat=\"10.00000 100.0000\">"+data.data + "<a href=\"#\" class=\"twit\"><img src=\"http://cdn1.iconfinder.com/data/icons/social/16/picons03.png\"></a>"+"</div>");
           $('.not-display').fadeIn('slow');
       });



    $('.msg').hover(
        function(){
            $(this).addClass('selected');
        },
        function(){
            $(this).removeClass('selected');
       }
    );
    
    $('#locate').toggle(
        function(){
        $('.info').show();
        $('.messages').css('top', '90px');
    },
        function(){
       $('.info').hide();
       $('.messages').css('top', '60px');
   }
    );

    $('.show-form-box').toggle(
        function(){
        $('.form-box').show();
        $('.messages').css('top', '160px');
    },
        function(){
       $('.form-box').hide();
       $('.messages').css('top', '60px');
   }
    );

    $('.twit').each(function(){
        var text = $(this).parent().attr('data-msg');
        $(this).attr('href', "https://twitter.com/intent/tweet?text="+text+"+checkin from geojam %23itjam");
    });

});