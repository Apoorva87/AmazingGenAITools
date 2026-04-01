# Master Outline
## Transformer Architecture — A Comprehensive Graduate-Level Deep Dive

### Structure

- **Format**: 8 interconnected HTML pages (1 main + 7 sub-topics)
- **Style**: Lilian Weng / Jay Alammar hybrid
- **Each page**: 3-layer model (Intuition -> Formalism -> Engineering)
- **Cross-linking**: Each page links to related sections in other pages

---

## Page 0: The Transformer — A Unified View (Main Narrative Page)

### 0.1 Introduction: Why Transformers Changed Everything
- The shift from recurrence to attention
- Timeline: RNNs -> Attention -> Transformers -> LLMs
- What this guide covers and how to navigate it

### 0.2 Architecture Overview
- Full architecture diagram (interactive)
- Component inventory: what each part does in one sentence
- Reading paths: sequential vs. topic-focused

### 0.3 The Big Picture: How a Transformer Processes Text
- Tokenization -> Embedding -> N Layers -> Prediction
- Residual stream view: layers as additive operations
- The forward pass in pseudocode

### 0.4 Navigating This Guide
- Recommended reading order for different backgrounds
- Prerequisites checklist
- Cross-reference map

**Sources**: S001, S003, S025, S027

---

## Page 1: Self-Attention Mechanism

### 1.1 Intuition Layer
- 1.1.1 Attention as looking up in a fuzzy dictionary
- 1.1.2 Why tokens need to talk to each other
- 1.1.3 Visual: attention as information routing

### 1.2 Formalism Layer
- 1.2.1 The QKV framework: definitions and dimensions
- 1.2.2 Dot-product similarity and the scaling factor
  - Derivation: variance of dot-products grows with d_k
  - Proof: Var(q.k) = d_k when q,k are unit Gaussian
- 1.2.3 Softmax and the attention distribution
- 1.2.4 Multi-head attention: parallel subspace attention
  - Head dimensions: d_k = d_v = d_model / n_heads
  - Concatenation and output projection
- 1.2.5 Self-attention vs cross-attention vs causal attention
  - Masking strategies
- 1.2.6 Complexity analysis: O(n^2 * d) time, O(n^2) space

### 1.3 Engineering Layer
- 1.3.1 Implementing scaled dot-product attention in PyTorch
- 1.3.2 Implementing multi-head attention
- 1.3.3 Causal mask implementation
- 1.3.4 KV cache for efficient inference
- 1.3.5 Multi-query and grouped-query attention
- 1.3.6 Benchmarking: attention FLOPs and memory

### 1.4 Going Deeper
- What different attention heads learn
- Attention entropy and collapse
- Further reading and references

**Sources**: S001, S002, S003, S025, S026, S028, S034, S036, S050

---

## Page 2: Positional Encoding Deep Dive

### 2.1 Intuition Layer
- 2.1.1 The bag-of-words problem: why order matters
- 2.1.2 Permutation invariance of self-attention (visual proof)
- 2.1.3 What properties should a good position encoding have?

### 2.2 Formalism Layer
- 2.2.1 Sinusoidal positional encoding
  - Frequency band decomposition
  - Relative position as rotation (linear transformation proof)
- 2.2.2 Learned positional embeddings
  - Trainable lookup table
  - Comparison with sinusoidal
- 2.2.3 Relative position encodings (Shaw et al., T5)
- 2.2.4 Rotary Position Embedding (RoPE)
  - Derivation from desired inner-product properties
  - 2D rotation matrices
  - Extension to d dimensions
- 2.2.5 ALiBi: attention bias without embeddings
  - Linear bias formulation
  - Per-head slope design

### 2.3 Engineering Layer
- 2.3.1 Implementing sinusoidal PE in PyTorch
- 2.3.2 Implementing RoPE in PyTorch
- 2.3.3 Length extrapolation experiments
- 2.3.4 NTK-aware scaling and YaRN for long context

### 2.4 Going Deeper
- The length generalization problem
- Position encoding in vision (2D considerations)
- Further reading

**Sources**: S001, S005, S006, S030, S038, S032, S004, S044

---

## Page 3: Normalization Techniques

