from django.shortcuts import render, get_object_or_404
import requests
from comuni.models import Regione, Provincia
from datetime import date, timedelta
from ColoreRegioni import ColoreRegioni
# Create your views here.

def coloreRegione(nomeRegione):
    regione = get_object_or_404(Regione, nome=nomeRegione)
    if nomeRegione == 'P.A. Bolzano':
        nomeRegione = 'Trentino-Alto Adige/Südtirol'
    if nomeRegione == 'P.A. Trento':
        nomeRegione = 'Trentino-Alto Adige/Südtirol'
    if nomeRegione == 'Friuli Venezia Giulia':
        nomeRegione = 'Friuli-Venezia Giulia'
    if nomeRegione == 'Abruzzo':
        nomeRegione = 'Abbruzzo'
    zoneRegioni = ColoreRegioni().colori_emoji
    tmp = [regione.nome, zoneRegioni[nomeRegione][0]]
    return tmp

def calcolaTotale(lista):
    positivi_oggi = lista[0]['nuovi_positivi']
    positivi_ieri = lista[1]['nuovi_positivi']
    tamponi_oggi = lista[0]['tamponi'] - lista[1]['tamponi']
    tamponi_ieri = lista[1]['tamponi'] - lista[2]['tamponi']
    dimessi_oggi = lista[0]['dimessi_guariti'] - lista[1]['dimessi_guariti']
    dimessi_ieri = lista[1]['dimessi_guariti'] - lista[2]['dimessi_guariti']
    deceduti_oggi = lista[0]['deceduti'] - lista[1]['deceduti']
    deceduti_ieri = lista[1]['deceduti'] - lista[2]['deceduti']
    positivi_totali = lista[0]['totale_positivi']
    tamponi_totali = lista[0]['tamponi']
    dimessi_totali = lista[0]['dimessi_guariti']
    deceduti_totale = lista[0]['deceduti']
    totale_casi = lista[0]['totale_casi']
    lista_casi = []
    lista_giorni = []
    for i in lista[:31]:
        lista_casi.append(i["nuovi_positivi"])
        tmp = i['data'][5:10]
        lista_giorni.append(tmp[3:] + tmp[2] + tmp[:2])
    lista_casi = lista_casi[::-1]
    lista_giorni = lista_giorni[::-1]
    d = {
        'positivi_oggi': positivi_oggi,
        'positivi_ieri': positivi_ieri,
        'tamponi_oggi': tamponi_oggi,
        'tamponi_ieri': tamponi_ieri,
        'dimessi_oggi': dimessi_oggi,
        'dimessi_ieri': dimessi_ieri,
        'deceduti_oggi': deceduti_oggi,
        'deceduti_ieri': deceduti_ieri,
        'positivi_totali': positivi_totali,
        'tamponi_totali': tamponi_totali,
        'dimessi_totali': dimessi_totali,
        'deceduti_totali': deceduti_totale,
        'lista_casi': lista_casi,
        'lista_giorni': lista_giorni,
        'totale_casi': totale_casi,
    }
    return d

def homepage(request):
    url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
    response = requests.get(url).json()[::-1]
    context = calcolaTotale(response)
    zona = 'Italia'
    context['zona'] = zona
    regioni = Regione.objects.all()
    context['regioni'] = regioni
    url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json'
    response = requests.get(url).json()[::-1]
    sorted_response = sorted(response, key=lambda k: k['nuovi_positivi'], reverse=True)
    lista = []
    casi_totali_nazionale = context['positivi_oggi']
    for i in sorted_response:
        percentuale = 100 * i['nuovi_positivi'] / casi_totali_nazionale
        lista.append({'regione': get_object_or_404(Regione, nome=i['denominazione_regione']), 'percentuale': percentuale})
    context['listaPercentile'] = lista
    url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-note.json'
    response = requests.get(url).json()[::-1]
    context['nota'] = response[0]
    return render(request, 'app/homepage.html', context)

def regione_detail(request, codice_istat):
    regione = get_object_or_404(Regione, codice_regione=codice_istat)
    if True:
        #regione = Regione.objects.filter(codice_regione=codice_istat)
        url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json'
        response = requests.get(url).json()[::-1]
        lista = []
        for i in range(len(response)):
            if response[i]['denominazione_regione'] == regione.nome:
                lista.append(response[i])
        context = calcolaTotale(lista)
        context['zona'] = regione.nome
        regioni = Regione.objects.all()
        context['regioni'] = regioni
        context['regione'] = coloreRegione(regione.nome)
        url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json'
        response = requests.get(url).json()
        sorted_response = sorted(response, key=lambda k: k['totale_casi'], reverse=True)
        listaProvince = []
        lista = []
        for i in sorted_response:
            if (i['denominazione_regione'] == regione.nome) and ('aggiorna' not in i['denominazione_provincia']) and ('Regione' not in i['denominazione_provincia']):
                listaProvince.append(i)
        casi_totali_regione = context['totale_casi']
        tmp = 0
        for i in listaProvince:
            percentuale = 100 * i['totale_casi'] / casi_totali_regione
            lista.append({'regione': get_object_or_404(Provincia, nome=i['denominazione_provincia']), 'percentuale': percentuale})
            tmp += percentuale
        context['listaPercentile'] = lista
    return render(request, 'app/detail_regione.html', context)

def notizie_list_view(request):
    data = (date.today() + timedelta(days=-5)).strftime("%Y-%m-%d")
    if request.GET.get('q') == None:
        url = f'http://newsapi.org/v2/everything?qInTitle=covid+OR+virus+OR+vaccin&from={data}&language=it&sortBy=popularity,-&apiKey=14f262fcefa24a3f98e8e69056a181c9'
    else:
        url = f'http://newsapi.org/v2/everything?q={request.GET.get("q")}&qInTitle=covid+OR+virus+OR+vaccin&from={data}&language=it&sortBy=popularity,-&apiKey=14f262fcefa24a3f98e8e69056a181c9'
    response = requests.get(url).json()
    oggi = date.today()
    giorno_oggi = oggi.day
    mese_oggi = oggi.month
    anno_oggi = oggi.year
    tmp_oggi = date(anno_oggi, mese_oggi, giorno_oggi)
    for i in range(len(response['articles'])):
        anno, mese, giorno = response['articles'][i]['publishedAt'][:10].split('-')
        tmp_articolo = date(int(anno), int(mese), int(giorno))
        giorni_mancanti = (tmp_oggi - tmp_articolo).days
        if giorni_mancanti == 0:
            response['articles'][i]['publishedAt'] = 'Pubblicato oggi'
        elif giorni_mancanti == 1:
            response['articles'][i]['publishedAt'] = 'Pubblicato ieri'
        elif giorni_mancanti == 2:
            response['articles'][i]['publishedAt'] = "Pubblicato l'altro ieri"
        else:
            response['articles'][i]['publishedAt'] = f"Pubblicato {giorni_mancanti} giorni fa"
    context = {'articoli': response}
    regioni = Regione.objects.all()
    context['regioni'] = regioni
    return render(request, 'app/notizie_list.html', context)



    # codice...



