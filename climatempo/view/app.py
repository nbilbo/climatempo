# python
import json
import tkinter as tk
from tkinter import messagebox
import typing
import os

# 3rd
import ttkbootstrap as ttk

# local
from climatempo import configuracoes
from climatempo import excecoes
from climatempo import raspagem


class App(tk.Tk):
    titulo = 'Clima Tempo'
    geometria = '500x500'
    tema = 'classic'
    fonte = ('Arial', 16, 'bold')

    def __init__(self, *args, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)
        self.geometry(self.geometria)
        self.title(self.titulo)

        # widgets
        self.selecionar_estado = SelecionarEstado(self)
        self.selecionar_cidade = SelecionarCidade(self)
        self.clima = Clima(self)
        self.selecionar_estado.pack(side='top', fill='x')
        self.selecionar_cidade.pack(side='left', fill='both', expand=True)
        self.clima.pack(side='left', fill='both', expand=True)

        self.resetar_clima()
        self.buscar_cidades()

        # binds e comandos
        self.selecionar_estado.btn_pesquisar.config(
            command=self.buscar_cidades
        )
        self.selecionar_cidade.btn_pesquisar.config(command=self.pesquisar)

    def resetar_clima(self) -> None:
        """Resetar os outputs referentes ao clima."""
        self.clima.desempacotar()
        self.clima.label_cidade.config(text='')
        self.clima.label_desc.config(text='')
        self.clima.label_nascer.config(text='')
        self.clima.label_por.config(text='')
        self.clima.label_temp.config(text='')

    def buscar_cidades(self) -> None:
        """
        Atualizar a lista de cidades apartir
        do estado atualmente selecionado.
        """
        treeview = self.selecionar_cidade.treeview
        treeview.delete(*treeview.get_children())
        cidades = self.selecionar_estado.cidades()
        for cidade in cidades:
            treeview.insert('', 'end', text=cidade)

    def pesquisar(self) -> None:
        """
        Apartir da cidade selecionada, buscar pelas informacoes
        de clima.
        """
        try:
            treeview = self.selecionar_cidade.treeview
            selecoes = treeview.selection()
            if selecoes:
                selecao = selecoes[0]
                cidade = treeview.item(selecao)['text']
                estado = self.selecionar_estado.sigla()
                pesquisa = raspagem.pesquisar(cidade, estado)
                cidade_estado = pesquisa['nome']
                descricao = pesquisa['descricao']
                nascer = pesquisa['nascer']
                por = pesquisa['por']
                temperatura = pesquisa['temperatura']

                self.clima.label_cidade.config(text=cidade_estado)
                self.clima.label_nascer.config(text=nascer)
                self.clima.label_por.config(text=por)
                self.clima.label_temp.config(text=temperatura)
                self.clima.label_desc.config(text=descricao)
                self.clima.empacotar()

        except excecoes.CidadeNaoEncontrada:
            self.resetar_clima()
            messagebox.showinfo(
                'Aviso', f'Não conseguimos localizar a cidade "{cidade}"'
            )

        except Exception as error:
            self.resetar_clima()
            messagebox.showinfo('Aviso', str(error))


class SelecionarEstado(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super(SelecionarEstado, self).__init__(*args, **kwargs)
        self.config(padding=configuracoes.PADDING)

        with open(configuracoes.ESTADOS_PATH, 'r') as fp:
            self.estados: typing.Dict = json.loads(fp.read())

        nomes_estados = list(self.estados.keys())
        self.string_estados = tk.StringVar()
        self.combo_estados = ttk.Combobox(
            self, textvariable=self.string_estados
        )
        self.combo_estados.config(values=nomes_estados)
        self.string_estados.set(nomes_estados[0])
        self.btn_pesquisar = ttk.Button(self, text='Buscar cidades')
        label = ttk.Label(self, text='Estados')

        label.pack(side='top')
        self.combo_estados.pack(side='top', pady=configuracoes.PADDING)
        self.btn_pesquisar.pack(side='top', anchor='center')

    def cidades(self) -> typing.Optional[typing.List[str]]:
        estado_atual = self.string_estados.get()
        if self.estados.get(estado_atual):
            return self.estados[estado_atual]['cidades']

        return []

    def sigla(self) -> str:
        estado_atual = self.string_estados.get()

        return self.estados.get(estado_atual)['sigla']


class SelecionarCidade(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super(SelecionarCidade, self).__init__(*args, **kwargs)
        self.config(padding=configuracoes.PADDING)
        self.pack_propagate(False)

        self.treeview = ttk.Treeview(self)
        self.scrollbar = ttk.Scrollbar(self)
        self.btn_pesquisar = ttk.Button(self, text='Pesquisar')

        self.treeview.heading('#0', text='Cidades')
        self.treeview.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.treeview.yview)

        self.btn_pesquisar.pack(side='bottom', fill='x')
        self.scrollbar.pack(side='right', fill='y')
        self.treeview.pack(side='right', fill='both', expand=True)


class Clima(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super(Clima, self).__init__(*args, **kwargs)
        self.config(padding=configuracoes.PADDING)
        self.pack_propagate(False)

        self.brazil_img = tk.PhotoImage(
            file=os.path.join(configuracoes.IMGS_DIR, 'brazil.png')
        )
        self.label_cidade = ttk.Label(
            self, anchor='center', image=self.brazil_img, compound='left'
        )

        self.sunrise_img = tk.PhotoImage(
            file=os.path.join(configuracoes.IMGS_DIR, 'sunrise.png')
        )
        self.label_nascer = ttk.Label(
            self, anchor='center', image=self.sunrise_img, compound='left'
        )

        self.sunset_img = tk.PhotoImage(
            file=os.path.join(configuracoes.IMGS_DIR, 'sunset.png')
        )
        self.label_por = ttk.Label(
            self, anchor='center', image=self.sunset_img, compound='left'
        )

        self.temp_img = tk.PhotoImage(
            file=os.path.join(configuracoes.IMGS_DIR, 'temp.png')
        )
        self.label_temp = ttk.Label(
            self, anchor='center', image=self.temp_img, compound='left'
        )

        self.label_desc = ttk.Label(self, anchor='center')

    def desempacotar(self) -> None:
        for label in (
            self.label_cidade,
            self.label_nascer,
            self.label_por,
            self.label_temp,
            self.label_desc,
        ):
            label.pack_forget()

    def empacotar(self) -> None:
        for label in (
            self.label_cidade,
            self.label_nascer,
            self.label_por,
            self.label_temp,
            self.label_desc,
        ):
            label.pack(side='top', fill='x', expand=True, pady=5)
