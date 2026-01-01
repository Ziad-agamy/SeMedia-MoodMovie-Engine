# Context-Aware Movie Recommendation Engine

## Table of Contents
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Solution Architecture](#solution-architecture)
- [System Components](#system-components)
- [Roadmap](#roadmap)

## Project Overview
This project implements an advanced recommendation system designed to move beyond traditional keyword matching and collaborative filtering. By leveraging Large Language Models (LLMs) and semantic search, the system interprets the user's current emotional state and "vibe" to provide highly personalized movie suggestions.

## Problem Statement
Modern streaming platforms suffer from the "Paradox of Choice." While users have access to vast libraries of content, discovering a movie that fits a specific, often abstract, mood is difficult. Standard filtering (e.g., by genre or release year) fails to capture the nuance of a user's immediate psychological need—such as wanting "catharsis" or "low-energy background entertainment." This disconnect often leads to decision fatigue and user churn.

## Solution Architecture
The core philosophy of this engine is **Semantic Understanding over Metadata Matching**. The system treats user input not as a set of keywords, but as a narrative description of their desired experience. 

It functions by:
1.  **Decoding Intent**: Analyzing natural language to infer implicit signals like mood, energy level, and cognitive load.
2.  **Semantic Mapping**: Translating these signals into a rich textual description (the "vibe") that represents the ideal movie.
3.  **Vector Retrieval**: Using this description to query a vector database for content that matches the *feeling* of the request, not just the tags.

## System Components

### 1. Intent Analysis Module (Mood Extractor)
An LLM-driven component (see [`schemas.py`](app/user_intent/schemas.py)) that acts as the entry point for user interaction. It processes raw natural language to extract structured data points, including:
-   **Current Emotion**: The user's present state.
-   **Desired Goal**: The intended outcome (e.g., Uplift, Distract).
-   **Cognitive Load**: The preferred complexity of the content.
-   **Energy Required**: The level of energy required.

### 2. Semantic Query Generator (Film Vibe Generator)
This module bridges the gap between user intent and content retrieval. It synthesizes a cinematic description—a "synthetic synopsis"—based on the extracted intent. This generated text serves as the query for the vector database, ensuring that the search aligns with the thematic and atmospheric qualities the user is seeking (see [`vibe_predictor.py`](app/user_intent/vibe_predictor.py)).

### 3. Data Ingestion Pipeline
A robust data collection framework that has aggregated approximately **20,000 titles** (2010–2025) via the TMDB API ([`collect.py`](app/data/raw/collect.py)).
A dedicated processing script ([`data_pipeline.ipynb`](app/data/processed/data_pipeline.ipynb)) handles the transformation:
-   **Raw Data**: Ingests the initial `movies-raw.csv` containing raw API responses.
-   **Processed Data**: Outputs cleaned datasets with handled missing values, normalized text, and formatted fields, ensuring high-quality input for the embedding models.

## Roadmap
-   **RAG Pipeline Implementation**: Developing the Retrieval-Augmented Generation flow to ground LLM responses in the curated dataset.
-   **Vector Database Integration**: Indexing movie overviews and metadata for high-speed semantic retrieval.
-   **Frontend Development**: Creating an intuitive interface for real-time user interaction.
