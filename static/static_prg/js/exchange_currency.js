/* скрипт для выбора валют для обмена при изменении выбора пары из формы обмена вызывается по onchange="Exchange_currency_select_sell.call(this, event, {{currence_by.id}}) из form_exchange.html */
// при выборе select "ОТДАЕТЕ"
function Exchange_currency_select_by(event, currency_sell_id) {
    var currency_by_id = this.options[this.selectedIndex].value; // получаем id покупаемой валюты из select
    console.log(currency_by_id);
    console.log(currency_sell_id);
    var url = '/Exchange_currency_select_by/';
    var data = {}; /* Переменная массив */
    data.currency_by_id = currency_by_id;
    data.currency_sell_id = currency_sell_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('.form_exchange_currency [name="csrfmiddlewaretoken"]').val();
    console.log("Exchange_currency_select_by");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Exchange_currency_select_by на сервер в blok1/views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             //$('#kurs').html(""); /* очищаем(обновляем) строку курса пары валют(от html кода)*/
             /* достаем из словаря data по индексу currencys_pair_exchange_rate курс выбранной пары валют для отображения в строке курса */
             console.log(data); /* отображение в консоли курса пары выбранных валют */
             //$('#kurs').append('Курс обмена: 1 ' + data.name_currences_sell.currency + '➯ ' + data.currencys_pair_exchange_rate.kurs_sell + ' ' + data.name_currences_by.currency);
             if (data.result_pair_currencies == '1'){
                       // переход на страницу обмена выбранной пары валют
                       var url = '/form_exchange/' + data.name_currences_by.id + '/' + data.name_currences_sell.id;
                       $(location).attr('href',url);
             }
             else {
                       $.dialog('Такое направление обмена не существует!');
                       // перегружаем страницу с новыми списками данных продаваемых валют соответствующих покупаемой
                       var url = '/form_exchange/' + data.name_currences_by.id + '/' + data.name_currences_sell;
                       $(location).attr('href',url);
             }

         },
             error: function(){
                 console.log("error")
             }
         })
}

// при выборе select "ПОЛУЧАЕТЕ"
function Exchange_currency_select_sell(event, currency_by_id) {
    var currency_sell_id = this.options[this.selectedIndex].value;
    console.log(currency_by_id);
    console.log(currency_sell_id);
    var url = '/Exchange_currency_select_by/';
    var data = {}; /* Переменная массив */
    data.currency_by_id = currency_by_id;
    data.currency_sell_id = currency_sell_id;
    /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
    data["csrfmiddlewaretoken"] = $('.form_exchange_currency [name="csrfmiddlewaretoken"]').val();
    console.log("Exchange_currency_select_by");
    console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
    /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
    разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
    позволяет обмениваться данными между браузером и сервером.*/
     $.ajax({
         url: url, /* Отправляем массив данных data в обработку функцией Exchange_currency_select_by на сервер в views.py */
         type: 'POST', /* определяем что метод post*/
         data: data, /* передаем переменной data ответом от сервера наш словарь return_dict из views.py */
         cache: true, /* кеширование*/
         /* если успешный ответ сервера то success иначе error*/
         success: function (data) {
             console.log("OK"); /* отображение в консоли броузера для проверки */
             //$('#kurs').html(""); /* очищаем(обновляем) строку курса пары валют(от html кода)*/
             /* достаем из словаря data по индексу currencys_pair_exchange_rate курс выбранной пары валют для отображения в строке курса */
             console.log(data); /* отображение в консоли курса пары выбранных валют */
             //$('#kurs').append('Курс обмена: 1 ' + data.name_currences_sell.currency + '➯ ' + data.currencys_pair_exchange_rate.kurs_sell + ' ' + data.name_currences_by.currency);
             if (data.result_pair_currencies == '1'){
                       // переход на страницу обмена выбранной пары валют
                       var url = '/form_exchange/' + data.name_currences_by.id + '/' + data.name_currences_sell.id;
                       $(location).attr('href',url);
             }
             else {
                       $.alert('Такое направление обмена не существует!');
             }

         },
             error: function(){
                 console.log("error")
             }
         })

}

