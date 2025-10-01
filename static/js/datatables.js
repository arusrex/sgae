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
                    extend: 'print',
                    text: 'Imprimir',
                    exportOptions: {
                        columns: ':not(.no-print)'
                    },

                    customize: async function (window) {
                        const agora = new Date();
                        const dataHora = agora.toLocaleDateString('pt-BR');

                        const response = await fetch(`/sistema/dados_sistema_json/`);
                        const dados = await response.json();

                        const nomeSistema = dados.sistema_nome;
                        const userSitema = dados.sistema_user;
                        const logoEscola = "/static/assets/img/carimbo.png";
                        const logoJahu = "/static/assets/img/jahu.png";
                        const logoEducacao = "/static/assets/img/educacao.png";

                        let style = window.document.createElement('style');
                        style.type = 'text/css';
                        style.innerHTML = `
                            @media print {
                                header {
                                    width: 100%;
                                }
                                footer {
                                    width: 100%;
                                    padding: 5px;
                                }

                                footer small {
                                    font-size: 10px;
                                }
                            }
                        `;
                        window.document.head.appendChild(style);

                        const body = window.document.body;

                        const top = document.createElement('header');
                        top.innerHTML = `<div class="d-flex flex-row gap-3 align-items-center">
                                            <img src="${logoEscola}" width="60" height="60" class="img-fluid"><br>
                                            <h3>${nomeSistema}</h3>
                                        </div>`

                        body.insertBefore(
                            top,
                            body.firstChild
                        );
                        const bottom = document.createElement('footer')
                        bottom.innerHTML = `<div class="d-flex gap-2 align-items-center">
                                                <img src="${logoJahu}" width="30" height="30" class="img-fluid"><br>
                                                <img src="${logoEducacao}" width="30" height="30" class="img-fluid"><br>
                                                <div><small>Gerado em ${dataHora} por ${userSitema} - SGAE / Sistema de Gestão Administrativo Escolar por JEF Nº 12435</small></div>
                                            </div>`
                        body.appendChild(
                            bottom
                        );
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
