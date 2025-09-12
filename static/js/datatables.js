window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    // const datatablesSimple = document.getElementById('datatablesSimple');
    // if (datatablesSimple) {
    //     new simpleDatatables.DataTable(datatablesSimple);
    // }

    let table = new DataTable('#datatablesSimple', {
        language: {
            url:'https://cdn.datatables.net/plug-ins/1.12.1/i18n/pt-BR.json'
        },
        layout: {
            top2Start: {
                buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
            },
            topStart: 'pageLength',
            topEnd: 'search',
            bottomStart: 'info',
            bottomEnd: 'paging',
        },
    });

    const tabelas = document.querySelectorAll('#datatablesSimple');
    tabelas.forEach(element => {
        element.classList.add('border', 'table', 'table-striped', 'table-hover', 'table-bordered', 'table-sm');
    });
});