### 3.1 Intuition Layer
- 3.1.1 Why deep networks need normalization
- 3.1.2 The internal covariate shift argument
- 3.1.3 Visual: activation distributions with and without normalization

### 3.2 Formalism Layer
- 3.2.1 Batch Normalization vs Layer Normalization
  - Why batch dim is wrong for variable-length sequences
- 3.2.2 Layer Normalization: math and properties
  - Per-feature statistics computation
  - Learnable affine parameters
- 3.2.3 Post-LN: original Transformer placement
  - Gradient flow analysis (Xiong et al.)
  - Why warmup is required
- 3.2.4 Pre-LN: the modern standard
  - Gradient magnitude analysis: bounded at all depths
  - No warmup needed
- 3.2.5 RMSNorm: dropping the mean
  - Mathematical simplification
  - Why it works: centering is redundant

### 3.3 Engineering Layer
- 3.3.1 Implementing LayerNorm from scratch
- 3.3.2 Implementing RMSNorm from scratch
- 3.3.3 Pre-LN vs Post-LN Transformer block code
- 3.3.4 Numerical stability in mixed precision

### 3.4 Going Deeper
- QK-Norm for attention stability
- DeepNorm for very deep models
- Further reading

**Sources**: S007, S021, S047, S032, S029, S002, S049

---

## Page 4: Feed-Forward Networks & Activation Functions

### 4.1 Intuition Layer
- 4.1.1 What happens between attention layers?
- 4.1.2 FFN as per-token transformation
- 4.1.3 The expansion-compression metaphor: project up, filter, project down

### 4.2 Formalism Layer
- 4.2.1 Position-wise FFN: two linear layers + activation
  - Parameter counts and dimensions
- 4.2.2 Activation functions: ReLU, GELU, SwiGLU
  - Mathematical definitions
  - Gradient properties
  - Sparsity characteristics
- 4.2.3 Gated Linear Units (GLU family)
  - Gating mechanism
  - Three-matrix formulation
  - Parameter budget adjustment
- 4.2.4 FFN as key-value memory (Geva et al.)
  - First layer rows as keys, second layer columns as values
  - Implications for knowledge storage

### 4.3 Engineering Layer
- 4.3.1 Implementing standard FFN in PyTorch
- 4.3.2 Implementing SwiGLU FFN
- 4.3.3 Activation function comparison: speed and memory benchmarks
- 4.3.4 Parameter count calculator

### 4.4 Going Deeper
- Sparse MoE as FFN replacement
- Mechanistic interpretability of FFN neurons
- Further reading

**Sources**: S001, S011, S025, S037, S062, S032, S049, S002

---

## Page 5: The Encoder-Decoder Architecture

### 5.1 Intuition Layer
- 5.1.1 From seq2seq with attention to the Transformer
- 5.1.2 The assembly line metaphor: encoder builds, decoder generates
- 5.1.3 Architecture family tree: enc-only, dec-only, enc-dec

### 5.2 Formalism Layer
- 5.2.1 Complete Transformer block
  - Attention + Add&Norm + FFN + Add&Norm
  - Residual connections and information preservation
- 5.2.2 Encoder stack
  - Bidirectional self-attention
  - Layer-by-layer refinement
- 5.2.3 Decoder stack
  - Causal self-attention
  - Cross-attention mechanism
  - Autoregressive generation
- 5.2.4 The residual stream interpretation
  - Each layer reads from and writes to the stream
  - Implications for mechanistic interpretability
- 5.2.5 Architecture variants deep dive
  - BERT (encoder-only): MLM objective, bidirectional context
  - GPT (decoder-only): causal LM, autoregressive generation
  - T5 (encoder-decoder): text-to-text framework

### 5.3 Engineering Layer
- 5.3.1 Building a Transformer block from components
- 5.3.2 Stacking blocks into encoder and decoder
- 5.3.3 Building a minimal GPT (following Karpathy)
- 5.3.4 Weight tying: embedding and output projection
- 5.3.5 Full model parameter counting

### 5.4 Going Deeper
- Why decoder-only won for LLMs
- The prefix-LM alternative
- Further reading

**Sources**: S001, S002, S003, S012, S013, S014, S023, S024, S025, S027, S029, S033, S043, S044, S048, S049

