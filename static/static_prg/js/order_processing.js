// скрипт таблицы datatables.net
// orders_table это id нашей таблицы в order_processing.html
$(document).ready(function() {
        $('#orders_table').DataTable(
                {
                    dom: 'lfBrtip',
                    lengthMenu: [
                    [ 10, 15, 50, 100 ],
                    [ '10 Записей', '15 Записей', '50 Записей', '100 Записей' ]
                    ],
                    buttons: [

                        {   extend: 'copy', exportOptions: {
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                }
                        },
                        {   extend: 'csv', exportOptions: {
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                }
                        },
                        {   extend: 'excel', exportOptions: {
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                }
                        },
                        {   extend: 'pdf', exportOptions: {
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                }
                        },
                        {
                            extend: 'print',
                            text: 'Печать',
                            titleAttr: 'Печать таблицы',
                            title: 'Заявки со статусом - ожидают оплаты клиентом',
                            autoPrint: true,
                            exportOptions: {
                                columns: ':visible',
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                            },
                            customize: function (win) {
                                $(win.document.body).find('table').addClass('display').css('font-size', '9px');
                                $(win.document.body).find('tr:nth-child(odd) td').each(function(index){
                                    $(this).css('background-color','#D0D0D0');
                                });
                                $(win.document.body).find('h1').css('text-align','center');
                            }
                        }
                    ],
                    "order":  [[ 0, "asc" ]], // "order":  [[ 0, "asc" ]] сортировка по первому столбцу по возрастанию
                    "pageLength": 10, // по умолчанию не более 10 записей на одной странице
                    scrollY:        "300px",
                    scrollX:        true,
                    scrollCollapse: true,
                    paging:         true,
                    fixedColumns:   {
                        left: 1,
                        right: 2
                    },
                    'columnDefs': [
                    {'targets': [14],
                     'searchable': false,
                     'orderable': false
                    }]

                }
        );


// Проверка возможности покупки заявки на бирже Poloniex по input type="submit" и class="check_currency" из order_processing.html
$('.check_currency').click(function(e) {
    e.preventDefault();
    var item_id = $(this).data("item_id");
    console.log(item_id);
    var url = '/Poloniex/Order_processing_check/'; /* blok4/views.py функция Order_processing_check */
    var data = {}; /* Переменная массив */
    data.item_id= item_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('#form-orderstable [name="csrfmiddlewaretoken"]').val();
    console.log("Order_processing_check");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Order_processing_buy на сервер в blok4/views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_izm из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             var dt = new Date(); // текущая дата
             var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds(); // текущее время
             console.log(data); /* отображение в консоли ответа от blok4/views.py функция Order_processing_check */
             dp = ""
             $.each(data.deposit, function(k, v){
                    dp = dp + '<h4>' + 'Дата: ' + v.timestamp + '</h4>' + '<h4>' + ' Сумма: ' + v.amount + ' ' +
                     v.currency + '</h4>' + '<h4>' + ' Адрес: ' + v.address + '</h4>' +
                      '<h4>' + '---------------------------------------------' + '</h4>';
                 });

             $.alert('Результат проверки Poloniex' + ', ' + time + ' : ' + '<h4>' + data.info + '</h4>' +
              'Баланс(остаток): ' + '<h4>' + data.balans + '  ' + data.name_currency_symbol + '</h4>' +
               'Текущий курс биржи Poloniex: ' + '<h4>' + data.kurs + '</h4>' +
                'Курс продажи Клиенту: ' + '<h4>' + data.kurs_sell + '</h4>' +
                 'Сумма ожидаемого прихода от Клиента: ' + '<h4>' + Number(data.sum_currency_buy).toFixed(5) + '  ' + data.name_currency_symbol + '</h4>' +
                  'На кошелек(адрес): ' + '<h4>' + data.wallet_fact + '</h4>' +
                   'ПОСТУПИЛО: ' + dp);


         },
             error: function(){
                 console.log("error")
             }
         })
     });

