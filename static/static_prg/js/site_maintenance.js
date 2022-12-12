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
                                columns: [0, 1, 2, 3],
                                }
                        },
                        {   extend: 'csv', exportOptions: {
                                columns: [0, 1, 2, 3],
                                }
                        },
                        {   extend: 'excel', exportOptions: {
                                columns: [0, 1, 2, 3],
                                }
                        },
                        {   extend: 'pdf', exportOptions: {
                                columns: [0, 1, 2, 3],
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
                                columns: [0, 1, 2, 3],
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
                    "pageLength": 10, // по умолчанию не более 5 записей на одной странице
                    scrollY:        "300px",
                    scrollX:        true,
                    scrollCollapse: true,
                    paging:         true,
                    fixedColumns:   {
                        left: 1,
                        right: 1
                    },
                    'columnDefs': [
                    {'targets': [4],
                     'searchable': false,
                     'orderable': false
                    }]

                }
        );

$('.check_active').click(function(e) {
    e.preventDefault();
    var item_id = $(this).data("item_id");
    console.log(item_id);
    var url = '/Kabinet/Site_maintenance_active/';
    var data = {}; /* Переменная массив */
    data.item_id= item_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('#form-orderstable [name="csrfmiddlewaretoken"]').val();
    console.log("Site_maintenance_check");
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
             $.alert('Сайт переведен на техобслуживание');
             setTimeout("window.location.reload()", 1500); /* перегружаем страницу */

         },
             error: function(){
                 console.log("error")
             }
         })
     });


$('.check_deactivate').click(function(e) {
    e.preventDefault();
    var item_id = $(this).data("item_id");
    console.log(item_id);
    var url = '/Kabinet/Site_maintenance_deactivate/';
    var data = {}; /* Переменная массив */
    data.item_id= item_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('#form-orderstable [name="csrfmiddlewaretoken"]').val();
    console.log("Site_maintenance_check");
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
             $.alert('Сайт переведен в рабочий режим');
             setTimeout("window.location.reload()", 1500); /* перегружаем страницу */

         },
             error: function(){
                 console.log("error")
             }
         })
     });

});