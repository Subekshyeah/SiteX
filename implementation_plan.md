# SiteX Semester 8 Transition Plan

This document outlines the detailed steps, features, and dependencies required for transitioning SiteX from its Semester 7 baseline to the final Semester 8 architecture. The transition focuses on upgrading the core analytical engine to a Graph Neural Network (GNN), automating data pipelines with Overpass API, migrating to a robust PostGIS database, and introducing advanced geospatial front-end features.

## Decision Log

- **Database Selection:** We will proceed with **SQLite + SpatiaLite**. It is free, serverless, and integrates easily into Python/FastAPI without external hosting costs.
- **Model Focus:** We are fully committing to the **Graph Neural Network (HeteroGAT)** as requested by supervisors. We will deprecate the XGBoost fallback strategy for now to concentrate our efforts.
- **Isochrone API:** We will integrate **OpenRouteService**. It has a generous free tier, is open-source, and can be self-hosted in the future, making it highly scalable for the project's long-term shape.
- **Overpass API Pipeline:** The data fetching pipeline will be a manually triggered script for now. We will delay automated cron-scheduling until later phases.
- **Training Data Size:** The current dataset of 3000–4000 rows is a solid foundation for training our initial HeteroGAT model, especially when enriched with spatial topology features.

## Proposed Changes

---

### Data Engineering & Storage (Owner: Roj)

- **Database Setup:** 
  - Configure **SQLite with the SpatiaLite extension**.
  - Migrate existing data (`CSV_Reference/`, `master_cafes_metrics.csv`, `Roadway.geojson`) into SQLite spatial tables using `GeoPandas.to_file()`.
- **Data Ingestion Automation:** 
  - Transition from Apify to **Overpass API** via a manually-triggered Python script for fetching OpenStreetMap (OSM) data.
  - Implement parsing of specific OSM tags (`amenity`, `cuisine`, `price_range`, `brand`) for café/retail characterization.
- **Graph Construction Pipeline:** 
  - Construct PyTorch Geometric `HeteroData` objects combining POIs and road networks.
  - Engineer node features (encoding categorical data like price tier into embeddings/one-hot vectors).

#### [MODIFY] `backend/app/lib/road_network.py`
*(Will be updated to support edge-snapping, subgraph extraction, and integration with the PyTorch Geometric data pipeline)*

---

### Machine Learning & AI Core (Owner: Sujal & Subekshya)

- **GNN Transition (HeteroGAT):**
  - Implement a Heterogeneous Graph Attention Network (HeteroGAT) using PyTorch Geometric to predict suitability scores. We will train this directly on the existing 3000-4000 labeled nodes.
  - Define node features (centrality, walkability) and edge structures.
  - Setup training loops with appropriate loss functions (MSE/MAE) and evaluation metrics (R² score).
- **Competitor Analytics & Market Saturation:**
  - Implement DBSCAN clustering to detect "synergy hubs" vs. "isolated competitors".
  - Calculate Herfindahl-Hirschman Index (HHI) for market saturation/cannibalization.
- **Persona-Aware Scoring:**
  - Introduce dynamic feature weighting based on user persona (e.g., Budget vs. Premium Café).
- **Explainable AI (XAI):**
  - Refine Gemini API prompts to ingest graph-topology features and model insights for natural language score explanations.

---

### Backend System (FastAPI) (Owner: Sujal & Subekshya)

- **Endpoint Upgrades:**
  - Update `POST /api/v1/predict-score/` to serve the new GNN model. Implement FastAPI `BackgroundTasks` if graph inference introduces latency.
  - Update `POST /api/v1/explain/` to parse graph context for Gemini.
  - Add `POST /api/v1/competitor-analysis/` to serve clustering and HHI metrics.
- **Model Serialization:**
  - Setup efficient saving/loading mechanisms for PyTorch models (`torch.save/load`) at application startup.

---

### Frontend UI & Map Features (Owner: Sujal)

- **Advanced Map Layers:**
  - Integrate **OpenRouteService** for dynamic Isochrone generation.
  - Add `Leaflet.heat` for density heatmaps.
  - Manage state for toggling POI categories via GeoJSON overlays.
- **User Inputs:**
  - Implement Business Persona UI (allow users to specify their café model).
- **State Management:**
  - Introduce robust state management (Zustand or Context API) for handling pins, layers, and result panels.

---

### Documentation & Presentation (Owner: Anish)

- **Academic Report:**
  - Write comprehensive chapters on GeoAI literature review, RFM analysis, GNN concepts, and project methodology.
- **API Auto-Docs:**
  - Ensure FastAPI Swagger UI (`/docs`) is fully documented using docstrings, response models, and request examples.
- **System Architecture Diagrams:**
  - Maintain updated Notion and GitHub README documentation.

## Verification Plan

### Automated Tests
- Unit tests for the Overpass API automated fetching script.
- Graph construction verification (testing `HeteroData` integrity and shape mapping).
- Regression testing on model metrics (comparing HeteroGAT MAE/RMSE against historical baselines).

### Manual Verification
- Dropping test pins in Kathmandu on the new frontend and visually verifying the generated Isochrones and Heatmap overlays.
- Reading the Gemini-generated explainability output to ensure it accurately mentions graph-derived logic (e.g., "Betweenness centrality is high here...").
- Confirming the persona switch (Budget -> Premium) alters the suitability score realistically for the same dropped pin.
