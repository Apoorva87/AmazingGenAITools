# Labs Plan
## Transformer Architecture Deep Dive

### Lab Design Principles
- Language: Python 3.10+ with PyTorch
- Format: Jupyter notebooks with interleaved explanation
- Difficulty: progressive (guided -> scaffolded -> independent)
- Each lab: ~30-60 minutes
- All labs buildable on a single GPU or even CPU (small model sizes)

---

### Lab 1: Attention from Scratch
**Page**: Self-Attention Mechanism
**Duration**: 45 min
**Prerequisites**: PyTorch basics, matrix multiplication

**Objectives**:
- Implement scaled dot-product attention without using nn.MultiheadAttention
- Implement multi-head attention with explicit projections
- Visualize attention weights

**Exercises**:
1. Implement `scaled_dot_product_attention(Q, K, V, mask=None)` manually
2. Verify scaling factor effect: compare softmax distributions with and without 1/sqrt(d_k)
3. Implement `MultiHeadAttention(nn.Module)` with Q, K, V projections
4. Add causal masking for autoregressive attention
5. Visualize attention patterns for a sample sentence using matplotlib heatmaps
6. **Challenge**: Implement KV cache for incremental decoding

**Starter Code**: Provided
**Solution**: In companion notebook
**Source Reference**: S002 (Annotated Transformer), S034 (Raschka)

---

### Lab 2: Positional Encodings — Build and Compare
**Page**: Positional Encoding Deep Dive
**Duration**: 40 min
**Prerequisites**: Lab 1, trigonometry basics

**Objectives**:
- Implement sinusoidal PE and visualize frequency bands
- Implement RoPE and verify relative position property
- Compare extrapolation behavior

**Exercises**:
1. Implement sinusoidal positional encoding. Visualize as a heatmap (position vs dimension)
2. Show that sinusoidal PE satisfies: PE(pos+k) can be written as linear function of PE(pos)
3. Implement RoPE using rotation matrices for pairs of dimensions
4. Verify: dot product of RoPE-encoded vectors depends only on relative position
5. Implement learned positional embeddings
6. **Experiment**: Train small models with each PE type. Compare loss on sequences longer than training length

**Starter Code**: Provided
**Source Reference**: S006 (EleutherAI RoPE blog), S002 (Annotated Transformer)

---

### Lab 3: Normalization Showdown
**Page**: Normalization Techniques
**Duration**: 30 min
**Prerequisites**: Lab 1, basic statistics

**Objectives**:
- Implement LayerNorm and RMSNorm from scratch
- Compare Pre-LN and Post-LN training stability

**Exercises**:
1. Implement `LayerNorm(nn.Module)` from scratch (match nn.LayerNorm output)
2. Implement `RMSNorm(nn.Module)` from scratch
3. Build a 2-layer Transformer block with Pre-LN placement
4. Build the same block with Post-LN placement
5. **Experiment**: Train both on a toy task. Plot gradient norms across layers over training. Observe stability difference
6. **Experiment**: Try Post-LN without learning rate warmup. Document what happens

**Starter Code**: Provided (toy dataset and training loop)
**Source Reference**: S007 (Xiong et al.), S021 (RMSNorm), S049 (nanoGPT)

---

### Lab 4: FFN and Activation Deep Dive
**Page**: Feed-Forward Networks & Activation Functions
**Duration**: 30 min
**Prerequisites**: Lab 1

**Objectives**:
- Implement standard and SwiGLU FFN
- Compare activations empirically

**Exercises**:
1. Implement standard FFN: `Linear(d_model, d_ff) -> ReLU -> Linear(d_ff, d_model)`
2. Implement GELU FFN (using exact GELU, not approximation)
3. Implement SwiGLU FFN with three weight matrices
4. Count parameters for each variant (given d_model=512, d_ff=2048 for standard, adjusted for SwiGLU)
5. **Experiment**: Plot activation patterns: for random inputs, how many neurons are active? Compare ReLU vs GELU vs SwiGLU
6. **Benchmark**: Time forward+backward pass for each variant. Measure speed difference

**Starter Code**: Provided
**Source Reference**: S011 (Shazeer GLU), S037 (GELU), S049 (nanoGPT)

---

