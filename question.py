from langchain.callbacks import get_openai_callback
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma

from caching import get_cached_data, cache_data
from utils import load_and_split_text, get_file_hash


def get_answer(question, file_path):
    try:
        cache_key = 'Embeddings - ' + get_file_hash(file_path)
        embeddings = get_cached_data(cache_key)

        if embeddings is None:
            embeddings = OpenAIEmbeddings()
            cache_data(cache_key, embeddings)

        texts = load_and_split_text(file_path)
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
