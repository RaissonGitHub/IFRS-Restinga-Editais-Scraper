from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from editais_scraper import scrape_editais_bs
import uvicorn
import requests

app = FastAPI()

@app.get("/editais")
def get_editais(
    termo: Optional[str] = Query(None, description="Termo para busca nos editais"),
    detalhado: bool = Query(False, description="Retorna detalhes dos editais"),
    limit: Optional[int] = Query(None, description="Número máximo de resultados"),
    offset: Optional[int] = Query(None, description="Número de resultados a pular")
):
    """
    Rota para buscar editais usando BeautifulSoup.
    Parâmetros:
    - termo: termo para busca nos títulos, status ou categorias
    - detalhado: se True, retorna documentos detalhados do edital
    - limit: número máximo de resultados retornados
    - offset: número de resultados a pular antes de retornar
    """
    try:
        resultado = scrape_editais_bs(termo_busca=termo, detalhado=detalhado, limit=limit, offset=offset)
        return {"editais": resultado}
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Erro ao acessar site externo: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":

    uvicorn.run(".editais_api:app", host="127.0.0.1", port=8000, reload=True)
