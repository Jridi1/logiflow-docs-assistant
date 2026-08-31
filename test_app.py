from embeddings import get_embeddings
from sklearn.metrics.pairwise import cosine_similarity

from chain import ask
def test_ask():
    questions = ["What's the rate limit on the bulk shipment endpoint?",
                 "How many bulk shipment requests can I send per minute?",
                 "Why am I getting rate limited on `/v2/shipments/bulk` even though I'm on Enterprise?"]
    emb = get_embeddings()

    expected_value = "10 req/min flat cap, regardless of plan"
    expected_value_encoded = emb.embed_query(expected_value)
    for question in questions:
        true_value = ask(question).answer.lower()
        true_value_encoded = emb.embed_query(true_value)

        similarity = cosine_similarity([expected_value_encoded], [true_value_encoded])[0][0]

        assert similarity > 0.2
        assert "10" in  true_value 
        assert "req" in true_value or "request" in true_value  
        assert "minute" in true_value or "min" in true_value
        assert "plan" in true_value
    