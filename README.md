# API de Editais IFRS Restinga

Este projeto contém dois módulos principais:
- **editais_scraper.py**: realiza o scraping dos editais do IFRS Restinga.
- **editais_api.py**: fornece uma API REST usando FastAPI para consultar os editais.

## Requisitos

- Python 3.13 (ou compatível)
- Instalar as dependências do projeto:
  ```sh
  pip install -r requirements.txt
  ```

## Como rodar o projeto

1. Ative o ambiente virtual (se estiver usando um):
   ```sh
   .\Scripts\Activate.ps1
   ```
2. Execute a API:
  ```sh
  uvicorn editais_api:app --reload
  ```
  A API estará disponível em `http://127.0.0.1:8000`.



## Endpoints

### `/editais`

Parâmetros:
- `termo` (opcional): termo para busca nos títulos, status ou categorias.
- `detalhado` (opcional, padrão: False): se True, retorna documentos detalhados do edital.
- `limit` (opcional): número máximo de resultados.
- `offset` (opcional): número de resultados a pular.

## Estrutura de retorno

### Sem detalhamento (`detalhado=False`)

```json
{
  "editais": [
    {
      "ultima_atualizacao": "27/08/2025",
      "titulo": "Edital de Bolsas",
      "link": "https://ifrs.edu.br/restinga/editais/123",
      "data": "27/08/2025",
      "categorias": ["Bolsas", "Estudantes"],
      "status": "Aberto"
    }
  ]
}
```

### Com detalhamento (`detalhado=True`)

```json
{
  "editais": [
    {
      "ultima_atualizacao": "27/08/2025",
      "titulo": "Edital de Bolsas",
      "link": "https://ifrs.edu.br/restinga/editais/123",
      "data": "27/08/2025",
      "categorias": ["Bolsas", "Estudantes"],
      "status": "Aberto",
      "documentos": {
        "arquivos": [
          {
            "publicacao": "27/08/2025",
            "nome": "Edital Completo",
            "link": "https://ifrs.edu.br/restinga/editais/123/edital.pdf",
            "grupo": "Principal"
          }
        ],
        "informacoes_adicionais": [
          "Informações extras sobre o edital..."
        ],
        "outros": [
          {
            "texto": "Anexo I",
            "link": "https://ifrs.edu.br/restinga/editais/123/anexo1.pdf"
          }
        ]
      }
    }
  ]
}
```

## Observações

- O projeto faz scraping do site oficial do IFRS Restinga, podendo estar sujeito a mudanças na estrutura do site.
