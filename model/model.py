import datetime

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        situazioni = MeteoDao.get_all_situazioni()
        self._diz_situazioni = {}
        self.popola_diz_situazioni()

    def popola_diz_situazioni(self):
        situazioni = MeteoDao.get_all_situazioni()
        for s in situazioni:
            if self._diz_situazioni.get(s.localita) is None:
                self._diz_situazioni[s.localita] = []
            self._diz_situazioni[s.localita].append(s)
       # print(self._diz_situazioni)

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
            print(costi)
            print(min(costi.items(), key=lambda x : x[1]))
            return min(costi.items(), key=lambda x : x[1])
        else:
            for c in self._diz_situazioni.keys():
                return self.sequenza_ricorsione(giorno - 1, mese)



