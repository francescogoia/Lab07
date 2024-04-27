import copy
import datetime

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        situazioni = MeteoDao.get_all_situazioni()
        self._diz_situazioni = {}
        self._set_situazioni = set()
        self.popola_situazioni()
        self.N_ricorsioni = 0
        self._soluzioni = []
        self.N_soluzioni = 0
    def popola_situazioni(self):
        situazioni = MeteoDao.get_all_situazioni()
        for s in situazioni:
            if self._diz_situazioni.get(s.localita) is None:
                self._diz_situazioni[s.localita] = []
            self._diz_situazioni[s.localita].append(s)
            self._set_situazioni.add(s)
        #print(self._diz_situazioni)
        #print(self._set_situazioni)

    def umidita_media(self, mese):
        risultato = []
        for citta in self._diz_situazioni.keys():
            umidita_tot = 0
            num_misurazioni = 0
            for s in self._diz_situazioni[citta]:
                if mese is not None and s.get_mese() == mese:
                    umidita_tot += s.umidita
                    num_misurazioni += 1
                else:
                    umidita_tot += s.umidita
                    num_misurazioni += 1
            umidita_media_citta = umidita_tot / num_misurazioni
            risultato.append((citta, umidita_media_citta))
        #print(risultato)
        return risultato



    def sequenza_ricorsione(self, giorno, mese):
        if giorno == 1:
            costi = {}
            for c in self._diz_situazioni.keys():
                costi[c] = 0
                for s in self._diz_situazioni[c]:
                    if s.data.month == mese:
                        costi[c] += s.umidita
          #  print(costi)
          #  print(min(costi.items(), key=lambda x : x[1]))
            return min(costi.items(), key=lambda x : x[1])
        else:
            for c in self._diz_situazioni.keys():
                return self.sequenza_ricorsione(giorno - 1, mese)


    def ricorsione(self, mese, giorno, parziale):
        self.N_ricorsioni += 1
        if len(parziale) == 15 :
            risultato = self.aggiungi_costi(parziale)
            #print(risultato)
            self._soluzioni.append(copy.deepcopy(risultato))
            self.N_soluzioni += 1

        else:
            for situa in self._set_situazioni:
                if situa.get_mese() == mese and situa.data.day == giorno:
                    parziale.append((situa.localita, situa.data, situa.umidita))
                    if self.citta_ammissibile(parziale) == True:
                        self.ricorsione(mese, giorno +1, parziale)
                    parziale.pop()


    def aggiungi_costi(self, parziale):               # parziale è una lista di tuple (localita, data, umidita)
        costo_tot = 0
        for i in range(len(parziale)):
            costo_var = parziale[i][2]
            costo_maggiorato = 0
            if i <= 1:
                costo_maggiorato = 0
            else:
                if parziale[i][0] != parziale[i - 1][0] or parziale[i - 1][0] != parziale[i - 2][0]:
                    costo_maggiorato = 100
            costi = costo_var + costo_maggiorato
            costo_tot += costi

        return costo_tot, parziale


    def citta_ammissibile(self, parziale):
        diz_citta = {}
        for i in range(len(parziale)):
            diz_citta[parziale[i][0]] = 0
        for i in range(len(parziale)):
            diz_citta[parziale[i][0]] += 1
            if diz_citta[parziale[i][0]] > 6:
                return False
        giorni_consecutivi = False
        if len(parziale) == 1:
            giorni_consecutivi = True
        elif len(parziale) == 2 and parziale[0][0] == parziale[1][0]:
            giorni_consecutivi = True
        elif len(parziale) == 3 and parziale[0][0] == parziale[1][0] and parziale[1][0] == parziale[2][0]:
            giorni_consecutivi = True
        elif len(parziale) > 3:
            i = len(parziale) - 1
            if parziale[i - 1][0] == parziale[i - 2][0] and parziale[i - 2][0] == parziale[i - 3][0]:       # i 3 precedenti sono uguali (può cambiare città)
                giorni_consecutivi = True
            elif parziale[i][0] == parziale[i - 1][0] and parziale[i - 1][0] == parziale[i - 2][0]:         # uguale ai due precedenti
                giorni_consecutivi = True
            elif parziale[i][0] == parziale[i - 1][0]:                                                      # uguale al precedente
                giorni_consecutivi = True
        return giorni_consecutivi


    def soluzione_migliore(self):
        soluzioni = self._soluzioni
        minimo = min(soluzioni, key=lambda x : x[0])
        print(minimo)
        return minimo
