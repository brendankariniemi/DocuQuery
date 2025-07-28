import os

from langchain.callbacks import get_openai_callback
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma

from caching import get_cached_data, cache_data
from utils import load_and_split_text


def get_answer(question):
    """Return answer to *question* by searching across all pre-populated documents."""
    try:
        embeddings = get_cached_data('Embeddings')
        if embeddings is None:
            embeddings = OpenAIEmbeddings()
            cache_data('Embeddings', embeddings)

        # Gather and split text from every supported document in /documents
        docs_dir = 'documents'
        texts = []
        for filename in os.listdir(docs_dir):
            if filename.lower().endswith(('.pdf', '.txt')):
                texts.extend(load_and_split_text(os.path.join(docs_dir, filename)))

        vectors = Chroma.from_documents(texts, embeddings)

        chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="map_rerank",
                                                            retriever=vectors.as_retriever(),
                                                            return_source_documents=True)

        with get_openai_callback() as cb:
            result = chain({"question": question})
        print(cb)

        answer = result.get('answer')
        page = result.get('source_documents', [{}])[0].metadata.get('page', '')

        return answer, page

    except Exception as e:
        return 'Exception: ' + str(e), 1
