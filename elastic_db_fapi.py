from fastapi import FastAPI, HTTPException, Form
from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore

app = FastAPI()

@app.post('/write_documents')
async def write_documents(file_path: str = Form(...)):
    doc_store = ElasticsearchDocumentStore(
        host='localhost',
        username='', password='',
        index='aurelius'
    )

    try:
        with open(file_path, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='File not found')

    data = data.split('\n')

    data_json = [
        {
            'content': paragraph,
            'meta': {
                'source': 'meditations'
            }
        } for paragraph in data
    ]

    doc_store.write_documents(data_json)

    return 'Documents written successfully!'
