# HeteroGAT Implementation Plan

Now that your database is enriched with normalized metrics and the `composite_score`, the data is perfectly primed for a Graph Neural Network (GNN). Since our dataset has different types of entities (Places, Categories, Users/Reviewers), a **Heterogeneous Graph Attention Network (HeteroGAT)** is the ideal architecture.

Here is the step-by-step technical plan to build and train this model.

## Open Questions for You
> [!IMPORTANT]
> **What is the primary goal of the GNN?** 
> 1. **Recommendation System (Link Prediction):** Predicting which new Places a User will like (recommending places to users).
> 2. **Place Success Prediction (Node Regression):** Predicting the `composite_score` of a place based on its structural attributes (categories, location) before it even gets reviews.
> 
> *The plan below assumes a generalized HeteroGAT setup that leans toward Recommendation/Embedding Generation, but we can tailor it based on your answer.*

---

## Phase 1: Environment Setup
We need to install the deep learning ecosystem for graph networks.
- Install **PyTorch** (configured for your machine's CUDA/CPU).
- Install **PyTorch Geometric (PyG)**, which has native support for `HeteroData` and `HGTConv` (Heterogeneous Graph Transformer/Attention layers).
- Install `scikit-learn` and `torchmetrics` for evaluation.

## Phase 2: Graph Construction Pipeline
We will write a Python script (e.g., `build_graph.py`) to convert `ktm_all.db` into a PyG `HeteroData` object.

### Node Types
1. **`place`**: 
   - **Features:** `[rating_score_component, volume_score_component, foot_traffic_score_component, open_hours_score_component, lat, lng]`
   - **Target Label:** `composite_score` (if doing node prediction)
2. **`category`**:
   - **Features:** SentenceTransformer embeddings of the category name (e.g., "coffee shop" → 384-dimensional vector).
3. **`user`** (extracted from `reviews` table):
   - **Features:** Initialized as trainable embedding vectors (or aggregated features like average rating given).

### Edge Types
1. **`(place, has_category, category)`**: Unweighted structural edges.
2. **`(user, reviewed, place)`**:
   - **Edge Features:** `[rating, sentiment_score, sentiment_compound]` extracted from the reviews table.

## Phase 3: HeteroGAT Model Architecture
We will build the PyTorch model (`model.py`).

1. **Feature Transformation (Linear Layers):** Since different node types have different feature dimensions, we'll project them into a common hidden dimension (e.g., 64 or 128) using a `torch.nn.ModuleDict`.
2. **Heterogeneous Attention Layers:** 
   - We will use 2 to 3 layers of `HGTConv` (Heterogeneous Graph Transformer) or `HANConv` (Heterogeneous Attention Network).
   - These layers calculate attention scores differently depending on the *type* of relationship (e.g., a User-Place relationship is weighted differently than a Place-Category relationship).
3. **Output Head:**
   - *For Recommendation:* A dot-product decoder between User embeddings and Place embeddings.
   - *For Scoring:* An MLP (Multi-Layer Perceptron) reading the Place embedding to output a single continuous value (`composite_score`).

## Phase 4: Training Pipeline
1. **Mini-Batching:** Because 50k places + users + categories is too large to fit in memory all at once, we will use PyG's `HeteroNeighborLoader` to sample subgraphs during training.
2. **Loss Function:** 
   - Binary Cross Entropy (BCE) with Negative Sampling if training a recommendation system.
   - Mean Squared Error (MSE) if predicting scores.
3. **Optimization:** AdamW optimizer with a learning rate scheduler (ReduceLROnPlateau).
4. **Splits:** 80% Train, 10% Validation, 10% Test edges/nodes.

## Phase 5: Evaluation & Export
1. Evaluate metrics on the Test set (RMSE, Precision@K, NDCG depending on the task).
2. Save the trained model weights (`.pth`).
3. **Export Embeddings:** Run the trained model once over the entire graph to extract the final 64-dimensional dense vectors for all Places.
4. Save these embeddings back into `ktm_all.db` (e.g., creating a `place_embeddings` table). These vectors can then be used in your backend for real-time similarity search (e.g., "Find places similar to this one").

---

**Next Steps:**
Please review the open questions above. If this plan aligns with your vision, let me know whether you want to focus on **Recommendation (Link Prediction)** or **Place Scoring (Node Prediction)**, and I'll start generating the graph construction scripts!