// Удаление заявки по input type="submit" и class="del_currency" из order_processing.html
$('.del_currency').click(function(e) {
    e.preventDefault();
    var item_id = $(this).data("item_id");
    console.log(item_id);
    var url = '/Poloniex/Order_processing_del/';
    var data = {}; /* Переменная массив */
    data.item_id= item_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('#form-orderstable [name="csrfmiddlewaretoken"]').val();
    console.log("Order_processing_del");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Order_processing_buy на сервер в blok4/views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             var dt = new Date(); // текущая дата
             var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds(); // текущее время
             console.log(data); /* отображение в консоли ответа от blok4/views.py функция Order_processing_del */
             $.alert('Заявка ' + data.exchange_requests + ' удалена');
             setTimeout("window.location.reload()", 1500); /* перегружаем страницу */


         },
             error: function(){
                 console.log("error")
             }
         })
     });

// Покупки по заявке на бирже Poloniex по input type="submit" и class="buy_currency" из order_processing.html
$('.buy_currency').click(function(e) {
    e.preventDefault();
    var item_id = $(this).data("item_id");
    console.log(item_id);
    var url = '/Poloniex/Order_processing_buy/';
    var data = {}; /* Переменная массив */
    data.item_id= item_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('#form-orderstable [name="csrfmiddlewaretoken"]').val();
    console.log("Order_processing_buy");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Order_processing_buy на сервер в blok4/views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             var dt = new Date(); // текущая дата
             var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds(); // текущее время
             console.log(data); /* отображение в консоли ответа от blok4/views.py функция Order_processing_buy */
             $.alert(data.info);
             if(data.i != 1){
                    setTimeout("window.location.reload()", 1500); /* перегружаем страницу */
             }

         },
             error: function(){
                 console.log("error")
             }
         })
     });

});

// Исполнение заявки по input type="submit" и class="perform_currency" из order_processing.html
$('.perform_currency').click(function(e) {
    e.preventDefault();
    var item_id = $(this).data("item_id");
    console.log(item_id);
    var url = '/Poloniex/Order_processing_perform/';
    var data = {}; /* Переменная массив */
    data.item_id = item_id;

    $.confirm({
    title: 'Изменить',
    content: '' +
    '<form action="" class="formName">' +
    '<div class="form-group">' +
    '<label>фактический курс</label>' +
    '<input type="number" placeholder="0.00000000" class="kurs_buy_fact form-control" required />' +
    '<label>фактический сумма покупки</label>' +
    '<input type="number" placeholder="0.00000000" class="sum_currency_buy_fact form-control" required />' +
    '</div>' +
    '</form>',
    buttons: {
        formSubmit: {
            text: 'Submit',
            btnClass: 'btn-blue',
            action: function () {
                var kurs_buy_fact = this.$content.find('.kurs_buy_fact').val();
                var sum_currency_buy_fact = this.$content.find('.sum_currency_buy_fact').val();
                if(kurs_buy_fact == 0){
                    $.alert('укажите фактический курс покупки!');
                    return false;
                }
                if(sum_currency_buy_fact == 0){
                    $.alert('укажите фактическую сумму покупки!');
                    return false;
                }
                data.kurs_buy_fact = kurs_buy_fact;
                data.sum_currency_buy_fact = sum_currency_buy_fact;
                /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
                data["csrfmiddlewaretoken"] = $('#form-orderstable [name="csrfmiddlewaretoken"]').val();
                console.log("Order_processing_perform");
                console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
                /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
                разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
                позволяет обмениваться данными между браузером и сервером.*/
                 $.ajax({
                     url: url, /* Отправляем массив данных data в обработку функцией Order_processing_buy на сервер в blok4/views.py */
                     type: 'POST', /* определяем что метод post*/
                     data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
                     cache: true, /* кеширование*/
                     /* если успешный ответ сервера то success иначе error*/
                     success: function (data) {
                         console.log("OK"); /* отображение в консоли броузера для проверки */
                         var dt = new Date(); // текущая дата
                         var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds(); // текущее время
                         console.log(data); /* отображение в консоли ответа от blok4/views.py функция Order_processing_del */
                         $.alert('Заявка ' + data.exchange_requests + ' исполнена');
                         setTimeout("window.location.reload()", 1500); /* перегружаем страницу */


                     },
                         error: function(){
                             console.log("error")
                         }
                     })

            }
        },
        cancel: function () {
            //close
        },
    },
    onContentReady: function () {
        // bind to events
        var jc = this;
        this.$content.find('form').on('submit', function (e) {
            // if the user submits the form by pressing enter in the field.
            e.preventDefault();
            jc.$$formSubmit.trigger('click'); // reference the button and click it

        });
    }
    });




     });