// вычисление поля формы input для отображения результата вычисления по id=result из form_exchange.html
function Input_result(event, kurs) {
        // Get the input elements by targeting their id:
        var sum = $("#sum_by").val()
        console.log(kurs)
        console.log(sum)
        if(kurs == 0){
            $('#result').val(0);
            $.alert('Курс не установлен!');
        }
        else{
            $('#result').val((sum / kurs).toFixed(2)); // округляем до 2 десятич знаков
        }

}

// вычисление поля формы input для отображения результата вычисления по id=sum_by из form_exchange.html
function Input_sum(event, kurs) {
        // Get the input elements by targeting their id:
        var sum = $("#result").val()
        console.log(kurs)
        console.log(sum)
        if(kurs == 0){
            $('#sum_by').val(0);
            $.alert('Курс не установлен!');
        }
        else{
            $('#sum_by').val((sum * kurs).toFixed(2)); // округляем до 2 десятич знаков
        }

}

// Функция проверки введенных данных формы обмена
function validateForm() {
    var a = document.forms["form_exchange_currency"]["sum_by"].value;
    var b = document.forms["form_exchange_currency"]["result"].value;
    var c = document.forms["form_exchange_currency"]["wallet_by"].value;
    var d = document.forms["form_exchange_currency"]["wallet_sell"].value;
    var e = document.forms["form_exchange_currency"]["email"].value;
    var market = document.forms["form_exchange_currency"]["market"].value;
    var i = 0; // индикатор
    var k = 0; // индикатор
    if (a == null || a == "" || a == 0, b == null || b == "" || b == 0) {
      //$.alert('Cумма должна быть больше 0!');
      $(".error_sum").html("");
      $(".error_sum").append('Cумма должна быть больше 0!').css('color', 'red');
      $("#sum_by").css('border-color', 'red');
      $("#result").css('border-color', 'red');
      return false;
    }
    else {
      $("#sum_by").css('border-color', 'green');
      $("#result").css('border-color', 'green');
      $(".error_sum").html("");
    }
    if (c == null || c == "") {
      if(market == 3) {
        //$.alert('Поле "Карта" раздел "Отдаете" не может быть пустым!');
        $("#error_wallet_by").html("");
        $("#error_wallet_by").append('Поле "Карта" не может быть пустым!').css('color', 'red');
        $("#placeholder_bank_name_buy").css('border-color', 'red');
      }
      else {
        //$.alert('Поле "С кошелька" не может быть пустым!');
        $("#error_wallet_by").html("");
        $("#error_wallet_by").append('Поле "С кошелька" не может быть пустым!').css('color', 'red');
        $("#wallet_by").css('border-color', 'red');
      }
      return false;
    }
    else {
      if(market == 3) {
        // проверка номера карты скриптом jquery.creditCardValidator.js
        $('#placeholder_bank_name_buy').validateCreditCard(function(result){
            if(!(result.valid)){
                    console.log(result.valid)
                    $("#error_wallet_by").html("");
                	$("#error_wallet_by").append('Проверьте номер карты отправителя').css('color', 'red');
                	$("#placeholder_bank_name_buy").css('background-color','#FFFFDF');
                	$("#placeholder_bank_name_buy").css('border-color', 'red');
            		i = 1;
            }
            else {
                $("#error_wallet_by").html("");
                $("#placeholder_bank_name_buy").css('background-color','');
                $("#placeholder_bank_name_buy").css('border-color', 'green');
            }
        });
        if(i==1){
            return false;
        }
      }
      else {
        $("#wallet_by").css('border-color', 'green');
        $("#error_wallet_by").html("");
      }
    }
    if (d == null || d == "") {
      if(market == 3) {
        //$.alert('Поле "Карта" раздел "Получаете" не может быть пустым!');
        $("#error_wallet_sell").html("");
        $("#error_wallet_sell").append('Поле "Карта" не может быть пустым!').css('color', 'red');
        $("#placeholder_bank_name_sell").css('border-color', 'red');
      }
      else {
        //$.alert('Поле "На счет" не может быть пустым!');
        $("#error_wallet_sell").html("");
        $("#error_wallet_sell").append('Поле "На счет" не может быть пустым!').css('color', 'red');
        $("#wallet_sell").css('border-color', 'red');
      }
      return false;
    }
    else {
      if(market == 3) {
        // проверка номера карты скриптом jquery.creditCardValidator.js
        $('#placeholder_bank_name_sell').validateCreditCard(function(result){
            if(!(result.valid)){
                    console.log(result.valid)
                    $("#error_wallet_sell").html("");
                	$("#error_wallet_sell").append('Проверьте номер карты получателя').css('color', 'red');
                	$("#placeholder_bank_name_sell").css('background-color','#FFFFDF');
                	$("#placeholder_bank_name_sell").css('border-color', 'red');
            		k = 1;
            }
            else {
                $("#error_wallet_sell").html("");
                $("#placeholder_bank_name_sell").css('background-color','');
                $("#placeholder_bank_name_sell").css('border-color', 'green');
            }
        });
        if(k==1){
            return false;
        }
      }
      else {
        $("#wallet_sell").css('border-color', 'green');
        $("#error_wallet_sell").html("");
      }
    }
    if (e == null || e == "") {
      //$.alert('Поле email не может быть пустым!');
      $("#error_email").html("");
      $("#error_email").append('Поле email не может быть пустым!').css('color', 'red');
      $("#email").css('border-color', 'red');
      return false;
    }
    else {
      $("#email").css('border-color', 'green');
      $("#error_email").html("");
    }
  }


