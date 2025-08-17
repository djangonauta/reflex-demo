import asyncio
from typing import List

import reflex as rx

from .github import github
from .models import Produto


class State(rx.State):
    carregando: bool = False
    id: int = 0
    nome: str = ""
    preco: float = 0.0
    produtos: List[Produto] = []

    def init_produto(self):
        self.id = 0
        self.nome = ""
        self.preco = 0.0

    @rx.event
    def set_id(self, id):
        self.id = id

    @rx.event
    def set_nome(self, nome):
        self.nome = nome

    @rx.event
    def set_preco(self, preco):
        self.preco = float(preco)

    @rx.event(background=True)
    async def adicionar_produto(self, form_data: dict):
        async with rx.asession() as s:
            async with self:
                try:
                    self.carregando = True
                    yield
                    await asyncio.sleep(1)

                    if self.id != 0:
                        stmt = Produto.select().where(Produto.id == self.id)
                        produto = (await s.exec(stmt)).one()
                        produto.nome = self.nome
                        produto.preco = self.preco

                    else:
                        del form_data["id"]
                        produto = Produto(**form_data)

                    s.add(produto)
                    await s.commit()

                    msg = "atualizado" if self.id else "cadastrado"
                    msg = f"Produto {produto} {msg} com sucesso!"
                    yield rx.toast(msg, position="top-center")

                    if self.id != 0:
                        self.produtos = [
                            produto if p.id == produto.id else p for p in self.produtos
                        ]

                    else:
                        self.produtos.append(produto)

                    self.init_produto()
                    yield rx.set_focus("nome_produto")

                except Exception as e:
                    print(e)

                finally:
                    self.carregando = False

    @rx.event(background=True)
    async def remover_produto(self, produto):
        async with rx.asession() as s:
            async with self:
                try:
                    self.carregando = True
                    yield

                    await asyncio.sleep(1)
                    stmt = Produto.select().where(Produto.id == produto["id"])
                    produto = (await s.exec(stmt)).one()
                    await s.delete(produto)
                    await s.commit()

                    self.produtos.remove(produto)
                    yield rx.toast(f"Produto {produto} removido com sucesso", position="top-center")
                    yield rx.set_focus("nome_produto")

                except Exception as e:
                    print(e)

                finally:
                    self.carregando = False

    @rx.event(background=True)
    async def carregar_produtos(self):
        async with rx.asession() as s:
            async with self:
                self.carregando = True
                self.init_produto()
                yield

                await asyncio.sleep(1)
                try:
                    stmt = Produto.select().order_by(Produto.id)  # type: ignore
                    resultado = await s.exec(stmt)
                    self.produtos = list(resultado.all())

                except Exception as e:
                    print(e)

                finally:
                    self.carregando = False

    @rx.event
    def editar_produto(self, produto: Produto):
        self.set_id(produto.id)
        self.set_nome(produto.nome)
        self.set_preco(produto.preco)

    @rx.event(background=True)
    async def limpar_produto(self):
        async with self:
            self.init_produto()


def form_produto():
    return rx.form.root(
        rx.vstack(
            rx.input(
                name="id",
                type="hidden",
                value=State.id,
                on_change=State.set_id,
                display="none",
            ),
            rx.input(
                id="nome_produto",
                name="nome",
                placeholder="Nome do produto",
                required=True,
                auto_focus=True,
                value=State.nome,
                on_change=State.set_nome,
            ),
            rx.input(
                name="preco",
                placeholder="Preço do produto",
                type="number",
                step="0.01",
                required=True,
                value=State.preco,
                on_change=State.set_preco,
            ),
            rx.hstack(
                rx.button(
                    rx.spinner(loading=State.carregando),
                    rx.icon("save", size=15),
                    rx.cond(
                        State.id != 0, rx.text("Atualizar produto"), rx.text("Cadastrar produto")
                    ),
                    cursor="pointer",
                    disabled=State.carregando,
                ),
                rx.button(
                    rx.icon("eraser", size=15),
                    rx.text("Limpar produto"),
                    type="button",
                    cursor="pointer",
                    on_click=State.limpar_produto,
                ),
            ),
        ),
        on_submit=State.adicionar_produto,
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
                            on_click=lambda: State.remover_produto(produto),
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
        on_click=lambda: State.editar_produto(produto),
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
        rx.table.body(rx.foreach(State.produtos, produto_linha)),
    )


def index():
    return rx.container(
        rx.color_mode.button(position="top-left"),
        rx.vstack(
            rx.heading("Produtos", size="8"),
            form_produto(),
            rx.spinner(tabela_produtos(), size="3", loading=State.carregando),
            rx.link("Outra página", href="/github", title="Via react-router"),
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index, "/", title="Aplicação teste Reflex", on_load=State.carregar_produtos)
app.add_page(github, "/github", title="Profile github")
