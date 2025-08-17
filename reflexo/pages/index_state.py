import asyncio
from typing import List

import reflex as rx

from ..models import Produto


class IndexState(rx.State):
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
