# Learning Objectives
## Transformer Architecture — Graduate-Level Deep Dive

### Global Learning Objectives

By completing this learning resource, you will be able to:

1. **Explain** the complete Transformer architecture from first principles, including the mathematical foundations, design decisions, and engineering trade-offs.

2. **Implement** a working Transformer model from scratch in PyTorch, including attention, positional encoding, normalization, and feed-forward layers.

3. **Analyze** attention patterns, gradient flow, and training dynamics to diagnose and fix common Transformer training issues.

4. **Compare** architectural variants (encoder-only, decoder-only, encoder-decoder) and justify which to use for a given task.

5. **Evaluate** modern efficiency techniques (FlashAttention, sparse attention, MoE, SSM hybrids) and assess their trade-offs.

6. **Apply** scaling laws and training best practices to plan a Transformer training run.

---

### Per-Page Learning Objectives

#### Page 1: Self-Attention Mechanism
- LO-1.1: Derive scaled dot-product attention from the soft dictionary lookup metaphor
- LO-1.2: Explain why the 1/sqrt(d_k) scaling factor is necessary (variance analysis)
- LO-1.3: Implement single-head and multi-head attention in PyTorch from scratch
- LO-1.4: Explain causal masking and implement it for autoregressive generation
- LO-1.5: Calculate the FLOPs and memory cost of attention for a given sequence length
- LO-1.6: Describe how KV cache works and calculate its memory footprint

#### Page 2: Positional Encoding Deep Dive
- LO-2.1: Prove that self-attention is permutation-invariant and explain why position info is needed
- LO-2.2: Derive the sinusoidal positional encoding and explain its relative position property
- LO-2.3: Derive RoPE from the requirement that dot-product depends only on relative position
- LO-2.4: Implement sinusoidal PE, learned PE, and RoPE in PyTorch
- LO-2.5: Compare ALiBi with embedding-based approaches for length generalization
- LO-2.6: Explain the length extrapolation problem and modern mitigation strategies

#### Page 3: Normalization Techniques
- LO-3.1: Explain why Transformers use LayerNorm instead of BatchNorm
- LO-3.2: Analyze the gradient flow difference between Pre-LN and Post-LN placement
- LO-3.3: Derive RMSNorm and explain why removing mean-centering works
- LO-3.4: Implement LayerNorm and RMSNorm from scratch in PyTorch
- LO-3.5: Predict the training stability implications of normalization placement choices

#### Page 4: Feed-Forward Networks & Activation Functions
- LO-4.1: Explain the role of the FFN sublayer in a Transformer block
- LO-4.2: Describe the FFN as key-value memory interpretation
- LO-4.3: Compare ReLU, GELU, and SwiGLU mathematically and experimentally
- LO-4.4: Implement standard FFN and SwiGLU FFN in PyTorch
- LO-4.5: Calculate parameter counts for standard vs gated FFN variants

#### Page 5: The Encoder-Decoder Architecture
- LO-5.1: Trace information flow through a complete encoder-decoder Transformer
- LO-5.2: Explain the residual stream interpretation of Transformer layers
- LO-5.3: Implement a complete Transformer block (attention + norm + FFN + residual)
- LO-5.4: Compare encoder-only, decoder-only, and encoder-decoder architectures with concrete task examples
- LO-5.5: Build a minimal working GPT model in PyTorch

#### Page 6: Training Transformers
- LO-6.1: Design a learning rate schedule with warmup and cosine decay
- LO-6.2: Explain why AdamW is preferred over Adam with L2 regularization
- LO-6.3: Implement a complete training loop with mixed precision, gradient clipping, and gradient accumulation
- LO-6.4: Use scaling laws to predict the loss of a model given compute budget
- LO-6.5: Diagnose common training instabilities (loss spikes, gradient explosion)

#### Page 7: Modern Transformer Variants
- LO-7.1: Classify efficient attention methods using the Tay et al. taxonomy
- LO-7.2: Explain how FlashAttention achieves exact attention with reduced memory
- LO-7.3: Describe MoE routing and the load-balancing challenge
- LO-7.4: Explain the ViT approach to applying Transformers to images
- LO-7.5: Compare attention-based and SSM-based sequence modeling and explain hybrid architectures
- LO-7.6: Assess which modern techniques are practical vs. theoretical curiosities

---

Total learning objectives: 33
