/* не использую, т.к. после перерисовки страницы $(location).attr('href',url); изменить текст не получилось */
/* скрипт для Страницы заявки с номером ID для обмена клиентом выбранных валют и суммы перед оплатой с обновлением страницы вызывается по class="form_exchange_currency_bid_info" из exchange_currency_bid.html */
$(document).ready(function(){  /* Стандартная обертка, т.е. скрипт выполняется когда загрузится весь html документ */

/* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы
    e.preventDefault();*/
    var form = $('.form_exchange_currency_bid_info'); /* Принимаем форму(form) по class=form_exchange_currency_bid_info из exchange_currency_bid.html */
    console.log(form); /* Выводим на консоль значения полученной формы */
    var url = form.attr("action");
    console.log(url);
    var csrf_token = $('.form_exchange_currency_bid_info [name="csrfmiddlewaretoken"]').val();
    console.log(csrf_token);
    /* Считываем элементы div в котором прописан data-аттрибут data-имя переменной
    выбранной валюты со значениями из exchange_currency_bid.html по селектору class="data_exchange" */
    /* Присваиваем переменной currency_by_id значение data-аттрибута currency_by_id переданного через div */
    /*var currency_by_id = $(this).data("currency_by_id");*/
    var currency_by_id = $('input[name="currency_by_id"]').val();
    console.log(currency_by_id);
    var currency_by_currency = $('input[name="currency_by_currency"]').val();
    console.log(currency_by_currency);
    var currency_sell_id = $('input[name="currency_sell_id"]').val();
    console.log(currency_sell_id);
    var currency_sell_currency = $('input[name="currency_sell_currency"]').val();
    console.log(currency_sell_currency);
    var request_id = $('input[name="request_id"]').val();
    console.log(request_id);
    $(location).attr('href',url);
    $('#str1').append('Заявка ID ' + request_id + ' Обмен ' + currency_by_currency + ' на ' + currency_sell_currency);
    console.log(request_id);





});