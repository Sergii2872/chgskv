// Этот скрипт не использую , т.к. вызываю из forms по action в load_poloniex_namecurrency.html функцию Load_Poloniex_Currencies в blok4\views.py
// https://djangowithreactjs.quora.com
// https://www.youtube.com/watch?v=3uYmbbpvJfM пример при загрузке файла
// progress bar для загрузки больших файлов(картинок, видео), здесь не применяю , использую только строку для информирования

/* скрипт для загрузки криптовалют с Poloniex вызывается по class="progressbar" из load_poloniex_namecurrency.html */
$(document).ready(function(){  /* Стандартная обертка, т.е. скрипт выполняется когда загрузится весь html документ */

const progress_bar = document.getElementById('progress') /* Переменной progress_bar присваиваем элемент по id = progress */

$('.progressbar').click(function(e) {
     /* Изменение стандартного выполнения формы - Отмена отправки формы на сервер, где е это переданный параметр (элемент),
     элемент можем назвать как хотим. Делается для того чтобы мы могли считать данные с формы */
        e.preventDefault();
        progress_bar.classList.remove("not-visible"); /* Отменяем стиль , т.е. показываем progress bar в load_poloniex_namecurrency.html */
        var form = $('.upload_form'); /* Принимаем форму(form) по class=upload_form из load_poloniex_namecurrency.html */
        console.log(form); /* Выводим на консоль значения полученной формы */
        var url = form.attr("action");
        console.log(url);
        var csrf_token = $('.upload_form [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        Progressbar_Updating(url, csrf_token)
     });


/* Отправка данных в БД методом ajax */
     function Progressbar_Updating(url, csrf_token){
        var data = {};
        /* csrf_token нужен django чтобы делать post запрос и проверять что запрос пришел именно с нашей страницы а не сторонний */
        data["csrfmiddlewaretoken"] = csrf_token;
        /* url это адрес на который необходимо отправлять post запрос, делаем через атрибут action, кот. работает с префиксами всех языков(англ,рус и т.д.)
        присваивается url адрес который прописан в атрибуте action нашей формы form в файле load_poloniex_namecurrency.html
        т.е. через urls.py по Load_Poloniex_Currencies переходим к функции Load_Poloniex_Currencies в views.py*/
        console.log("Progressbar_Updating");
        console.log(data); /* просмотр в консоли значений переменной data (для проверки)*/
        /* Ajax - это подход к построению интерактивных пользовательских интерфейсов web-приложений,
        разработанный на javaScript, который в фоновом режиме (без перезагрузки всей страницы, как в PHP)
        позволяет обмениваться данными между браузером и сервером.*/
         $.ajax({
             url: url, /* Отправляем массив данных data в обработку функцией Load_Poloniex_Currencies на сервер в views.py */
             type: 'POST', /* определяем что метод post*/
             data: data, /* передаем переменной data значения в views.py, т.е. здесь передает только csrf_token */
             cache: false, /* кеширование*/
             dataType: 'json',
             /*contentType: false,*/
             /*processData: false,*/
             beforeSend: function(){
             },
             xhr:function(){
                 const xhr = new window.XMLHttpRequest();
                 $('#progress').html(' Ожидайте! Идет загрузка валют Poloniex')
                 // код для загрузки файла
                 //const xhr = new window.XMLHttpRequest();
                 //xhr.upload.addEventListener('progress', e=>{
                    //if(e.lengthComputable){
                        //const percentProgress = (e.loaded/e.total)*100;
                        //console.log(percentProgress);
                        //$('#progress').html('<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="' +
                                            //percentProgress + '" aria-valuemin="0" aria-valuemax="100" style="width:' + percentProgress + '%"></div>')
                    //}
                 //});
                 return xhr
             },
             /* если успешный ответ сервера то success иначе error*/
             success: function (response) {
                 console.log("OK"); /* отображение в консоли броузера для проверки */
                 console.log(response);
                 progress_bar.classList.add('not-visible')
             },
             error: function(){
                 console.log("error")
             }
         })

     };


});