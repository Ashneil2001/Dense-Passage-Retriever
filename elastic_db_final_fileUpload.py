
from fastapi import FastAPI, File, UploadFile
from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore
import uvicorn

app = FastAPI()

# @app.route('/write_documents', methods=['POST'])
# def write_documents():
#     doc_store = ElasticsearchDocumentStore(
#         host='localhost',
#         username='', password='',
#         index='aurelius'
#     )
#     file_path = request.files['file']
#     file_path.save(file_path.filename)
 

#     with open(file_path.filename, 'r',encoding='utf-8') as f:
#         data = f.read()

#     data = data.split('\n')
#     print(data)
#     data_json = [
#         {
#             'content': paragraph,
#             'meta': {
#                 'source': 'meditations'
#             }
#         } for paragraph in data
#     ]

#     doc_store.write_documents(data_json)

#     return 'Documents written successfully!'

@app.post('/write_documents')
async def write(file : UploadFile = File(...)):

    file_location = file.filename

    with open(file_location,'wb') as f:
        f.write(file.file.read())

    doc_store = ElasticsearchDocumentStore(
        host='localhost',
        username='', password='',
        index='aurelius'
    )
    with open(file_location, 'r',encoding='utf-8') as f:
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
    uvicorn.run(app)
