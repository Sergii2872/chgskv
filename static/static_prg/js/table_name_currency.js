// Скрипт отрисовки таблицы плагина datatables.net для таблицы БД наименования валют Name_Currency, подключен в blok2/name_currency.html
// Пример кода взял https://github.com/twtrubiks/DRF-dataTable-Example-server-side
// видео примера https://www.youtube.com/watch?v=E0Pf5Ci-vGw
// методом ajax обмениваемся данными с функцией list класса NameCurrency_ViewSet в blok2/views.py
// вызов по роутеру в chgskv/urls.py
let table = $('#datatables').DataTable({
    dom: 'lfBrtip', // параметры расположения для show entris и search
    // задаем параметры расположения кнопок и названия в show entris https://www.datatables.net/forums/discussion/56362/buttons-and-show-entries#Comment_152110
    lengthMenu: [
    [ 10, 25, 50, 100 ],
    [ '10 Записей', '25 Записей', '50 Записей', '100 Записей' ]
    ],
    select: true, // выбор по клику строки или несколько строк
    buttons: [

        {   extend: 'copy', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // выбор столбцов для скрина таблицы
                }
        },
        {   extend: 'csv', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // выбор столбцов для csv файла
                }
        },
        {   extend: 'excel', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // выбор столбцов для excel файла
                }
        },
        {   extend: 'pdf', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // выбор столбцов для pdf файла
                }
        },
        {
            extend: 'print',
            text: 'Печать', // наименование кнопки
            titleAttr: 'Печать таблицы', // подсказка при наведении
            title: 'Справочник наименования валют', // заголовок печати, если не задаем то печатает title html страницы
            autoPrint: true, // false - отключение всплывающего окна печати
            exportOptions: {
                //columns: ':visible',
                columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // выбор столбцов для печати
            },
            //text: '<i class="fa fa-print fa-lg text-success"></i>',
            //message: 'REPORT NAME' , // текст в отчете
            customize: function (win) {
                $(win.document.body).find('table').addClass('display').css('font-size', '9px');
                $(win.document.body).find('tr:nth-child(odd) td').each(function(index){
                    $(this).css('background-color','#D0D0D0');
                });
                $(win.document.body).find('h1').css('text-align','center'); // заголовок по центру
            }
        }

    ],
    //"dom": '<"top"i>rt<"bottom"flp><"clear">',
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/Name_Currency/",
        "type": "GET"
    },
    "columns": [
        {"data": "id"}, // пустая колонка для chekbox
        {"data": "id"},
        {"data": "market_exchange.market", "defaultContent": "не задан"},
        {"data": "id_market"},
        {"data": "currency"},
        {"data": "symbol"},
        // отображаем саму картинку
        //https://www.codeproject.com/Questions/5272942/How-do-I-display-binary-image-in-jquery-datatable
        {
        "data": "image_currency", "name": "Иконка",
        "render": function (data, type, row, meta) {
            var imgsrc = data;
            return '<img class="img-responsive" src="' + imgsrc +'"height="30px" width="30px"/>';}
        },
        {"data": "wallet"},
        {"data": "is_active"},
        {"data": "created"},
        {"data": "updated"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-info">Изменить</button>' + '&nbsp;&nbsp' +
            '<button type="button" class="btn btn-danger">Удалить</button>'
        }
    ],

    // для chekbox https://www.gyrocode.com/articles/jquery-datatables-how-to-add-a-checkbox-column/
    'columnDefs': [
        {'targets': 0,
         'searchable': false,
         'orderable': false,
         'className': 'dt-body-center',
         'render': function (data, type, full, meta){
             return '<input type="checkbox" name="id[]" value="' + $('<div/>').text(data).html() + '">';
        }},
        {'targets': [11],  // поля отключена сортировка [P1,...,Pn]
         'searchable': false,
         'orderable': false
        }],

      'order': [[1, 'asc']],  //столбец к которому применяется сортировка, определен в ORDER_COLUMN_CHOICES_PricesCurrency blok2/models.py
      scrollY:        "300px",
      scrollX:        true,
      scrollCollapse: true,
      paging:         true,
      fixedColumns:   {
           left: 2,
           right: 1
      }

});

