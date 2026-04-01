# Research Notes: Modern Transformer Variants
## Sub-topic 7 of 7

### Key Concepts to Cover

1. **Efficient Attention Taxonomy (Tay et al. 2020)**
   - Fixed patterns: local window, strided, random (BigBird)
   - Learnable patterns: learned sparsity (Reformer via LSH)
   - Memory-based: compressed memory tokens (Set Transformer)
   - Low-rank: Linformer (project K, V to lower dimension)
   - Kernel methods: Performer (FAVOR+ random features)
   - Core motivation: reduce O(n^2) to O(n) or O(n*sqrt(n))

2. **Sparse Attention: Longformer**
   - Local sliding window attention: each token attends to w neighbors
   - Global attention: special tokens (e.g., [CLS]) attend to all tokens
   - Dilated sliding window: exponentially increasing receptive field
   - Complexity: O(n * w) instead of O(n^2)
   - Practical for documents up to 4096+ tokens

3. **Sparse Attention: BigBird**
   - Three attention patterns combined:
     - Random attention: each token attends to r random tokens
     - Window attention: local neighbors
     - Global attention: g tokens attend to/from all
   - Theoretical result: sparse attention can be Turing-complete
   - Matches full attention quality on many benchmarks

4. **Linear Attention / Performer (FAVOR+)**
   - Key insight: softmax(QK^T)V can be approximated with kernel trick
   - phi(Q) * (phi(K)^T * V) instead of softmax(Q * K^T) * V
   - Changes association order: O(n * d^2) instead of O(n^2 * d)
   - Random feature approximation for softmax kernel
   - Theoretically elegant but practically limited adoption

5. **FlashAttention**
   - Not an approximation — computes exact standard attention
   - IO-aware: designed around GPU memory hierarchy (SRAM vs HBM)
   - Tiling: process attention in blocks that fit in SRAM
   - Recomputation: don't materialize full n x n attention matrix
   - Results: 2-4x speedup, significant memory savings
   - FlashAttention-2: better parallelism, work partitioning
   - FlashAttention-3: hopper architecture, FP8 support
   - Now standard in all serious Transformer training

6. **Mixture-of-Experts (MoE)**
   - Replace single FFN with multiple expert FFNs + router
   - Router: linear layer that produces routing weights
   - Top-k routing: each token goes to k experts (typically k=1 or k=2)
   - **Switch Transformer**: simplified top-1 routing, trillion-parameter models
   - **GShard**: top-2 routing with auxiliary load-balancing loss
   - Load balancing: prevent experts from being under/over-utilized
   - Conditional computation: total params >> active params per token
   - Example: Mixtral 8x7B — 47B total params, ~13B active per token

7. **Vision Transformers (ViT)**
   - Input: image split into fixed-size patches (e.g., 16x16)
   - Each patch linearly embedded to d_model dimensions
   - Prepend [CLS] token for classification
   - Standard Transformer encoder on patch sequence
   - Position embeddings: learned 2D or 1D
   - DeiT: data-efficient training with distillation token
   - Showed Transformers can replace CNNs when data is sufficient

8. **State-Space Model Hybrids**
   - **Mamba**: selective state space model
     - Linear-time sequence modeling (O(n) instead of O(n^2))
     - Input-dependent selection mechanism
     - Hardware-aware implementation with scan algorithm
   - **Jamba (AI21)**: hybrid architecture
     - Interleave attention layers and Mamba layers
     - MoE in some layers
     - Best of both worlds: attention for precise recall, SSM for efficient long-range
   - Emerging pattern: hybrid architectures combining attention + alternatives

9. **Grouped-Query Attention (GQA)**
   - Multi-Head Attention: each head has own Q, K, V
   - Multi-Query Attention (MQA): all heads share K, V
   - GQA: intermediate — groups of heads share K, V
   - LLaMA 2 (70B): 8 KV heads for 64 query heads
   - Reduces KV cache size proportionally
   - Minimal quality degradation

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S008 (Efficient Transformers Survey) | Taxonomy | Framework for understanding all variants |
| S009 (FlashAttention) | Algorithm | IO-aware tiling and recomputation |
| S010 (FlashAttention-2) | Improved algorithm | Parallelism improvements |
| S017 (Switch Transformer) | MoE | Top-1 routing, scaling results |
| S018 (Longformer) | Sparse attention | Local + global pattern |
| S019 (ViT) | Vision | Patch embedding approach |
| S020 (Mamba) | SSM | Selective state space model |
| S004 (Weng Transformer Family v2) | Survey | Comprehensive taxonomy |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S041 (Performer) | Linear attention | FAVOR+ algorithm |
| S042 (BigBird) | Sparse attention | Random + window + global |
| S045 (HuggingFace MoE blog) | MoE practical | Diagrams, routing explanation |
| S046 (FlashAttention explained) | FlashAttention intuition | Accessible explanation |
| S058 (Jamba) | Hybrid architecture | SSM + attention combination |
| S060 (GQA paper) | Attention efficiency | Grouped-query mechanism |
| S032 (Umar Jamil LLaMA) | Modern practice | GQA, RoPE in production |

### Visual Resources Found
- Efficient Transformers taxonomy diagram (from Tay et al.)
- Longformer attention pattern: sliding window + global
- BigBird: three-pattern attention visualization
- FlashAttention: memory hierarchy + tiling diagram
- MoE routing: token-to-expert assignment visualization
- ViT: image -> patches -> tokens pipeline
- Mamba vs Transformer: complexity comparison
- GQA: head grouping diagram

### Code Examples Found
- FlashAttention: PyTorch integration via torch.nn.functional.scaled_dot_product_attention
- HuggingFace Transformers: Longformer, BigBird implementations
- Switch Transformer: simplified routing in PyTorch
- ViT: timm library implementation
- Mamba: reference implementation in PyTorch + Triton

### Teaching Sequence (Recommended)
1. The quadratic attention bottleneck: why efficiency matters (intuition)
2. Taxonomy of solutions: sparse, low-rank, kernel, IO-aware
3. Sparse attention: Longformer and BigBird with pattern visualizations
4. Linear attention: Performer — elegant but limited
5. FlashAttention: the practical winner (exact + fast)
6. MoE: conditional computation for parameter efficiency
7. ViT: Transformers invade computer vision
8. SSM hybrids: Mamba and beyond
9. GQA: efficient inference through KV sharing
10. The future: what's next for Transformer architectures?

### Cross-links to Other Sub-topics
- -> Self-Attention: all variants modify or replace standard attention
- -> Positional Encoding: RoPE is standard in most modern variants
- -> Normalization: RMSNorm in most modern variants
- -> FFN: MoE replaces single FFN with expert ensemble
- -> Training: FlashAttention enables larger batch sizes; MoE changes scaling dynamics
- -> Encoder-Decoder: most modern variants are decoder-only

### Open Questions
- Will attention survive or be replaced by SSMs?
- Can we get subquadratic attention without quality trade-offs?
- Is MoE routing fundamentally limited by load imbalance?
- How far can context windows extend? (currently 128K-1M+)
- Will hybrid architectures become the standard?
