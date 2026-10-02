# Permission-Aware AWS RAG Engine (Enterprise Knowledge System)

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazonaws)](https://aws.amazon.com/bedrock/)
[![OpenSearch](https://img.shields.io/badge/OpenSearch-Serverless-005FD1?logo=opensearch)](https://aws.amazon.com/opensearch-service/)
[![Framework](https://img.shields.io/badge/Methodology-PMI--CPMAI-blue)](https://www.pmi.org/)

An enterprise-grade, permission-aware Retrieval-Augmented Generation (RAG) architecture engineered on AWS. Enforces **AWS IAM Role-Based Access Control (RBAC)** metadata filtering inside vector search queries to prevent cross-departmental data leakage, backed by hybrid search and cross-encoder re-ranking.

---

## 1. Executive Business Case & CPMAI Feasibility

* **Target Audience**: 500+ Internal Tier-1 Support Representatives.
* **Problem**: Fragmented documentation increased support handle times and operational costs.
* **Solution**: A permission-aware RAG engine combining BM25 keyword search with OpenSearch Serverless vector indexing and Claude 3.5 Sonnet synthesis.
* **Financial Model**: CPMAI Phase I feasibility framework projects a **35% reduction in handle time** (~\$1.8M annual operational savings for a 500-agent tier-1 baseline).

---

## 2. Target System Architecture

```mermaid
graph TD
    subgraph ClientLayer ["1. Client & Authentication Layer"]
        User["User / Support Agent"]
        IdP["Identity Provider (Cognito / Entra ID)"]
    end

    subgraph IngestionPipeline ["Async Document Ingestion Pipeline"]
        S3Docs["Amazon S3 Bucket\n(Raw PDFs/Docs)"]
        IngestLambda["AWS Lambda\n(Chunking & Metadata Parsing)"]
        TitanEmbed["Amazon Bedrock\n(Titan Text Embeddings v2)"]
    end

    subgraph CoreOrchestration ["2. API & Orchestration Layer"]
        APIGW["AWS API Gateway"]
        Orchestrator["AWS Lambda Orchestrator\n(Python / LangChain)"]
    end

    subgraph SearchAndRetrieval ["3. Vector & Re-Ranking Engine"]
        OpenSearch[("Amazon OpenSearch Serverless\n(Vector Engine + BM25)")]
        ReRanker["Cohere Cross-Encoder Rerank\n(Amazon Bedrock)"]
    end

    subgraph InferenceLayer ["4. Foundation Model Layer"]
        BedrockLLM["Amazon Bedrock\n(Claude 3.5 Sonnet)"]
    end

    subgraph GovernanceAndTelemetry ["5. Telemetry & Security"]
        IAMRBAC["AWS IAM RBAC Policy Engine\n(Least-Privilege Metadata Filters)"]
        CloudWatch["Amazon CloudWatch\n(Token Spend & Latency)"]
    end

    %% Ingestion Flow
    S3Docs -->|S3 Event Trigger| IngestLambda
    IngestLambda -->|Generate Vector Embeddings| TitanEmbed
    TitanEmbed -->|Store Vectors + IAM Metadata| OpenSearch

    %% Query Flow
    User -->|1. Authenticate| IdP
    IdP -->|2. Return JWT with Role Claims| User
    User -->|3. Submit Query + JWT| APIGW
    APIGW -->|4. Validate Token & Authorize| Orchestrator
    Orchestrator -->|5. Extract Role & Attach IAM Filter| IAMRBAC
    IAMRBAC -->|6. Enforce Least-Privilege Query| OpenSearch
    OpenSearch -->|7. Return Authorized Candidate Chunks| ReRanker
    ReRanker -->|8. Return Top-N Re-Ranked Chunks| Orchestrator
    Orchestrator -->|9. Construct Prompt + Chunks| BedrockLLM
    BedrockLLM -->|10. Synthesize Answer + Citation Links| Orchestrator
    Orchestrator -->|11. Return Response| User

    %% Telemetry
    Orchestrator -.->|Log Token Spend & Latency| CloudWatch