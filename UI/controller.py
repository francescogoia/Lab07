import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        risultato = self._model.umidita_media(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))
        for i in risultato:
            self._view.lst_result.controls.append(ft.Text(f"{i[0]}: {i[1]}"))
            self._view.update_page()


    def handle_sequenza(self, e):
        risultato = self._model.sequenza_ricorsione(3, self._mese)
        pass

    def read_mese(self, e):         ## chiamata on-change
        self._mese = int(e.control.value)

