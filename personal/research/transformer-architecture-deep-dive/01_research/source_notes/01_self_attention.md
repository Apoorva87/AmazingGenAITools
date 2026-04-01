# Research Notes: Self-Attention Mechanism
## Sub-topic 1 of 7

### Key Concepts to Cover

1. **Scaled Dot-Product Attention**
   - Query, Key, Value interpretation: attention as soft dictionary lookup
   - Dot-product similarity: Q . K^T measures alignment
   - Scaling factor 1/sqrt(d_k): prevents softmax saturation in high dimensions
   - Softmax normalization: converts scores to probability distribution
   - Weighted sum of values: output is convex combination

2. **Multi-Head Attention (MHA)**
   - Multiple attention heads in parallel on projected subspaces
   - Each head: d_model -> d_k (where d_k = d_model / n_heads)
   - Concatenation + linear projection to recombine
   - Different heads learn different attention patterns (positional, syntactic, semantic)
   - Parameter count: 4 * d_model^2 (Q, K, V projections + output projection)

3. **Self-Attention vs Cross-Attention vs Causal Attention**
   - Self-attention: Q, K, V all derived from same sequence
   - Cross-attention: Q from decoder, K/V from encoder
   - Causal (masked) self-attention: lower-triangular mask prevents attending to future
   - Padding masks for variable-length batches

4. **Attention Patterns and Interpretation**
   - Attention weight visualization
   - What heads actually learn (positional, rare words, delimiter tracking)
   - Attention entropy as a diagnostic metric

5. **Multi-Query Attention (MQA) and Grouped-Query Attention (GQA)**
   - MQA: single K/V head shared across all Q heads (Shazeer 2019)
   - GQA: groups of Q heads share K/V heads (Ainslie 2023)
   - Memory bandwidth reduction for inference

6. **KV Cache for Efficient Inference**
   - Caching K/V for previously generated tokens
   - Incremental decoding: only compute attention for new token
   - Memory cost: 2 * n_layers * d_model * seq_len * bytes_per_param

7. **Computational Complexity**
   - Time: O(n^2 * d) for sequence length n, dimension d
   - Memory: O(n^2) for attention matrix
   - Why this is the bottleneck for long sequences

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S001 (Attention Is All You Need) | Original formulation | Mathematical definitions, architecture diagrams |
| S002 (Annotated Transformer) | Implementation | PyTorch code for every component |
| S003 (Illustrated Transformer) | Visualization | QKV flow diagrams, multi-head visualization |
| S025 (Karpathy GPT) | Code walkthrough | Live-coded attention with explanations |
| S034 (Raschka self-attention) | Step-by-step code | Clean from-scratch implementation |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S026 (3Blue1Brown attention) | Geometric intuition | Visual explanation of QKV as geometric operations |
| S028 (Umar Jamil attention) | Code + math | Detailed derivation with implementation |
| S044 (Bloem Transformer guide) | Holistic explanation | Alternative mathematical perspective |
| S050 (Weng Attention!) | Historical context | Evolution from Bahdanau to self-attention |
| S036 (Kipply inference) | Performance analysis | FLOP counting, memory bandwidth |

### Visual Resources Found
- Jay Alammar: Multi-head attention flow diagram (animated)
- 3Blue1Brown: QKV as geometric projections (video animation)
- Annotated Transformer: Attention heatmaps
- Sebastian Raschka: Step-by-step attention computation diagram

### Code Examples Found
- Annotated Transformer: Full attention class in PyTorch
- nanoGPT (S049): CausalSelfAttention class with FlashAttention support
- Sebastian Raschka: Manual attention computation without nn.Module
- Karpathy video: Live-coded attention from scratch

### Key Equations

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V

MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
  where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

### Teaching Sequence (Recommended)
1. Start with attention as dictionary lookup metaphor (intuition layer)
2. Derive scaled dot-product attention mathematically (formalism layer)
3. Implement single-head attention in PyTorch (engineering layer)
4. Extend to multi-head attention with projections
5. Add causal masking for decoder
6. Discuss KV cache for inference
7. Performance analysis and complexity

### Cross-links to Other Sub-topics
- -> Positional Encoding: attention is permutation-invariant, needs position info
- -> Normalization: LayerNorm applied before/after attention
- -> Encoder-Decoder: self-attention vs cross-attention in context
- -> Modern Variants: efficient attention, FlashAttention, GQA
- -> Training: attention dropout, gradient flow through attention

### Open Questions for Further Exploration
- Why does attention work so well compared to alternative mixing mechanisms?
- Is the softmax bottleneck a fundamental limitation?
- Can attention heads be pruned without quality loss?
