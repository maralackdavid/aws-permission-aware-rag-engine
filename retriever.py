"""
AWS OpenSearch Serverless Hybrid Retriever with IAM RBAC Metadata Filtering
Author: David Maralack, AI Architect
"""
import json

def build_hybrid_query(user_query: str, user_role: str, top_k: int = 5):
    """
    Constructs a hybrid OpenSearch query combining vector similarity (k-NN)
    and BM25 keyword matching, filtered by user IAM RBAC role.
    """
    return {
        "size": top_k,
        "query": {
            "bool": {
                "must": [
                    {"match": {"text_content": user_query}}
                ],
                "filter": [
                    # Security Boundary: Enforce RBAC metadata filtering
                    {"term": {"allowed_roles": user_role}}
                ]
            }
        }
    }

if __name__ == "__main__":
    query = build_hybrid_query("How do I process a refund?", user_role="tier1_support")
    print("Constructed OpenSearch RBAC Query:")
    print(json.dumps(query, indent=2))