let id = 0;

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    console.log(data);
    var imagenUrl = data.image_currency;
    console.log(imagenUrl);
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
        // EDIT button
        $('#market_exchange_id').val(data['market_exchange']['id']);
        //$('#market_exchange_id').val('0');
        $('#id_market').val(data['id_market']);
        $('#currency').val(data['currency']);
        $('#symbol').val(data['symbol']);
        //$('.dropify').dropify(); // инициализация по class="dropify" скрипт для выбора и предпросмотра картинки dropify.js подключаем в base.html
        // инициализация с изменением картинки по class="dropify" скрипт для выбора и предпросмотра картинки dropify.js подключаем в base.html
        var drEvent = $('.dropify').dropify(
            {
              defaultFile: imagenUrl
            });
        drEvent = drEvent.data('dropify');
        drEvent.resetPreview();
        drEvent.clearElement();
        drEvent.settings.defaultFile = imagenUrl;
        drEvent.destroy();
        drEvent.init();
        //$('#image_currency').val();
        //$('img').hide();
        //$("#image_currency").html("");
        //$("#blah-edit").append('<img class="img-responsive" src="' + objData +'"height="100px" width="100px"/>')
        $('#wallet').val(data['wallet']);
        $('#is_active').val('1');
        $('#type').val('edit');
        $('#modal_title').text('ИЗМЕНИТЬ');
        $("#myModal").modal();
    } else {
        // DELETE button
        $('#modal_title').text('УДАЛИТЬ');
        $("#confirm").modal();
    }

    id = data['id'];

});


// https://stackoverflow.com/questions/6150289/how-can-i-convert-an-image-into-base64-string-using-javascript
// https://askdev.ru/q/kak-preobrazovat-izobrazhenie-v-stroku-base64-s-pomoschyu-javascript-3395/
// функция кодировки файла изображения в base64, вызывается из input name_currency.html
function encodeImageFileAsURL() {

    var filesSelected = document.getElementById("image_currency").files;
    if (filesSelected.length > 0) {
      var fileToLoad = filesSelected[0];
      var fileReader = new FileReader();

        fileReader.onload = function(fileLoadedEvent) {

            var srcData = fileLoadedEvent.target.result; // <--- data: base64
            console.log("Converted Base64 version is " + srcData);
            $("#b64").val(srcData);

            //var names = $.map(filesSelected, function(val) { return val.name; }); // получаем имя файла из FileList object
            //console.log(names[0]);
            //$("#blah-edit").append('<img class="img-responsive" src="/media/image_currency/' + names[0] +'"height="100px" width="100px"/>')

            //document.getElementById('blah').src = srcData;  // предпросмотр картинки
      }
      fileReader.readAsDataURL(fileToLoad);

    }
  }


$('#token').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    var dataBase64 = encodeURIComponent($('#b64').val());
    console.log('RESULT:', dataBase64);
    data = $this.serialize() + '&image_currency=' + dataBase64;
    console.log('Data:', data);
    let type = $('#type').val();
    let method = '';
    let url = '/api/Name_Currency/';
    var csrf_token = $('#token [name="csrfmiddlewaretoken"]').val();
    if (type == 'new') {
        // new
        method = 'POST';
        // если файл картинки не загружен, то считываем файл noimage.png
        if (dataBase64 == '') {

        }

    } else {
        // edit
        url = url + id + '/';
        method = 'PUT';
    }
    $.ajax({
        url: url,
        method: method,
        headers:{"X-CSRFToken": csrf_token},
        data: data
    }).success(function (data, textStatus, jqXHR) {
        location.reload();
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });

});

