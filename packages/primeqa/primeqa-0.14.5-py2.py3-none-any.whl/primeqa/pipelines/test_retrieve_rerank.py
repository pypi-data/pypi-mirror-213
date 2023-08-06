from primeqa.pipelines.retrieve_rerank import RetrieveRerankPipeline
from primeqa.components.retriever.sparse import BM25Retriever
from primeqa.components.reranker.colbert_reranker import ColBERTReranker

queries = [
    "Which is the largest city in the state of Oregon?",
    "In which country was cholera first diagnosed?"
]
index_root = "/dccstor/colbert-ir/bsiyer/PQLL/indexes/bm25"
index_name = "wikiindex"
reranker_model = "/dccstor/colbert-ir/bsiyer/PQLL/experiments/apr5_2023/2023-04/05/11.05.23/checkpoints/colbert.dnn.batch_17524.model"
reranker_model = "/dccstor/colbert-ir/franzm/experiments/mar3_22_21/2023-03/22/14.39.40/checkpoints/colbert-LAST.dnn"


retriever = BM25Retriever(index_root=index_root, index_name=index_name, collection=None)
retriever.load()
hitsperquery = retriever.predict(queries, max_num_documents=10, include_text=True)

hits_per_query_for_reranking = []
for hits in hitsperquery:
    hits_for_reranking = []
    for r in hits:
        hits_for_reranking.append({
                    "document": {
                        "document_id": r[0],
                        "text": r[2],
                        "title": r[3]
                    },
                    "score": r[1]
                })
    hits_per_query_for_reranking.append(hits_for_reranking)


print(hits_per_query_for_reranking[0])

print("RERANKING...")
reranker = ColBERTReranker(model=reranker_model)
reranker.load()
reranked_results = reranker.predict(queries, hits_per_query_for_reranking)
print(reranked_results[0])
print("done")
    
