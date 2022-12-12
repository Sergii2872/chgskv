// Скрипт всплывающих информационных окон
// Выпадающее инфо окно , выполняется по popup из scripts_reg.js где передается id="box1  boxN" для info.html
function popup(vidsob) {
    // выпадает окно при вызове функции popup из js скриптов
    $(vidsob).show(function(){
        $('#overlay').fadeIn('fast',function(){
            $(vidsob).animate({'top':'160px'},300);
        });
    });
     // Скрываем окно по клику
    $('.boxclose').click(function(){
        $(vidsob).animate({'top':'-200px'},300,function(){
            $('#overlay').fadeOut('fast');
        });
    });

    //	 Скрываем информационное окно по клавише Escape
    $(document).on('keyup', function(e) {
	    if ( e.key == "Escape" ) {
		    $(vidsob).animate({'top':'-200px'},300,function(){
            $('#overlay').fadeOut('fast');
            });
	    }
    });

};

/*  Код до оптимизации
// Окно регистрации пользователя
function popup1(vidsob) {
    $(vidsob).show(function(){
        $('#overlay1').fadeIn('fast',function(){
            $('#box1').animate({'top':'160px'},300);
        }) //.delay(5000);
    });
    $('#boxclose1').click(function(){
        $('#box1').animate({'top':'-200px'},300,function(){
            $('#overlay1').fadeOut('fast');
        });
    });
};
*/