### Lab 5: Build a Complete Transformer
**Page**: The Encoder-Decoder Architecture
**Duration**: 60 min
**Prerequisites**: Labs 1-4

**Objectives**:
- Assemble all components into a working GPT-style model
- Generate text with the model

**Exercises**:
1. Combine attention + normalization + FFN into a `TransformerBlock(nn.Module)`
2. Stack N blocks into a `GPT(nn.Module)` with token + position embeddings and output head
3. Implement weight tying between embedding and output projection
4. Count total parameters for GPT-small config (N=6, d_model=384, n_heads=6)
5. Implement `generate(prompt, max_tokens, temperature)` with top-k sampling
6. **Optional**: Also build an encoder-decoder variant with cross-attention
7. **Challenge**: Implement the same model following both Pre-LN and Post-LN conventions

**Starter Code**: Component implementations from Labs 1-4
**Source Reference**: S025 (Karpathy GPT), S048 (minGPT), S049 (nanoGPT)

---

### Lab 6: Training Your Transformer
**Page**: Training Transformers
**Duration**: 60 min
**Prerequisites**: Lab 5

**Objectives**:
- Implement a production-quality training loop
- Train a small GPT on Shakespeare text

**Exercises**:
1. Implement a custom LR scheduler: linear warmup + cosine decay
2. Set up AdamW with proper weight decay (apply only to weight matrices, not biases/norms)
3. Add gradient clipping (max_norm=1.0)
4. Add mixed precision training using `torch.cuda.amp` / `torch.amp`
5. Add gradient accumulation for effective batch size control
6. Train GPT on tiny Shakespeare dataset. Monitor: loss, grad norms, LR, generated samples
7. **Experiment**: Compare training with and without warmup. Plot loss curves
8. **Experiment**: Try different learning rates (1e-3, 3e-4, 1e-4). Find the instability boundary

**Starter Code**: Model from Lab 5, Shakespeare dataset
**Source Reference**: S025 (Karpathy GPT), S049 (nanoGPT)

---

### Lab 7: Modern Attention Variants
**Page**: Modern Transformer Variants
**Duration**: 45 min
**Prerequisites**: Lab 1, Lab 5

**Objectives**:
- Use FlashAttention via PyTorch
- Implement a simple sparse attention pattern
- Implement basic MoE routing

**Exercises**:
1. Compare `torch.nn.functional.scaled_dot_product_attention` (FlashAttention) with manual attention: verify output matches, benchmark speed
2. Implement sliding-window attention (local attention with window size w)
3. Implement a simple top-k MoE router with 4 experts
4. Add auxiliary load-balancing loss to the MoE router
5. Implement ViT-style patch embedding for CIFAR-10 images
6. **Benchmark**: Plot attention time vs sequence length for standard vs flash vs local attention
7. **Challenge**: Combine sliding-window + global attention (simplified Longformer)

**Starter Code**: Partial implementations provided
**Source Reference**: S009 (FlashAttention), S017 (Switch Transformer), S019 (ViT)

---

### Summary

| Lab | Page | Duration | Difficulty | Key Deliverable |
|-----|------|----------|------------|----------------|
| 1 | Self-Attention | 45 min | Guided | Working MHA implementation |
| 2 | Positional Encoding | 40 min | Guided | Three PE implementations + comparison |
| 3 | Normalization | 30 min | Scaffolded | Pre-LN vs Post-LN stability comparison |
| 4 | FFN & Activations | 30 min | Scaffolded | SwiGLU implementation + benchmarks |
| 5 | Encoder-Decoder | 60 min | Scaffolded | Complete working GPT model |
| 6 | Training | 60 min | Independent | Trained GPT on Shakespeare |
| 7 | Modern Variants | 45 min | Independent | FlashAttention + MoE + ViT experiments |
| **Total** | | **5h 10min** | | |

### Cumulative Build

Labs are designed to build on each other:
```
Lab 1 (attention) + Lab 2 (PE) + Lab 3 (norm) + Lab 4 (FFN)
                    ↓
              Lab 5 (full model)
                    ↓
              Lab 6 (training)
                    ↓
              Lab 7 (modern variants)
```

Each lab produces reusable modules that are composed in later labs. By Lab 6, the student has built and trained a complete Transformer from scratch.
