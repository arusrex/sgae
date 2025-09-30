window.addEventListener('DOMContentLoaded', event => {

    const tabelas = document.querySelectorAll('#datatablesSimple');
    let numero = 1;
    let buttons = [];
    let info = null;
    let pageLength = null;
    let search = null;
    let paging = null;

    tabelas.forEach(element => {
        element.id = element.id + numero;

        if (!element.classList.contains('sem-botoes')) {
            buttons = [
                {
                    extend: 'copy',
                    text: 'Copiar',
                    exportOptions: {
                        columns: ':not(.no-print)'
                    }
                },
                {
                    extend: 'csv',
                    text: 'Gerar CSV',
                    exportOptions: {
                        columns: ':not(.no-print)'
                    }
                },
                {
                    extend: 'excel',
                    text: 'Gerar Excel',
                    exportOptions: {
                        columns: ':not(.no-print)'
                    }
                },
                {
                    extend: 'pdf',
                    text: 'Gerar PDF',
                    exportOptions: {
                        columns: ':not(.no-print)'
                    }
                },
                {
                    extend: 'print',
                    text: 'Imprimir',
                    exportOptions: {
                        columns: ':not(.no-print)'
                    }
                },
            ];
        } else {
            buttons = [];
        }

        if (!element.classList.contains('sem-info')) {
            info = 'info';
        } else {
            info = null;
        }

        if (!element.classList.contains('sem-qtd-por-paginas')) {
            pageLength = 'pageLength';
        } else {
            infpageLengtho = null;
        }
        
        if (!element.classList.contains('sem-pesquisa')) {
            search = 'search';
        } else {
            search = null;
        }
        
        if (!element.classList.contains('sem-paginacao')) {
            paging = 'paging';
        } else {
            paging = null;
        }



        let table = new DataTable(`#${element.id}`, {
            responsive: true,
            order: [],
            language: {
                url:'https://cdn.datatables.net/plug-ins/1.12.1/i18n/pt-BR.json'
            },
            layout: {
                top2Start: {
                    buttons: buttons,
                },
                topStart: pageLength,
                topEnd: search,
                bottomStart: info,
                bottomEnd: paging,
            },
        });

        element.classList.add('border', 'table', 'table-striped', 'table-hover', 'table-bordered', 'table-sm');
        numero ++;
        
    });
});
