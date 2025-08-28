import requests
from bs4 import BeautifulSoup


def scrape_editais_bs(termo_busca=None, detalhado=False, limit=None, offset=None):
    """
    Realiza o scraping da página de editais usando BeautifulSoup, busca um termo e retorna os links dos PDFs.
    Parâmetros:
    - termo_busca: termo para busca nos títulos, status ou categorias
    - detalhado: se True, retorna documentos detalhados do edital (pdf e outros documentos)
    - limit: número máximo de resultados retornados
    - offset: número de resultados a pular antes de retornar
    Retorna: lista de editais
    """

    # Conexão
    url_base = "https://ifrs.edu.br/restinga/editais/"
    try:
        response = requests.get(url_base)
        response.raise_for_status()
    except requests.RequestException as e:
        return [{"erro": f"Falha ao acessar a página: {str(e)}"}]
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tabela de editais
    tabela = soup.find('table', class_='editais__table')
    if not tabela:
        return [{"erro": "Tabela de editais não encontrada."}]
    

    linhas = tabela.find_all('tr')
    editais = []

    # Extração de dados
    for linha in linhas:
        celulas = linha.find_all('td')
        if not celulas:
            continue
        edital = {}
        edital['ultima_atualizacao'] = celulas[0].get_text(strip=True)
        edital['titulo'] = celulas[1].get_text(strip=True)
        edital['link'] = celulas[1].find('a')['href'] if celulas[1].find('a') else "N/A"
        edital['data'] = celulas[2].get_text(strip=True)
        edital['categorias'] = [a.get_text(strip=True) for a in celulas[3].find_all('a')]
        edital['status'] = celulas[4].find('a').get_text(strip=True) if celulas[4].find('a') else "N/A"
        editais.append(edital)

    if termo_busca:
        editais = [edital for edital in editais 
                   if termo_busca.lower() in edital['titulo'].lower()
                   or termo_busca.lower() in edital['status'].lower() 
                   or termo_busca.lower() in ' '.join(edital['categorias']).lower()
                   ]
        
    if offset is not None:
        editais = editais[offset:]
    if limit is not None:
        editais = editais[:limit]

    if detalhado:
        for edital in editais:
            documentos = scrape_pagina_edital_bs(edital['link'])
            edital['documentos'] = documentos

    return editais


def scrape_pagina_edital_bs(url_edital):
    """
    Acessa a página de um edital e extrai os links dos arquivos PDF usando BeautifulSoup.
    Retorna: dict com arquivos, informações adicionais contidas na página e outros links contidos nela
    """

    # Conexão
    try:
        response = requests.get(url_edital)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"erro": f"Falha ao acessar a página do edital: {str(e)}"}
    soup = BeautifulSoup(response.text, 'html.parser')

    # Estrutura
    conteudo = {
        'arquivos': [],
        'informacoes_adicionais': [],
        'outros': [],
    }

    # Extração de dados

    # Informações adicionais
    info = soup.find(class_='edital__content')
    if info:
        texto = info.get_text(separator=' ', strip=True)
        # Ignora informações de compartilhamento
        texto = texto.replace('Compartilhar conteúdo: Facebook Twitter LinkedIn Pinterest WhatsApp', '')
        conteudo['informacoes_adicionais'].append(texto)
        # Se houver algum link, adiciona à lista de outros
        for link in info.find_all('a'):
            caminho = link.get('href')
            texto_link = link.get_text(strip=True)
            if caminho and 'crunchify-social__link' not in link.get('class', []) and texto_link:
                conteudo['outros'].append({'texto': texto_link, 'link': caminho})

    # Tabela de arquivos
    tabela_arquivos = soup.find('table', class_='edital__table')
    if tabela_arquivos:
        for linha in tabela_arquivos.find_all('tr'):
            celulas = linha.find_all('td')
            if len(celulas) < 3:
                continue
            documento = {}
            documento['publicacao'] = celulas[0].get_text(strip=True)
            strong = celulas[1].find('strong')
            documento['nome'] = strong.get_text(strip=True) if strong else "N/A"
            link = celulas[1].find('a')
            documento['link'] = link['href'] if link else "N/A"
            documento['grupo'] = celulas[2].get_text(strip=True)
            valido = all(valor != "N/A" for valor in documento.values())
            if valido:
                conteudo['arquivos'].append(documento)
    return conteudo
