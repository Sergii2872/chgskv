/* формы изменения учетных данных пользователя вызываются из account_user.html и account_user_pass.html*/
$(document).ready(function(){  /* Стандартная обертка, т.е. скрипт выполняется когда загрузится весь html документ */

     $('#auth_user').click(function(e) { /* По нажатию кнопки id="auth_user" account_user.html) вызываем функцию, передаем параметр e(элемент) */

     /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
     элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        var form = $('#form_auth'); /* Принимаем форму(form) по id=form_auth из account_user.html*/
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('#form_auth [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        var izm_fname = $('#fname').val(); /* Передаем имя пользователя */
        console.log(izm_fname);
        var izm_lname = $('#lname').val(); /* Передаем фамилию пользователя */
        console.log(izm_lname);
        var izm_locat = $('#locat').val(); /* Передаем адрес пользователя */
        console.log(izm_locat);
        var izm_bdate = $('#bdate').val(); /* Передаем дату рождения пользователя */
        console.log(izm_bdate);
        userIzm(izm_fname, izm_lname, izm_locat, izm_bdate, url, csrf_token)

     });

     $('#auth_userp').click(function(e) { /* По нажатию кнопки id="auth_user" account_user_pass.html) вызываем функцию, передаем параметр e(элемент) */

     /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
     элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        var form = $('#form_auth'); /* Принимаем форму(form) по id=form_auth из account_user.html*/
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('#form_auth [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        var izm_pass1 = $('#pass1').val(); /* Передаем пароль пользователя */
        console.log(izm_pass1);
        var izm_pass2 = $('#pass2').val(); /* Передаем повторный пароль пользователя */
        console.log(izm_pass2);
        userIzmP(izm_pass1, izm_pass2, url, csrf_token)

     });

     /* Отправка данных в БД методом ajax для изменения учетных данных пользователя*/
     function userIzm(izm_fname, izm_lname, izm_locat, izm_bdate, url, csrf_token){
        var data = {}; /* Переменная массив, присваиваем ей полученные имя,фамилию,адрес и дату рождения */
        data.izm_fname = izm_fname;
        data.izm_lname = izm_lname;
        data.izm_locat = izm_locat;
        data.izm_bdate = izm_bdate;

        /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
        data["csrfmiddlewaretoken"] = csrf_token;

        /* url это адрес на который необходимо отправлять post запрос, делаем через атрибут action.
        присваивается url адрес который прописан в атрибуте action нашей формы form в файле navbarreg.html
        т.е. через urls.py по registration переходим к функции Registration в views.py*/
        console.log("Выполняется функция userIzm");
        console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/

        /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
        разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
        позволяет обмениваться данными между браузером и сервером.*/
         $.ajax({
             url: url, /* Отправляем массив данных data в обработку функцией Account_user(запись в БД) на сервер в views.py */
             type: 'POST', /* определяем что метод post*/
             data: data, /* передаем переменной data ответом от сервера наш словарь return_izm из views.py */
             cache: true, /* кеширование*/
             /* если успешный ответ сервера то success иначе error*/
             success: function (data) {
                 console.log("Ответ ОК, полученные данные:"); /* отображение в консоли броузера для проверки */
                 console.log(data);
                 if (data){
                    if (data.vreg == '1'){
                        $('#fn').text(" "+data.first_name);
                        $('#ln').text(" "+data.last_name);
                        $('#lc').text(" "+data.location);
                        $('#bd').text(" "+$.date(data.birth_date));

                        popup('#box9'); /* вызываем выпадающее окно из wind_pop.js, передаем id="box9" для info.html */
                        }
                    if (data.vreg == '0'){
                        popup('#box10'); /* вызываем выпадающее окно из wind_pop.js, передаем id="box10" для info.html */
                    }
                 }

             },
             error: function(){
                 console.log("error")
             }
         })

     }

     /* Отправка данных в БД методом ajax для изменения учетных данных пользователя(только пароля)*/
     function userIzmP(izm_pass1, izm_pass2, url, csrf_token){
        var data = {}; /* Переменная массив, присваиваем ей полученные имя,фамилию,адрес и дату рождения */
        data.izm_pass1 = izm_pass1;
        data.izm_pass2 = izm_pass2;

        /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
        data["csrfmiddlewaretoken"] = csrf_token;

        /* url это адрес на который необходимо отправлять post запрос, делаем через атрибут action.
        присваивается url адрес который прописан в атрибуте action нашей формы form в файле navbarreg.html
        т.е. через urls.py по registration переходим к функции Registration в views.py*/
        console.log("Выполняется функция userIzmP");
        console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/

        /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
        разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
        позволяет обмениваться данными между браузером и сервером.*/
         $.ajax({
             url: url, /* Отправляем массив данных data в обработку функцией Registration(запись в БД) на сервер в views.py */
             type: 'POST', /* определяем что метод post*/
             data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
             cache: true, /* кеширование*/
             /* если успешный ответ сервера то success иначе error*/
             success: function (data) {
                 console.log("OK"); /* отображение в консоли броузера для проверки */
                 /* достаем из словаря data по индексу reg_login логин пользователя */
                 console.log(data); /* отображение в консоли логина пользователя */
                 if (data){ /* вызываем выпадающее окно из wind_pop.js, передаем id="box6  boxN" для info.html */
                     if (data.vizm == '0'){
                        alert('Пароль успешно изменен!');
                        //popup('#box6');
                        window.location.replace("http://"+location.host+"/Kabinet"); /* перегружаем страницу кабинета*/
                     }
                     if (data.vizm == '1'){
                        popup('#box7');
                     }
                     if (data.vizm == '2'){
                        popup('#box8');
                     }
                 }

             },
             error: function(){
                 console.log("error")
             }
         })

     }

/* Функция инвертирования строки, не использую */
function reverseStr(str) {
    return str.split("").reverse().join("");
}

/* Функция преобразования даты */
$.date = function(dateObject) {
    var d = new Date(dateObject);
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    var date = day + "-" + month + "-" + year;

    return date;
};

});




