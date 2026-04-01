# Research Notes: Positional Encoding Deep Dive
## Sub-topic 2 of 7

### Key Concepts to Cover

1. **Why Position Matters**
   - Self-attention is permutation-invariant: Attention(PQ, PK, PV) = P * Attention(Q, K, V)
   - Without position info, "dog bites man" = "man bites dog"
   - Position encoding breaks symmetry and provides ordering information

2. **Sinusoidal Positional Encoding (Original Transformer)**
   - PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
   - PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
   - Why sin/cos: any relative position can be represented as linear combination
   - Frequency bands: different dimensions encode position at different scales
   - Added (not concatenated) to token embeddings

3. **Learned Positional Embeddings**
   - Trainable embedding table: E[pos] for pos in [0, max_length-1]
   - Used in BERT, GPT-2
   - Pros: can learn task-specific patterns; Cons: fixed max length, no extrapolation
   - Empirically similar to sinusoidal in original Transformer experiments

4. **Relative Position Encodings**
   - Encode relative distance (i-j) instead of absolute position
   - Shaw et al. (2018): learnable relative position bias
   - T5 relative position bias: bucketed log-scale distances
   - Advantages: better length generalization, translation invariance

5. **Rotary Position Embedding (RoPE)**
   - Core idea: encode position through rotation of Q/K vectors
   - f(q, pos_m) . f(k, pos_n) depends only on (q . k) and (m - n)
   - 2D rotation matrix applied to consecutive dimension pairs
   - Elegant: relative position emerges naturally from absolute encoding
   - Used in LLaMA, PaLM, Gemma, Mistral, Qwen — dominant in modern LLMs
   - Implementation: element-wise multiply with cos/sin, then combine

6. **ALiBi (Attention with Linear Biases)**
   - No position embedding at all
   - Add linear bias: -m * |i - j| to attention scores (before softmax)
   - Per-head slopes m: geometric sequence from 2^(-8/n_heads) to 2^(-8)
   - Strong length generalization: train short, test long
   - Used in BLOOM, MPT

7. **Length Extrapolation Problem**
   - Models fail on sequences longer than training length
   - Sinusoidal: theoretically generalizes but doesn't in practice
   - Learned embeddings: hard-capped at max training length
   - RoPE + NTK-aware scaling: extend context by modifying frequency base
   - YaRN, LongRoPE: more sophisticated RoPE scaling methods

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S001 (Attention Is All You Need) | Sinusoidal PE definition | Original formulation and motivation |
| S005 (RoFormer) | RoPE mathematical derivation | Full rotation-based derivation |
| S006 (EleutherAI RoPE blog) | RoPE intuition + code | Bridging paper to implementation |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S030 (Umar Jamil PE video) | Visual explanation | Sinusoidal encoding walkthrough |
| S038 (ALiBi paper) | Linear biases | Alternative approach, extrapolation results |
| S032 (Umar Jamil LLaMA) | RoPE in practice | How RoPE is used in production models |
| S004 (Weng Transformer Family v2) | Survey | Comparative taxonomy of position methods |
| S044 (Bloem guide) | Mathematical treatment | Clear derivation of sinusoidal properties |
| S051 (d2l.ai) | Textbook treatment | Pedagogical sequencing |

### Visual Resources Found
- Sinusoidal frequency bands: heatmap visualization (d2l.ai)
- RoPE rotation: 2D rotation animation (EleutherAI blog)
- ALiBi: attention bias matrix visualization
- Comparison diagram: absolute vs relative vs rotary vs ALiBi

### Code Examples Found
- EleutherAI blog: RoPE implementation in PyTorch
- nanoGPT: learned position embeddings
- LLaMA source (HuggingFace): RoPE with precomputed frequencies
- Annotated Transformer: sinusoidal PE class

### Key Equations

```
Sinusoidal:
  PE(pos, 2i)   = sin(pos / 10000^(2i/d))
  PE(pos, 2i+1) = cos(pos / 10000^(2i/d))

RoPE (for dimension pair):
  f(x, pos) = [[cos(pos*theta), -sin(pos*theta)],
               [sin(pos*theta),  cos(pos*theta)]] @ [x_2i, x_2i+1]

  <f(q,m), f(k,n)> = g(q, k, m-n)  -- relative position emerges!

ALiBi:
  attention_scores += -m * |i - j|  for each head with slope m
```

### Teaching Sequence (Recommended)
1. Show that self-attention is permutation-invariant (intuition: bag of words problem)
2. Introduce sinusoidal PE with frequency-band visualization
3. Derive the relative-position property of sinusoidal PE
4. Discuss learned embeddings (simpler but limited)
5. Motivate relative position: why absolute can be wasteful
6. Derive RoPE from first principles (rotation in 2D, extend to d dimensions)
7. Implement RoPE in PyTorch
8. Compare ALiBi as a radical simplification
9. Length extrapolation experiments and scaling methods

### Cross-links to Other Sub-topics
- -> Self-Attention: PE breaks permutation invariance of attention
- -> Encoder-Decoder: different PE needs for bidirectional vs causal
- -> Modern Variants: RoPE + NTK scaling for long context models
- -> Training: position embedding warmup, long-context fine-tuning

### Pitfalls to Cover
- Extrapolation failure: attention score explosion beyond training length
- Forgetting to scale RoPE frequencies for long context fine-tuning
- Absolute PE making models fragile to input length changes