$('#confirm').on('click', '#delete', function (e) {
    var csrf_token = $('#token [name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/api/Name_Currency/' + id + '/',
        headers:{"X-CSRFToken": csrf_token},
        method: 'DELETE'
    }).success(function (data, textStatus, jqXHR) {
        location.reload();
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});


$('#new').on('click', function (e) {
    $('#market_exchange_id').val('1');
    $('#id_market').val('');
    $('#currency').val('');
    $('#symbol').val('');
    $("#blah-edit").html("");
    //$('#image_currency').val();
    //$('.dropify').dropify(); // инициализация по class="dropify" скрипт для выбора и предпросмотра картинки dropify.js подключаем в base.html
    // инициализация с изменением картинки по class="dropify" скрипт для выбора и предпросмотра картинки dropify.js подключаем в base.html
    var imagenUrl = '/media/image_currency/noimage.png';
    var drEvent = $('.dropify').dropify(
            {
              defaultFile: imagenUrl
            });
        drEvent = drEvent.data('dropify');
        drEvent.resetPreview();
        drEvent.clearElement();
        drEvent.settings.defaultFile = imagenUrl;
        drEvent.destroy();
        drEvent.init();
    $('#wallet').val('');
    $('#is_active').val('1');
    $('#type').val('new');
    $('#modal_title').text('НОВАЯ ЗАПИСЬ');
    $("#myModal").modal();
});


// для столбца chekbox https://www.gyrocode.com/articles/jquery-datatables-how-to-add-a-checkbox-column/
// Handle click on "Select all" control
   $('#example-select-all').on('click', function(){
      // Get all rows with search applied
      var rows = table.rows({ 'search': 'applied' }).nodes();
      // Check/uncheck checkboxes for all rows in the table
      $('input[type="checkbox"]', rows).prop('checked', this.checked);
   });

   // Handle click on checkbox to set state of "Select all" control
   $('#datatables tbody').on('change', 'input[type="checkbox"]', function(){
      // If checkbox is not checked
      if(!this.checked){
         var el = $('#example-select-all').get(0);
         // If "Select all" control is checked and has 'indeterminate' property
         if(el && el.checked && ('indeterminate' in el)){
            // Set visual state of "Select all" control
            // as 'indeterminate'
            el.indeterminate = true;
         }

      }

   });

// Handle form submission event
$('#frm-datatables').on('submit', function(e){
    e.preventDefault();
    //if (confirm("Вы уверенны!") == true) {
  $.confirm({
    title: 'Внимание!',
    content: 'Удаление группы записей! Будут удалены все записи в справочниках связанные с этой валютой !!!',
    type: 'red',
    buttons: {
        confirm: {
        text: 'Удалить',
        btnClass: 'btn-red',
        action: function () {

            var form = this;

          // Iterate over all checkboxes in the table
          table.$('input[type="checkbox"]').each(function(){
             // If checkbox doesn't exist in DOM
             if(!$.contains(document, this)){
                // If checkbox is checked
                if(this.checked){
                   // Create a hidden element
                   $(form).append(
                      $('<input>')
                         .attr('type', 'hidden')
                         .attr('name', this.name)
                         .val(this.value)
                   );

                }
             }
          });

          // Output form data to a console
          //$('#chekbox').text($(form).serialize()); // текст для name_currency.html
          //console.log("Данные формы на сервер", $(form).serialize()); // получаем данные формы
          // получаем список словарей значений поля checkbox(datatable "columns": {"data": "id"}) таблицы формы
          var data = table.$('input[type="checkbox"]').serializeArray();
          //console.log("Data", data);
          //var id = data[0].value; // значение первого словаря из списка словарей
          //console.log("Id", id);
          var id = [];
          // получаем список значений словарей переменной data
          $(data).each(function(i, field){
            id.push(field.value); // добавляем в список значение
            });
          //console.log("Список Id на удаление", id);
          var url = [];
          $(id).each(function(i){
                url.push('/api/Name_Currency/' + id[i] + '/');
                });
          //console.log("Список url на удаление", url);
          var csrf_token = $('#token [name="csrfmiddlewaretoken"]').val();
          // удаляем по выбору chekbox группу записей
          $(url).each(function(i){
                //console.log(url[i]);
                $.ajax({
                //url: ['/api/Name_Currency/' + id + '/'],
                url: url[i],
                headers:{"X-CSRFToken": csrf_token},
                method: 'DELETE'
            }).success(function (data, textStatus, jqXHR) {
                //console.log("Ok")
                location.reload();
            }).error(function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR)
            });
                });

          //location.reload();
          // Prevent actual form submission
          e.preventDefault();

        }},
        cancel: {
        text: 'Отменить',
        btnClass: 'btn-blue',
        action: function () {
           e.preventDefault();
           $.alert('Удаление отменено!');

        }}
    }
  });

});

/*    // https://www.cyberforum.ru/javascript-jquery/thread1917032.html
    $('#datatables tbody').on('click', 'tr', function () {
        $(this).toggleClass('selected');
    });

    $('#button').click(function () {
        var ids = $.map(table.rows('.selected').data(), function (item) {
            return item[0]
        });
        console.log(ids)
        alert(table.rows('.selected').data().length + ' row(s) selected');
    });
*/

/*$('#prn').on('click', function (e) {
    var csrf_token = $('#token [name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "{% url 'Print_pdf' %}",
        headers:{"X-CSRFToken": csrf_token},
        method: 'POST',
        cache: true, /* кеширование*/
/*        success: function (data) {
            console.log("OK"); /* отображение в консоли броузера для проверки */
/*            console.log(data); /* отображение в консоли логина пользователя */
/*            },
            error: function(){
                console.log("error")
            }

    });
});
*/

/*
// функция вызывается из blok2/templates/report1.html
// не использую для таблиц плагина datatables, т.к. в нём есть функция печати
function callPrint() {
    var printCSS = '<link rel="stylesheet" href="css/print.css" type="text/css" />';
    var printTitle = document.getElementById('print-title').innerHTML;
    var printTable = document.getElementById('print-tables').innerHTML;
    //var printImg = document.getElementById('print-img').innerHTML;
    //var printText = document.getElementById('print-text').innerHTML;
    var windowPrint = window.open('','','left=50,top=50,width=800,height=640,toolbar=0,scrollbars=1,status=0');
    windowPrint.document.write(printCSS);
    windowPrint.document.write(printTitle);
    windowPrint.document.write(printTable);
    //windowPrint.document.write(printImg);
    //windowPrint.document.write(printText);
    windowPrint.document.close();
    windowPrint.focus();
    windowPrint.print();
    windowPrint.close();
}
*/