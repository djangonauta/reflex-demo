import reflex as rx

from ..models import Produto
from .index_state import IndexState


def form_produto():
    return rx.form.root(
        rx.vstack(
            rx.input(
                name="id",
                type="hidden",
                value=IndexState.id,
                on_change=IndexState.set_id,
                display="none",
            ),
            rx.input(
                id="nome_produto",
                name="nome",
                placeholder="Nome do produto",
                required=True,
                auto_focus=True,
                value=IndexState.nome,
                on_change=IndexState.set_nome,
            ),
            rx.input(
                name="preco",
                placeholder="Preço do produto",
                type="number",
                step="0.01",
                required=True,
                value=IndexState.preco,
                on_change=IndexState.set_preco,
            ),
            rx.hstack(
                rx.button(
                    rx.spinner(loading=IndexState.carregando),
                    rx.icon("save", size=15),
                    rx.cond(
                        IndexState.id != 0,
                        rx.text("Atualizar produto"),
                        rx.text("Cadastrar produto"),
                    ),
                    cursor="pointer",
                    disabled=IndexState.carregando,
                ),
                rx.button(
                    rx.icon("eraser", size=15),
                    rx.text("Limpar produto"),
                    type="button",
                    cursor="pointer",
                    on_click=IndexState.limpar_produto,
                ),
            ),
        ),
        on_submit=IndexState.adicionar_produto,
    )


def botao_remover_produto(produto: Produto):
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(rx.icon("circle-x", size=15), cursor="pointer"),
        ),
        rx.alert_dialog.content(
            rx.vstack(
                rx.alert_dialog.title("Remover produto"),
                rx.alert_dialog.description("Confirma exclusão desse produto?"),
                rx.hstack(
                    rx.alert_dialog.cancel(
                        rx.button(rx.icon("circle-x"), rx.text("Cancelar"), cursor="pointer")
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            rx.icon("circle-check", size=15),
                            rx.text("Remover"),
                            on_click=lambda: IndexState.remover_produto(produto),
                            cursor="pointer",
                        )
                    ),
                ),
            )
        ),
    )


def botao_editar_produto(produto: Produto):
    return rx.button(
        rx.icon("pencil", size=15),
        rx.text("Editar"),
        on_click=lambda: IndexState.editar_produto(produto),
        cursor="pointer",
    )


def produto_linha(produto: Produto):
    return rx.table.row(
        rx.table.cell(produto.id),
        rx.table.cell(produto.nome),
        rx.table.cell(produto.preco),
        rx.table.cell(
            rx.hstack(
                botao_remover_produto(produto),
                botao_editar_produto(produto),
            )
        ),
    )


def tabela_produtos():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nome"),
                rx.table.column_header_cell("Preço"),
                rx.table.column_header_cell("Ações"),
            ),
        ),
        rx.table.body(rx.foreach(IndexState.produtos, produto_linha)),
    )


@rx.page("/", "Aplicação teste reflex", on_load=IndexState.carregar_produtos)
def index():
    return rx.container(
        rx.color_mode.button(position="top-left"),
        rx.vstack(
            rx.heading("Produtos", size="8"),
            form_produto(),
            rx.spinner(tabela_produtos(), size="3", loading=IndexState.carregando),
            rx.link("Outra página", href="/github", title="Via react-router"),
            justify="center",
            min_height="85vh",
        ),
    )
