# Visuals Plan
## Transformer Architecture Deep Dive

### Visual Design Principles
- Style: Clean, technical illustrations (Lilian Weng / Jay Alammar aesthetic)
- Colors: Consistent color palette across all pages
- Interactive: Where possible, add hover/click interactivity (HTML)
- Annotations: Every diagram has numbered callouts explained in text

---

### Page 0: Main Narrative

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V0.1 | Full Architecture Diagram | Interactive SVG | Complete Transformer with clickable components linking to sub-topic pages. Color-coded: attention (blue), norm (green), FFN (orange), PE (purple) |
| V0.2 | Timeline | Horizontal timeline | RNN -> Attention -> Transformer -> BERT/GPT -> LLMs. Key papers and dates |
| V0.3 | Reading Path Map | Node graph | Visual navigation showing page dependencies and reading orders |

---

### Page 1: Self-Attention

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V1.1 | Soft Dictionary Lookup | Animated diagram | Query looking up keys, getting weighted values. Show progression from exact match to soft match |
| V1.2 | QKV Projection | Matrix diagram | Input -> W_Q, W_K, W_V projections -> Q, K, V matrices. Show dimensions |
| V1.3 | Attention Score Computation | Step-by-step | Q * K^T -> scale -> softmax -> weights. Show actual numbers for a 4-token example |
| V1.4 | Scaling Factor Intuition | Distribution plot | Histogram of dot-product values for d_k=1 vs d_k=64 vs d_k=512. Show softmax saturation |
| V1.5 | Multi-Head Attention | Parallel lanes diagram | Multiple heads processing in parallel, concatenation, output projection |
| V1.6 | Attention Heatmap | Heatmap | Example attention weights for a real sentence. Show different heads attending to different patterns |
| V1.7 | Causal Mask | Matrix diagram | Lower-triangular mask applied to attention scores. Before and after |
| V1.8 | KV Cache | Sequential diagram | Show how KV cache grows during autoregressive generation. Memory vs recomputation |

---

### Page 2: Positional Encoding

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V2.1 | Permutation Invariance | Before/after | Same sentence with shuffled tokens producing same attention output (without PE) |
| V2.2 | Sinusoidal Heatmap | Heatmap | Position (y) vs dimension (x) showing sin/cos frequency bands |
| V2.3 | Frequency Bands | Wave plot | Multiple sinusoids at different frequencies. Show how position creates unique "fingerprint" |
| V2.4 | RoPE Rotation | 2D rotation animation | Show how rotation encodes position. Two vectors being rotated, their dot product depending on relative angle |
| V2.5 | Position Method Comparison | Comparison table + diagram | Side-by-side: sinusoidal, learned, RoPE, ALiBi. Show how each injects position information |
| V2.6 | Length Extrapolation | Line plot | Performance vs sequence length for different PE methods. Show where each breaks down |

---

### Page 3: Normalization

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V3.1 | BN vs LN | Tensor diagram | 3D tensor (batch, seq, features) with shading showing which dimensions each method normalizes |
| V3.2 | Pre-LN vs Post-LN | Side-by-side architecture | Two Transformer blocks showing different normalization placement. Color-coded residual paths |
| V3.3 | Gradient Flow | Gradient magnitude plot | Gradient norms across layers for Pre-LN vs Post-LN (from Xiong et al.) |
| V3.4 | Activation Distribution | Histogram | Activations with and without normalization across training steps |

---

### Page 4: FFN & Activations

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V4.1 | FFN Expansion-Compression | Bottleneck diagram | d_model -> d_ff -> d_model with dimensions labeled |
| V4.2 | Activation Function Comparison | Function plot | ReLU, GELU, SwiGLU, SiLU on same axes. Show gradients below |
| V4.3 | Gating Mechanism | Flow diagram | SwiGLU: two paths (gate and value), element-wise multiplication |
| V4.4 | FFN as Key-Value Memory | Memory metaphor | First layer rows as "keys", second layer columns as "values". Pattern matching visualization |

---

### Page 5: Encoder-Decoder

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V5.1 | Complete Transformer | Full architecture diagram | Detailed encoder-decoder with all components labeled. The definitive reference diagram |
| V5.2 | Residual Stream | Stream diagram | Horizontal stream with sublayers branching off and adding back. Show information flow |
| V5.3 | Cross-Attention | Q-KV diagram | Decoder queries attending to encoder keys/values. Show the asymmetric source |
| V5.4 | Architecture Variants | Three-column comparison | Encoder-only (BERT) vs Decoder-only (GPT) vs Encoder-Decoder (T5). Show which layers each uses |
| V5.5 | Autoregressive Generation | Step-by-step animation | Token-by-token generation showing growing context and KV cache |
| V5.6 | Information Flow Trace | Full trace diagram | Single input token traced through all layers to output prediction |

---

### Page 6: Training

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V6.1 | LR Schedule | Line plot | Warmup + cosine decay curve with annotations. Mark typical milestones |
| V6.2 | Adam vs AdamW | Weight space diagram | Show L2 reg vs weight decay difference in parameter update |
| V6.3 | Mixed Precision | Data type diagram | FP32, FP16, BF16 bit layouts. Show which parts of training use which precision |
| V6.4 | Scaling Laws | Log-log plot | Loss vs compute/params/data. Kaplan curves with Chinchilla optimal line |
| V6.5 | Loss Spike | Training loss curve | Realistic training loss with a spike event. Annotate cause and recovery |

---

### Page 7: Modern Variants

| ID | Visual | Type | Description |
|----|--------|------|-------------|
| V7.1 | Efficient Attention Taxonomy | Tree/taxonomy diagram | Categories from Tay et al. with representative methods |
| V7.2 | Sparse Attention Patterns | Attention matrix diagrams | Longformer (window+global), BigBird (random+window+global). Show pattern matrices |
| V7.3 | FlashAttention Memory Hierarchy | GPU diagram | HBM vs SRAM with tiled computation. Show data movement |
| V7.4 | FlashAttention Tiling | Block computation diagram | How attention is computed tile by tile without materializing full matrix |
| V7.5 | MoE Routing | Token-to-expert diagram | Tokens routed to different experts through router. Show load distribution |
| V7.6 | ViT Pipeline | Image processing pipeline | Image -> patches -> linear embedding -> Transformer encoder -> classification |
| V7.7 | Mamba vs Transformer | Complexity comparison | Side-by-side: quadratic attention vs linear SSM. Show scaling behavior |
| V7.8 | Model Architecture Timeline | Timeline | 2017-2025: major Transformer variant milestones |

---

### Summary

| Page | Diagrams | Interactive | Static |
|------|----------|-------------|--------|
| 0 | 3 | 1 | 2 |
| 1 | 8 | 2 | 6 |
| 2 | 6 | 1 | 5 |
| 3 | 4 | 0 | 4 |
| 4 | 4 | 0 | 4 |
| 5 | 6 | 2 | 4 |
| 6 | 5 | 0 | 5 |
| 7 | 8 | 1 | 7 |
| **Total** | **44** | **7** | **37** |
