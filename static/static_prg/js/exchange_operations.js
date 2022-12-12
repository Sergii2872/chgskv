// скрипт таблицы datatables.net
// orders_table это id нашей таблицы в exchange_operations.html
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
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                }
                        },
                        {   extend: 'csv', exportOptions: {
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                }
                        },
                        {   extend: 'excel', exportOptions: {
                                columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                }
                        },
                        {   extend: 'pdf', exportOptions: {
                                columns: [1, 3, 4, 6, 7, 13],
                                }
                        },
                        {
                            extend: 'print',
                            text: 'Печать',
                            titleAttr: 'Печать таблицы',
                            title: 'Все Заявки(операции) клиентов',
                            autoPrint: true,
                            exportOptions: {
                                columns: ':visible',
                                columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
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
                    //fixedColumns:   {
                    //    left: 2,
                    //    right: 1
                    //},
                    'columnDefs': [
                    {//'targets': [15],  // отключение колонки сортировки
                     'searchable': false,
                     'orderable': false
                    }]

                }
        );

});