/* скрипт для выполнения действий при клике на кнопки input из exchange_currency_bid_info.html вызывается по id="request_del" */
// кнопка при input value="Отменить заявку"
$(document).ready(function(){  /* Стандартная обертка, т.е. скрипт выполняется когда загрузится весь html документ */

$('#request_del').click(function(e) {
    e.preventDefault();
    var request_id = $(this).data("request_id");
    console.log(request_id);
    var url = '/Exchange_request_del/';
    var data = {}; /* Переменная массив */
    data.request_id= request_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('.form_exchange_currency_pay [name="csrfmiddlewaretoken"]').val();
    console.log("Exchange_request_del");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Exchange_request_del на сервер в blok1/views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             console.log(data); /* отображение в консоли ответа от blok1/views.py функция Exchange_request_del */
             if (data.result == '0'){
                       $('#info_time').html("");
                       $('#info_time').append('Время изменения статуса: ' + data.updated);
                       $('#info_status').html("");
                       $('#info_status').append('Заявка удалена').css('color', 'red');
                       $('#button').html("");
                       $('#exit_update').html("");
                       $.alert('Заявка удалена!');

             }


         },
             error: function(){
                 console.log("error")
             }
         })
     });


// кнопка при input value="Включить обновление"
$('#enable_update').click(function(e) {
    e.preventDefault();
    var request_id = $(this).data("request_id");
    var market = $(this).data("market");
    var name_bank_buy = $(this).data("name_bank_buy");
    console.log(request_id);
    console.log(market);
    console.log(name_bank_buy);
    var url = '/Exchange_currency_bid_info/'+request_id+'/'+market+'/'+name_bank_buy;
    var data = {}; /* Переменная массив */
    data.request_id = request_id;
    data.market = market;
    data.name_bank_buy = name_bank_buy;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('.form_exchange_currency_bid_info [name="csrfmiddlewaretoken"]').val();
    console.log("Обновление Exchange_currency_bid_info");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Exchange_currency_bid_info на сервер в blok1/views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_izm из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             console.log(data); /* отображение в консоли ответа от blok1/views.py функция Exchange_currency_bid_info */
             $('#exit_update').html("");
             // меняем кнопку включить на выключить, по которой по форме name="form_exchange_currency_bid_info"
             // переходим на страницу action="{% url 'Exchange_currency_bid_info' request_id=request_id market=market name_bank_buy=name_bank_buy %}" из exchange_currency_bid_info.html
             // в div id="exit_update"
             var r= $('<input type="submit" class="btn btn-primary btn-md section-top" value="Выключить обновление"/>');
             $("#exit_update").append(r);
             console.log(request_id);
             console.log(market);
             console.log(name_bank_buy);
             console.log(url);
             var delay = 30000; // интервал 30 секунд
             $('#button').html("");
             $('#button').append('Статус заявки будет обновляться каждые ' + delay/1000 + ' секунд ');
             $('#progressDiv').progressbar({
                value: 1, // задаем начальное значение прогрессбару
                create: function(event, ui) {$(this).find('.ui-widget-header').css({'background-color':'#5453c5'})} // цвет индикатора
             });
             startProgress(); // фнкция запуска прогрессбара
             // Метод setInterval предназначен для вызова кода через указанные промежутки времени(асинхронный)
             setInterval(function(){
                 $('#progressDiv').progressbar("destroy"); // удаляет функциональность индикатора выполнения прогрессбара
                 $('#progressDiv').progressbar({
                    value: 1, // задаем начальное значение прогрессбару
                    create: function(event, ui) {$(this).find('.ui-widget-header').css({'background-color':'#57d199'})} // цвет индикатора
                 });
                 startProgress(); // фнкция запуска прогрессбара
                 var dt = new Date();
                 var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds(); // текущее время
                 $('#button').html("");
                 $('#button').append('Обновление каждые ' + delay/1000 + ' секунд ' + time);
                 var url = '/Exchange_currency_bid_info/'+request_id+'/'+market+'/'+name_bank_buy;
                 data["csrfmiddlewaretoken"] = $('.form_exchange_currency_bid_info [name="csrfmiddlewaretoken"]').val();
                 $.ajax({
                         url: url, /* Отправляем массив данных data в обработку функцией /Exchange_currency_bid_info на сервер в blok1/views.py */
                         type: 'POST', /* определяем что метод post*/
                         data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
                         cache: true, /* кеширование*/
                         /* если успешный ответ сервера то success иначе error*/
                         success: function (data) {
                             console.log("OK"); /* отображение в консоли броузера для проверки */
                             console.log(data); /* отображение в консоли ответа от blok1/views.py функция /Exchange_currency_bid_info */
                             // обновляем статус
                             $('#info_status').html("");
                             if (data.status == 1){
                                $("#info_status").append('Принята, ожидает оплаты клиентом').css('color', '#165a8c')
                             }
                             if (data.status == 2){
                                $("#info_status").append('Заявка исполнена').css('color', '#1f6220')
                             }
                             if (data.status == 0){
                                $("#info_status").append('Заявка удалена').css('color', '#e3122d')
                             }
                         },
                         error: function(){
                             console.log("error")
                         }
                 });

             },delay);


         },
             error: function(){
                 console.log("error")
             }
         })
     });


// для прогресс бара библиотеки jquery ui js/jquery-ui.min.js
// пример https://professorweb.ru/my/javascript/jquery/level4/4_3.php
// описание, методы https://api.jqueryui.com/progressbar/#option-value
var i = 0;
function startProgress()
{
    if (i > 100){
        // обнуляем итерации для следующего интервала индикатора
        i = 0;
        return;}
    else
        $('#progressDiv').progressbar("value", i++);
        setTimeout(startProgress, 300);
}

});