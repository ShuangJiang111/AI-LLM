# export DASHSCOPE_API_KEY='sk-9fdaf5b5b2814c8380e47b427087618d'
# imports
from llama_index.embeddings.dashscope import (
    DashScopeEmbedding,
    DashScopeTextEmbeddingModels,
    DashScopeTextEmbeddingType,
)

# Create embeddings
# text_type=`document` to build index
embedder = DashScopeEmbedding(
    model_name=DashScopeTextEmbeddingModels.TEXT_EMBEDDING_V2,
    text_type=DashScopeTextEmbeddingType.TEXT_TYPE_DOCUMENT,
)
text_to_embedding = ["风急天高猿啸哀", "渚清沙白鸟飞回", "无边落木萧萧下", "不尽长江滚滚来"]
# Call text Embedding
result_embeddings = embedder.get_text_embedding_batch(text_to_embedding)
# requests and embedding result index is correspond to.
for index, embedding in enumerate(result_embeddings):
    if (
        embedding is None
    ):  # if the the correspondence request is embedding failed.
        print("The %s embedding failed." % text_to_embedding[index])
    else:
        print("Dimension of embeddings: %s" % len(embedding))
        print(
            "Input: %s, embedding is: %s"
            % (text_to_embedding[index], embedding[:5]) # embedding返回一个数组
        )