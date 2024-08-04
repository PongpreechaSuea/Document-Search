# https://sbert.net/docs/sentence_transformer/pretrained_models.html
MODEL = 'multi-qa-MiniLM-L6-dot-v1'

FILE_DOCUMENTS = "document_search.db"
NAME_DOCUMENTS = 'documents'
SPACE = "hnsw:space"
METHOD = "cosine"

FILEEXTENSIONS = ['*.txt', '*.pdf', '*.docx']