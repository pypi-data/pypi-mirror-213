from typing import List
from tqdm import tqdm

from primeqa.components.base import Reranker, Retriever


class RetrieveRerankPipeline:
    def __init__(self, retriever: Retriever, reranker: Reranker) -> None:
        self.retriever = retriever
        self.reranker = reranker
        self.corpus_passages = []
        if self.retriever.collection is not None:
            with open(self.retriever.collection, "r") as infile:
                for line in tqdm(infile):
                    id, text, title = line.split("\t")
                    self.corpus_passages.append(title + " " + text)

    def run(self, queries: List[str], rerank=True):
        
        # retrieve
        search_results = self.retriever.predict(input_texts=queries)
        
        # rerank
        results_per_query = []
        for results in search_results:
            hits = []
            for r in results:
                hits.append({
                    "document": {
                        "document_id": r['doc_id'],
                        "text": r["text"] if 'text' in r else self.corpus_passages[r['doc_id']],
                        "title": r["title"] if 'title' in r else None
                    },
                    "score": r['score']
                })
            results_per_query.append(hits)
                
        if rerank:
            reranked_results = self.reranker.predict(queries,results_per_query)
            return reranked_results
        else:
            return results_per_query
        
        
        
