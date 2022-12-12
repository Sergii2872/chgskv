// Скрипт отрисовки таблицы плагина datatables.net для таблицы БД наименования валют Balance_Currency, подключен в blok2/balance_Currency.html
// Пример кода взял https://github.com/twtrubiks/DRF-dataTable-Example-server-side
// Пример кода внешнего фильтра в таблице https://www.datatables.net/examples/plug-ins/range_filtering
// видео примера https://www.youtube.com/watch?v=E0Pf5Ci-vGw
// методом ajax обмениваемся данными с функцией list класса BalanceCurrency_ViewSet в blok2/views.py
// вызов по роутеру в chgskv/urls.py
let table = $('#datatables').DataTable({
    dom: 'lfBrtip', // параметры расположения для show entris и search
    // задаем параметры расположения кнопок и названия в show entris https://www.datatables.net/forums/discussion/56362/buttons-and-show-entries#Comment_152110
    lengthMenu: [
    [ 10, 25, 50, 100 ],
    [ '10 Записей', '25 Записей', '50 Записей', '100 Записей' ]
    ],
    buttons: [

        {   extend: 'copy', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6], // выбор столбцов для скрина таблицы
                }
        },
        {   extend: 'csv', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6], // выбор столбцов для csv файла
                }
        },
        {   extend: 'excel', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6], // выбор столбцов для excel файла
                }
        },
        {   extend: 'pdf', exportOptions: {
                columns: [1, 2, 3, 4, 5, 6], // выбор столбцов для pdf файла
                }
        },
        {
            extend: 'print',
            text: 'Печать', // наименование кнопки
            titleAttr: 'Печать таблицы', // подсказка при наведении
            title: 'Справочник курсов валют', // заголовок печати, если не задаем то печатает title html страницы
            autoPrint: true, // false - отключение всплывающего окна печати
            exportOptions: {
                //columns: ':visible',
                columns: [1, 2, 3, 4, 5, 6], // выбор столбцов для печати
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
    "serching": true,
    "ajax": {
        "url": "/api/Balance_Currency/",
        "type": "GET"
    },
    "columns": [
        {"data": "id"}, // пустая колонка для chekbox
        {"data": "id"},
        {"data": "name_currency.symbol", "defaultContent": "не задан"},  // , "name": "name_currency.id"
        //{"data": "name_currency_id"},
        {"data": "balance_amount"},
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
    'columnDefs': [{
         'targets': 0,
         'searchable': false,
         'orderable': false,
         'className': 'dt-body-center',
         'render': function (data, type, full, meta){
             return '<input type="checkbox" name="id[]" value="' + $('<div/>').text(data).html() + '">';
         }},
        {'targets': [7], // поля отключена сортировка [P1,...,Pn]
         'searchable': false,
         'orderable': false
        }],

      'order': [[1, 'asc']] //столбец к которому применяется сортировка, определен в ORDER_COLUMN_CHOICES_BalanceCurrency blok2/models.py

});

let id = 0;

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
        // EDIT button
        $('#name_currency_id').val(data['name_currency']['id']);
        $('#balance_amount').val(data['balance_amount']);
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

$('#token').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    //alert(JSON.stringify($this.serialize()));
    let type = $('#type').val();
    let method = '';
    let url = '/api/Balance_Currency/';
    var csrf_token = $('#token [name="csrfmiddlewaretoken"]').val();
    console.log(csrf_token);
    console.log(type);
    if (type == 'new') {
        // new
        method = 'POST';
    } else {
        // edit
        url = url + id + '/';
        method = 'PUT';
    }
    $.ajax({
        url: url,
        method: method,
        headers:{"X-CSRFToken": csrf_token},
        data: $this.serialize()
    }).success(function (data, textStatus, jqXHR) {
        //alert(JSON.stringify(data));
        //alert(JSON.stringify(jqXHR));
        location.reload()
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });

});

$('#confirm').on('click', '#delete', function (e) {
    var csrf_token = $('#token [name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/api/Balance_Currency/' + id + '/',
        headers:{"X-CSRFToken": csrf_token},
        method: 'DELETE'
    }).success(function (data, textStatus, jqXHR) {
        location.reload();
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});

// задаем начальные значения модального окна(по id myModal) новой записи или редактирования в blok2/prices_currency.html
$('#new').on('click', function (e) {
    $('#name_currency_id').val('1');
    $('#balance_amount').val('');
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
    content: 'Удаление группы записей!',
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
                url.push('/api/Balance_Currency/' + id[i] + '/');
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