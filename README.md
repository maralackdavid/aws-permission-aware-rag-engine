# Permission-Aware AWS RAG Engine (Enterprise Knowledge System)

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazonaws)](https://aws.amazon.com/bedrock/)
[![OpenSearch](https://img.shields.io/badge/OpenSearch-Serverless-005FD1?logo=opensearch)](https://aws.amazon.com/opensearch-service/)
[![Framework](https://img.shields.io/badge/Methodology-PMI--CPMAI-blue)](https://www.pmi.org/)

An enterprise-grade, permission-aware Retrieval-Augmented Generation (RAG) architecture engineered on AWS. Enforces **AWS IAM Role-Based Access Control (RBAC)** metadata filtering inside vector search queries to prevent cross-departmental data leakage, backed by hybrid search and cross-encoder re-ranking.

---

## 1. CPMAI Phase I: Matching AI to Business Needs

Following the **PMI Certified Professional in Managing AI (CPMAI) Phase I (Business Understanding)** framework, this architecture was evaluated to ensure AI is applied as a targeted, high-value solution rather than a technology trend.

### 1.1 Business Objective & ROI Feasibility
* **Target Audience**: 500+ Internal Tier-1 Support Representatives.
* **Problem Statement**: Enterprise support reps waste hundreds of hours searching across fragmented, siloed technical documentation, resulting in high average handle times (AHT) and rising operational support expenses.
* **Projected Financial ROI**: A 35% reduction in support handle time yields an estimated **\$1.8M in annual operational savings** for a 500-agent tier-1 baseline, achieving full payback within 12 months.

### 1.2 Cognitive vs. Non-Cognitive Justification
* **Why AI is Required (Probabilistic Need)**: Customer support queries contain high variability, semantic vagueness, and natural language nuances. Traditional keyword search (deterministic) fails when terminology differs between user queries and documentation.
* **Non-Cognitive Integration**: Deterministic automation handles standard authentication, API Gateway routing, and static user identity validation, reserving LLM probabilistic processing strictly for semantic context retrieval and natural language synthesis.

### 1.3 AI Pattern Mapping
* **Primary Pattern**: **Conversational and Human Interaction** (providing natural language Q&A grounded in enterprise documentation).
* **Secondary Pattern**: **Predictive Analytics & Decision Support** (re-ranking candidate context chunks to present optimal decision paths for support agents).

### 1.4 DIKUW Pyramid Alignment
* **Data (Base Facts)**: Raw PDFs, policy manuals, and support logs stored in Amazon S3.
* **Information (Organized Data)**: Document metadata, department ownership tags, and structured RBAC role attributes.
* **Knowledge (The AI Sweet Spot)**: Vector embeddings generated via Amazon Titan Text v2 and stored in OpenSearch Serverless, enabling pattern recognition across semantic concepts.
* **Understanding (Grounded Synthesis)**: Claude 3.5 Sonnet synthesizes precise, citation-backed support answers tailored to the user's permission scope.

### 1.5 CPMAI Go/No-Go Assessment (3x3 Feasibility Matrix)

| Feasibility Pillar | Assessment Criteria | Status | Strategic Justification |
| :--- | :--- | :---: | :--- |
| **Business Feasibility** | Problem Definition | 🟢 **GO** | Clear operational pain point with measurable \$1.8M AHT reduction target. |
| | Sponsor Commitment | 🟢 **GO** | Support leadership committed to adoption without expanding agent headcount. |
| | Sufficient ROI | 🟢 **GO** | High financial return with < 12-month payback period. |
| **Data Feasibility** | Data Availability | 🟢 **GO** | Comprehensive internal technical documentation and FAQs exist in S3. |
| | Access & Security | 🟢 **GO** | IT owns data repositories with authenticated IAM access. |
| | Data Quality | 🟢 **GO** | Pre-processing and chunking pipelines clean and structure legacy PDFs. |
| **Execution Feasibility** | Technology & Skills | 🟢 **GO** | AWS Bedrock and OpenSearch Serverless provide mature, managed infrastructure. |
| | Implementation Timeline | 🟢 **GO** | Agile pilot deployment achievable in short 2-week iterations. |
| | Operational Context | 🟢 **GO** | Embedded directly into support agent dashboard via REST API. |

*Overall Assessment*: **ALL GREEN (GO)** — Project approved for technical implementation.

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
3. CPMAI Critical Path Milestones Project Plan
This project plan applies the Cognitive Project Management for AI (CPMAI) 6-phase framework. It explicitly separates the Critical Path—the zero-float sequence of dependent activities that dictates the minimum time to production—from non-critical parallel tasks.
graph TD
    classDef critical fill:#ff9999,stroke:#990000,stroke-width:2px,color:#000;
    classDef slack fill:#e1f5fe,stroke:#0288d1,stroke-width:1px,color:#000;
    classDef gate fill:#ffe0b2,stroke:#f57c00,stroke-width:2px,color:#000;

    subgraph Phase1 ["Phase I: Business Understanding (W1-W2)"]
        M1["M1: CPMAI 3x3 Feasibility & ROI Model"]:::critical
        S1["Agile Team Charter & Sprint Backlog"]:::slack
        G1{"GATE 1: Go/No-Go Decision"}:::gate
    end

    subgraph Phase2 ["Phase II: Data Understanding (W3-W4)"]
        M2["M2: S3 Corpus Hygiene Audit & RBAC Claims Mapping"]:::critical
        G2{"GATE 2: Data Quality & Security Approval"}:::gate
    end

    subgraph Phase3 ["Phase III: Data Preparation (W5-W6)"]
        M3A["M3A: Ingestion Lambda & Semantic Chunking"]:::critical
        M3B["M3B: Titan Embeddings & OpenSearch RBAC Ingestion"]:::critical
    end

    subgraph Phase4 ["Phase IV: Model Development (W7-W8)"]
        M4A["M4A: OpenSearch Hybrid Search & Security Filter"]:::critical
        M4B["M4B: Cohere Re-Ranker & Versioned Prompt Config"]:::critical
        S2["UI Agent Dashboard Integration Stub"]:::slack
    end

    subgraph Phase5 ["Phase V: Model Evaluation (W9-W10)"]
        M5A["M5A: 100-Item Golden Test Dataset Curation"]:::critical
        M5B["M5B: Ragas Offline Eval & CI/CD Regression Gate"]:::critical
        G3{"GATE 3: Pre-Deployment SLA Verification"}:::gate
    end

    subgraph Phase6 ["Phase VI: Model Operationalization (W11-W12)"]
        M6A["M6A: AWS X-Ray & CloudWatch Telemetry Instrumentation"]:::critical
        M6B["M6B: Pilot Rollout & Human-in-the-Loop Escalation"]:::critical
        G4{"GATE 4: Production SLA Sign-off"}:::gate
    end

    %% Dependencies
    M1 --> G1
    S1 --> G1
    G1 -->|APPROVED| M2
    M2 --> G2
    G2 -->|APPROVED| M3A
    M3A --> M3B
    M3B --> M4A
    M4A --> M4B
    M4B --> M5A
    S2 --> M5A
    M5A --> M5B
    M5B --> G3
    G3 -->|PASSED| M6A
    M6A --> M6B
    M6B --> G4
