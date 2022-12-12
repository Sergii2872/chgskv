/* скрипт для списка валют пункт меню ОБМЕН вызывается по class="currencies_sell" из exchange.html */
$(document).ready(function(){  /* Стандартная обертка, т.е. скрипт выполняется когда загрузится весь html документ */

$('.currencies_sell').click(function(e) {
     /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
     элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        var form = $('.form_currencies_sell'); /* Принимаем форму(form) по class=form_currencies_sell из exchange.html*/
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('.form_currencies_sell [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        /* Считываем элементы div в котором прописан data-аттрибут data-currency_id
        выбранной валюты со значениями из exchange.html по селектору class="currencies_sell" */
        /* Присваиваем переменной currency_id значение data-аттрибута currency_id переданного через div */
        var currency_id = $(this).data("currency_id");
        console.log(currency_id);
        Currencies_Sell_Updating(currency_id, url, csrf_token)
     });


/* Отправка данных в БД методом ajax */
     function Currencies_Sell_Updating(currency_id, url, csrf_token){
        var data = {}; /* Переменная массив, присваиваем ей id покупаемой валюты*/
        data.currency_id = currency_id;
        /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
        data["csrfmiddlewaretoken"] = csrf_token;
        /* url это адрес на который необходимо отправлять post запрос, делаем через атрибут action, кот. работает с префиксами всех языков(англ,рус и т.д.)
        присваивается url адрес который прописан в атрибуте action нашей формы form в файле exchange.html
        т.е. через urls.py по list_currencies_sell переходим к функции list_currencies_sell в views.py*/
        console.log("Currencies_Sell_Updating");
        console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
        /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
        разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
        позволяет обмениваться данными между браузером и сервером.*/
         $.ajax({
             url: url, /* Отправляем массив данных data в обработку функцией list_currencies_sell на сервер в views.py */
             type: 'POST', /* определяем что метод post*/
             data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
             cache: true, /* кеширование*/
             /* если успешный ответ сервера то success иначе error*/
             success: function (data) {
                 console.log("OK"); /* отображение в консоли броузера для проверки */
                 $('#currencies_sell').html(""); /* очищаем(обновляем) блок заголовка покупки валют(от html кода) чтоб при выборе покупаемых валют продаваемые не дублировались в окне */
                 /* достаем из словаря data по индексу currency_purchase  список покупаемой валюты у клиента для отображения в заголовке наименования и */
                 /* и переменной currencie_purchase_id присваиваем id покупаемой у клиента валюты */
                 $.each(data.currency_purchase, function(k, v){
                    $('#currencies_sell').append('Вы отдаете ' + v.name_currences_purchase_currency);
                    currencie_purchase_id=v.name_currences_purchase_id;
                    market_exchange_id=v.name_currences_purchase_market_exchange_id;

                 });
                 /* достаем из словаря data по индексу currency_sell  список продаваемых валют */
                 console.log(data.currency_sell); /* отображение в консоли списка продаваемых валют */
                 $('#currencies_purchase').html(""); /* очищаем(обновляем) блок продажи валют(от html кода) чтоб при выборе покупаемых валют продаваемые не дублировались в окне */
                 $('#currencies_purchase').append('<div class="currency_table_title"><span>Вы получаете</span></div>');
                 /* проходим по списку продаваемых валют из словаря data по индексу currency_sell и показываем его в блоке */
                 /* в функции k - это индекс, v - сам объект(значение) из списка data.currency_sell */
                 /* в ссылке href передаем url значения выбранных клиентом для обмена валют currencie_purchase_id - id покупаемой валюты v.id - id продаваемой валюты*/
                 if (market_exchange_id == 3){
                    $.each(data.currency_sell, function(k, v){
                    $('#currencies_purchase').append('<a href="' + v.url1 + currencie_purchase_id + '/' + v.id +
                    '" id="txt1"><div class="contmeleft"><img src="'+v.image_currency+'"><p>' +
                    v.currency+'</p><p> Курс 1 ' + v.name_currency_currency +' ➯' + Number(v.kurs_sell_inverse).toFixed(8) +
                    '</p><p> Резерв ➯'+Number(v.balance_amount).toFixed(2) +
                    '</p></div></a></div></form>');
                 });
                 }
                 else {
                    $.each(data.currency_sell, function(k, v){
                    $('#currencies_purchase').append('<a href="' + v.url1 + currencie_purchase_id + '/' + v.id +
                    '" id="txt1"><div class="contmeleft"><img src="'+v.image_currency+'"><p>' +
                    v.currency+'</p><p> Курс 1 ➯' + Number(v.kurs_sell).toFixed(8) +
                    '</p><p> Резерв ➯'+Number(v.balance_amount).toFixed(2) +
                    '</p></div></a></div></form>');
                 });

                 }


             },
             error: function(){
                 console.log("error")
             }
         })

     };



});

