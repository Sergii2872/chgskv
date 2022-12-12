/* формы аутентификации и регистрации пользователя вызываются из navbarreg.html , стили форм в style.css, содержание в form_vh_reg.html*/
$(document).ready(function(){  /* Стандартная обертка, т.е. скрипт выполняется когда загрузится весь html документ */
  var vreg = 0; /* флаг 1 - аутентификация пользователя, 2 - регистрация нового пользователя */
  $('#nav-bar').fadeIn();
  $('#Log-in').click(function() {
    $('#Log-in').css('background-color', '#7CA5DA'); /* Цвета меню вход,регистрация*/
    $('#signUp').css('background-color', '#E2E7E4');
    $('#submit').hide().css({
      'left': '0px'
    });
    $('#SignupForm').hide().css({
      'top': '0px'
    });
    $('#login').show().animate({
      left: '52%',
    }, 400, function() {
      $('#login').css({
        '-webkit-transform': 'rotate(-0deg)',
        '-moz-transform': 'rotate(-0deg)'
      });
    });
    ///
    $('#Login_form').show().animate({
      top: '30px', // Отступ формы от верха
    }, 700, function() {
      //$('#image').css({'-webkit-transform' : 'rotate(-90deg)','-moz-transform' : 'rotate(-90deg)' });
    });
    return false;
  });

  $('#signUp').click(function() {
    $('#signUp').css('background-color', '#7CA5DA');
    $('#Log-in').css('background-color', '#E2E7E4');
    $('#login').hide().css({
      'left': '0px'
    });
    $('#Login_form').hide().css({
      'top': '0px'
    });
    $('#submit').show().animate({
      left: '52%',
    }, 400, function() {
      $('#submit').css({
        '-webkit-transform': 'rotate(-0deg)',
        '-moz-transform': 'rotate(-0deg)'
      });
    });
    ///
    $('#SignupForm').show().animate({
      top: '30px', // Отступ формы от верха
    }, 700, function() {
      //$('#image').css({'-webkit-transform' : 'rotate(-90deg)','-moz-transform' : 'rotate(-90deg)' });
    });
    return false;
  });

// Скрываем форму авторизации и регистрации по клику вне ее (не использую)
// https://misha.agency/javascript/klik-vne-elementa.html

jQuery(function($){
/*	$(document).mouseup( function(e){ // событие клика по веб-документу
		var div = $( "#Login_form" ); // тут указываем ID элемента
		var div1 = $( "#SignupForm" ); // тут указываем ID элемента
		if ( !div.is(e.target) // если клик был не по нашему блоку
		    && div.has(e.target).length === 0 ) { // и не по его дочерним элементам
			div.hide(); // скрываем его
		}
		if ( !div1.is(e.target) // если клик был не по нашему блоку
		    && div1.has(e.target).length === 0 ) { // и не по его дочерним элементам
			div1.hide(); // скрываем его
		}
	});*/

//	 Скрываем форму авторизации и регистрации по клавише Escape
//   https://misha.agency/javascript/klik-vne-elementa.html
    $(document).on('keyup', function(e) {
	    if ( e.key == "Escape" ) {
		    $( "#Login_form" ).hide();
		    $( "#SignupForm" ).hide();
	}
    });

});


// Скрываем форму регистрации по клику вне ее, старая версия закрывался даже на форме
//jQuery(document).click( function(event){
//	if( $(event.target).closest(".loginform").length )
//	return;
//	jQuery(".loginform").fadeOut("slow");
//	event.stopPropagation();
//	$('#Log-in').css('background-color', '#E2E7E4');
//	$('#signUp').css('background-color', '#E2E7E4');
//});



     // Функция входа, проверки , обработки форм
     function userVhod(e){
         /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
     элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        var form = $('#form_authentication'); /* Принимаем форму(form) по id=form_authentication из form_vh_reg.html*/
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('#form_authentication [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        var reg_login = $('#edit-name').val(); /* Передаем login пользователя */
        console.log(reg_login);
        var reg_pass = $('#edit-pass').val(); /* Передаем пароль пользователя */
        console.log(reg_pass);
        var reg_mail = ""
        var reg_pass2 = ""
        var reg_phone = ""
        var vreg = 1 /* 1 - аутентификация пользователя */
        userUpdating(reg_mail, reg_login, reg_pass, reg_pass2, reg_phone, url, csrf_token, vreg);
     }

     // Вход, проверка , обработка форм из navbarreg.html по id="form_authentication"
     $('#login').click(function(e) { /* По нажатию кнопки id="login" navbarreg.html) вызываем функцию, передаем параметр e(элемент) */
        userVhod(e);

     });

     // Событие по Enter Вход, проверка , обработка форм из navbarreg.html по input id="edit-name" id="edit-pass"
     $('#edit-name,#edit-pass').keydown(function(e) {
    	if(e.keyCode == 13) {
            userVhod(e);
        }
     });

     // Функция Регистрации и записи при отсутствии регистрации на сайте, обработка форм
     function userReg(e){
        /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
        элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        var form = $('#form_registration'); /* Принимаем форму(form) по id=form_registration из form_vh_reg.html*/
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('#form_registration [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        var reg_mail = $('#edit-mail').val(); /* Передаем mail пользователя */
        console.log(reg_mail);
        var reg_login = $('#edit-namer').val(); /* Передаем login пользователя */
        console.log(reg_login);
        var reg_pass = $('#edit-passr').val(); /* Передаем пароль пользователя */
        var reg_pass2 = $('#edit-passr2').val(); /* Передаем пароль(подтверждение) пользователя */
        var reg_phone = $('#edit-phone').val(); /* Передаем телефон пользователя */
        console.log(reg_phone);
        var vreg = 2 /* 2 - регистрация нового пользователя */
        console.log(reg_pass);
        userUpdating(reg_mail, reg_login, reg_pass, reg_pass2, reg_phone, url, csrf_token, vreg)
     }

     // Регистрация и запись при отсутствии регистрации на сайте, обработка форм из navbarreg.html по id="form_registration"
     $('#submit').click(function(e) { /* По нажатию кнопки id="submit" navbarreg.html) вызываем функцию, передаем параметр e(элемент) */
        userReg(e);

     });

     // Событие по Enter Регистрация и запись при отсутствии регистрации на сайте, обработка форм из navbarreg.html
     // по input id="edit-mail" id="edit-namer" id="edit-passr" id="edit-passr2" id="edit-phone"
     $('#edit-mail,#edit-namer,#edit-passr,#edit-passr2,#edit-phone').keydown(function(e) {
    	if(e.keyCode == 13) {
            userReg(e);
        }
     });

     // Выход и обработка форм из navbarreg.html по id="form_logout"
     $('#Log-out').click(function(e) { /* По нажатию кнопки id="Log-out" navbarreg.html) вызываем функцию, передаем параметр e(элемент) */
     /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
     элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        var form = $('#form_logout'); /* Принимаем форму(form) по id=form_registration из navbarreg.html*/
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('#form_authentication [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        var reg_login = ""
        var reg_pass = ""
        var reg_mail = ""
        var reg_pass2 = ""
        var reg_phone = ""
        var vreg = 3 /* 3 - выход пользователя */
        userUpdating(reg_mail ,reg_login, reg_pass, reg_pass2, reg_phone, url, csrf_token, vreg);
     });

     /* Отправка данных в БД методом ajax для регистрации, входа и выхода учетной записи*/
     function userUpdating(reg_mail,reg_login,reg_pass, reg_pass2, reg_phone, url, csrf_token, vreg){
        var data = {}; /* Переменная массив, присваиваем ей mail,login и пароль */
        data.reg_mail = reg_mail;
        data.reg_login = reg_login;
        data.reg_pass = reg_pass;
        data.reg_pass2 = reg_pass2;
        data.reg_phone = reg_phone;

        /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
        data["csrfmiddlewaretoken"] = csrf_token;
        data.vreg = vreg;

        /* url это адрес на который необходимо отправлять post запрос, делаем через атрибут action.
        присваивается url адрес который прописан в атрибуте action нашей формы form в файле navbarreg.html
        т.е. через urls.py по registration переходим к функции Registration в blok1/views.py*/
        console.log("Выполняется функция userUpdating");
        console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/

        /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
        разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
        позволяет обмениваться данными между браузером и сервером.*/
         $.ajax({
             url: url, /* Отправляем массив данных data в обработку функцией Registration(запись в БД) на сервер в blok1/views.py */
             type: 'POST', /* определяем что метод post*/
             data: data, /* передаем переменной data ответом от сервера наш словарь dict return_user из blok1/views.py */
             cache: true, /* кеширование*/
             /* если успешный ответ сервера то success иначе error*/
             success: function (data) {
                 console.log("OK"); /* отображение в консоли броузера для проверки */
                 /* достаем из словаря data по индексу reg_login логин пользователя */
                 console.log(data); /* отображение в консоли логина пользователя */
                 if (data){
                    if (data.vreg == '1' || data.vreg == '3'){
                       /* location.reload(); /* если пользователь логинится,регистрируется или выходит то перегружаем страницу */
                       window.location.replace("http://"+location.host); /* перегружаем домашнюю страницу */

                    }
                    else{  /* вызываем выпадающее окно из wind_pop.js, передаем id="box  boxN" для info.html */
                        if (data.vreg == '0'){
                            popup('#box');
                        }
                        if (data.vreg == '2'){
                            popup('#box1');
                        }
                        if (data.vreg == '4'){
                            popup('#box2');
                        }
                        if (data.vreg == '5'){
                            popup('#box3');
                        }
                        if (data.vreg == '6'){
                            popup('#box4');
                        }
                        if (data.vreg == '7'){
                            popup('#box5');
                        }
                    }

                 }

             },
             error: function(){
                 console.log("error")
             }
         })

     }

});



// Выход пользователя из кабинета, с переходом на главную страницу
//$(document).on('click', '#Log-out', function(e){
//    var vreg = 0
//    var url = "/";
//    $('#Log-out').attr('href',url);
//});
// 'http://'+location.host.toString()+
