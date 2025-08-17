import reflex as rx


class Produto(rx.Model, table=True):
    nome: str
    preco: float

    def __str__(self):
        return f"{self.nome}, R$ {self.preco}"