---

## Page 6: Training Transformers

### 6.1 Intuition Layer
- 6.1.1 Why Transformers are sensitive to hyperparameters
- 6.1.2 The warmup + decay recipe: why it works
- 6.1.3 The Chinchilla moment: rethinking how to spend compute

### 6.2 Formalism Layer
- 6.2.1 Learning rate schedules
  - Linear warmup derivation
  - Cosine decay formula
  - Inverse square root (original Transformer)
- 6.2.2 Optimizers: Adam to AdamW
  - Adam with momentum and adaptive LR
  - Why L2 != weight decay in Adam
  - AdamW formulation
- 6.2.3 Gradient clipping: global norm clipping
- 6.2.4 Label smoothing: soft targets
- 6.2.5 Scaling laws
  - Kaplan power laws
  - Chinchilla optimal frontier
  - Implications for model design

### 6.3 Engineering Layer
- 6.3.1 Implementing a custom LR scheduler (warmup + cosine)
- 6.3.2 Mixed precision training with PyTorch AMP
- 6.3.3 Gradient accumulation for large effective batch sizes
- 6.3.4 Complete training loop assembly
- 6.3.5 Monitoring: loss curves, gradient norms, learning rate

### 6.4 Going Deeper
- Training instabilities at scale: loss spikes, z-loss
- Distributed training: data parallelism, model parallelism (overview)
- Further reading

**Sources**: S001, S015, S016, S022, S025, S039, S040, S049, S002, S036

---

## Page 7: Modern Transformer Variants

### 7.1 Intuition Layer
- 7.1.1 The quadratic wall: why standard attention doesn't scale
- 7.1.2 Three strategies: make it sparse, make it linear, make it fast
- 7.1.3 Beyond NLP: Transformers for vision and beyond

### 7.2 Formalism Layer
- 7.2.1 Efficient attention taxonomy (Tay et al.)
- 7.2.2 Sparse attention: Longformer and BigBird
  - Attention patterns: local, global, random
  - Complexity analysis
- 7.2.3 Linear attention and Performer
  - Kernel trick on attention
  - FAVOR+ random features
- 7.2.4 FlashAttention
  - GPU memory hierarchy: HBM vs SRAM
  - Tiling algorithm
  - Recomputation vs materialization
  - Why it is exact (not approximate)
- 7.2.5 Mixture-of-Experts (MoE)
  - Router design and top-k selection
  - Load balancing loss
  - Switch Transformer: simplification to top-1
  - Active vs total parameters
- 7.2.6 Vision Transformers (ViT)
  - Patch embedding
  - CLS token and position embeddings
  - ViT vs CNN comparison
- 7.2.7 State-space model hybrids
  - Mamba: selective state spaces
  - Hybrid architectures: attention + SSM layers
  - Linear-time inference

### 7.3 Engineering Layer
- 7.3.1 Using FlashAttention in PyTorch (torch.nn.functional.scaled_dot_product_attention)
- 7.3.2 Implementing a simple sparse attention pattern
- 7.3.3 MoE routing implementation sketch
- 7.3.4 ViT patch embedding implementation

### 7.4 Going Deeper
- The future of attention: will it survive?
- Context length frontier: 128K to 1M+
- Multimodal Transformers
- Further reading

**Sources**: S004, S008, S009, S010, S017, S018, S019, S020, S041, S042, S045, S046, S058, S060

---

## Summary: Section Count and Coverage

| Page | Sections | Sources | LOs |
|------|----------|---------|-----|
| 0. Main Narrative | 4 | 4 | — |
| 1. Self-Attention | 4 (16 sub) | 9 | 6 |
| 2. Positional Encoding | 4 (13 sub) | 8 | 6 |
| 3. Normalization | 4 (12 sub) | 7 | 5 |
| 4. FFN & Activations | 4 (11 sub) | 9 | 5 |
| 5. Encoder-Decoder | 4 (14 sub) | 16 | 5 |
| 6. Training | 4 (13 sub) | 10 | 5 |
| 7. Modern Variants | 4 (14 sub) | 14 | 6 |
| **Total** | **32 main** | **52 unique** | **38** |