// отображение в input placeholder наменования карт банков для фиатных валют при загрузке страницы form_exchange.html
$(document).ready(function() {
    //var name_bank = 'Карта ' + $('#placeholder_bank_name').val();
    //var name_bank = $('#placeholder_bank_name').attr('value')
    //var name_bank = document.forms["form_exchange_currency"]["wallet_by"].value;
    //var name_bank = document.getElementById("placeholder_bank_name");
    var name_bank_buy = 'Карта ' + $('#placeholder_bank_name_buy').data("name_bank_buy");
    var name_bank_sell = 'Карта ' + $('#placeholder_bank_name_sell').data("name_bank_sell");
    $('#placeholder_bank_name_buy').attr('placeholder', name_bank_buy);
    $('#placeholder_bank_name_sell').attr('placeholder', name_bank_sell);
    // скрипт cleave.js библиотеки для работы с формой(для ввода номера кредитной карты)
    // https://nosir.github.io/cleave.js/
    // https://jsfiddle.net/nosir/aLnhdf3z/
    var cleave_buy = new Cleave('.input-element-buy', {
    creditCard: true,
    //delimiter: '-', // разделитель
    //creditCardStrictMode: true, // Расширить использование 19-значных PAN для поддерживаемых кредитных карт
    onCreditCardTypeChanged: function (type) {
        document.querySelector('.type-buy').innerHTML = type; // отображаем тип карты
    }
    });
    var cleave_sell = new Cleave('.input-element-sell', {
    creditCard: true,
    onCreditCardTypeChanged: function (type) {
        document.querySelector('.type-sell').innerHTML = type; // отображаем тип карты
    }
    });
})


// при выборе select(Отдаете) меняем наименование в placeholder
function Placeholder_name_bank_buy(event) {
    var placeholder_bank_buy = 'Карта ' + this.options[this.selectedIndex].value; // получаем наименование банка из select
    $('#placeholder_bank_name_buy').attr('placeholder', placeholder_bank_buy); // отображаем значение placeholder

}

// при выборе select(Получаете) меняем наименование в placeholder
function Placeholder_name_bank_sell(event) {
    var placeholder_bank_sell = 'Карта ' + this.options[this.selectedIndex].value; // получаем наименование банка из select
    $('#placeholder_bank_name_sell').attr('placeholder', placeholder_bank_sell); // отображаем значение placeholder

}