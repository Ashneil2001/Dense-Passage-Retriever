import requests
from flask import Flask, request
from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore

app = Flask(__name__)

@app.route('/write_documents', methods=['POST'])
def write_documents():
    doc_store = ElasticsearchDocumentStore(
        host='localhost',
        username='', password='',
        index='aurelius'
    )

    # Replace <FILE_PATH> with the actual file path received from Postman
    file_path = request.form.get('file_path')

    with open(file_path, 'r') as f:
        data = f.read()

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

if __name__ == '__main__':
    app.run(port=5000)
