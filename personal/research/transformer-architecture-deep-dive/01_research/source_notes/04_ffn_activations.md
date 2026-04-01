# Research Notes: Feed-Forward Networks & Activation Functions
## Sub-topic 4 of 7

### Key Concepts to Cover

1. **Position-Wise Feed-Forward Network (FFN)**
   - Applied independently to each position (token)
   - Two linear transformations with activation in between:
     FFN(x) = W_2 * activation(W_1 * x + b_1) + b_2
   - W_1: d_model -> d_ff (expansion), W_2: d_ff -> d_model (compression)
   - Standard expansion ratio: d_ff = 4 * d_model
   - Accounts for ~2/3 of Transformer parameters

2. **FFN as Key-Value Memory**
   - Geva et al. (2021): FFN first layer keys = W_1 rows, second layer values = W_2 columns
   - Each "key" activates on specific input patterns
   - Each "value" represents the information to inject into the residual stream
   - Implication: FFN stores factual knowledge, attention routes information
   - Mechanistic interpretability: neurons have interpretable meanings

3. **ReLU (Original Transformer)**
   - f(x) = max(0, x)
   - Simple but creates dead neurons (zero gradient for negative inputs)
   - Sparse activation: many neurons inactive for any given input
   - Used in original Transformer, BERT

4. **GELU (Gaussian Error Linear Unit)**
   - f(x) = x * Phi(x) where Phi is the standard Gaussian CDF
   - Approximation: f(x) ≈ 0.5x(1 + tanh(sqrt(2/pi)(x + 0.044715x^3)))
   - Smooth, non-monotonic near zero
   - Stochastic interpretation: multiply input by Bernoulli mask based on how extreme the value is
   - Used in GPT-2, BERT (later versions), most modern models pre-LLaMA

5. **Gated Linear Units (GLU) and SwiGLU**
   - GLU: f(x) = (xW_1) * sigmoid(xW_3) — element-wise gating
   - SwiGLU: f(x) = (x * W_1) * SiLU(x * W_3) where SiLU(x) = x * sigmoid(x)
   - Shazeer (2020): SwiGLU outperforms ReLU and GELU in Transformer FFN
   - Three weight matrices instead of two: W_1, W_2, W_3
   - To keep parameter count constant: reduce d_ff (e.g., d_ff = (2/3) * 4 * d_model)
   - Used in LLaMA, PaLM, Gemma, Mistral — standard in modern LLMs

6. **Expansion Ratio Design Choices**
   - Original: d_ff = 4 * d_model (expansion factor 4)
   - With SwiGLU: d_ff ≈ (8/3) * d_model to match parameter count
   - Some models use d_ff = 11008 for d_model = 4096 (LLaMA)
   - Trade-off: larger FFN = more capacity but more compute

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S001 (Attention Is All You Need) | FFN definition | Original formulation with ReLU |
| S011 (Shazeer GLU Variants) | SwiGLU derivation | Gated activation comparison experiments |
| S025 (Karpathy GPT) | FFN implementation | Code walkthrough |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S037 (Hendrycks GELU) | GELU paper | Mathematical definition, motivation |
| S062 (Geva FFN as memories) | Interpretability | FFN key-value memory interpretation |
| S032 (Umar Jamil LLaMA) | SwiGLU in practice | Modern FFN implementation |
| S049 (nanoGPT) | Code | MLP class with GELU |
| S002 (Annotated Transformer) | Code | Original FFN with ReLU |
| S034 (Raschka) | Code | Step-by-step FFN |

### Visual Resources Found
- FFN expansion/compression diagram: d_model -> d_ff -> d_model
- Activation function comparison plot: ReLU vs GELU vs SwiGLU
- GLU gating mechanism diagram
- FFN as key-value memory visualization (from Geva et al.)

### Code Examples Found
- Annotated Transformer: PositionwiseFeedForward class
- nanoGPT: MLP with GELU
- LLaMA implementation: SwiGLU FFN (3 weight matrices)
- Comparison snippet: all three activations in PyTorch

### Key Equations

```
FFN (original):
  FFN(x) = max(0, xW_1 + b_1)W_2 + b_2

GELU:
  GELU(x) = x * Phi(x) = x * 0.5 * (1 + erf(x/sqrt(2)))

SwiGLU FFN:
  FFN_SwiGLU(x) = (SiLU(xW_1) * xW_3)W_2
  where SiLU(x) = x * sigmoid(x)

Parameter count:
  Standard: 2 * d_model * d_ff
  SwiGLU:   3 * d_model * d_ff  (but d_ff is reduced)
```

### Teaching Sequence (Recommended)
1. FFN's role: what does it do after attention has mixed information? (intuition)
2. Position-wise independence: why each position gets the same FFN
3. Expansion-compression: d_model -> 4*d_model -> d_model as bottleneck-expansion
4. ReLU FFN implementation
5. GELU: smoother activation, probabilistic interpretation
6. GLU and SwiGLU: gating mechanism, why three matrices
7. FFN as key-value memory: interpretability perspective
8. Compare and benchmark: speed and quality of different activations

### Cross-links to Other Sub-topics
- -> Self-Attention: attention mixes tokens, FFN transforms representations
- -> Normalization: Pre-LN before FFN
- -> Encoder-Decoder: FFN in every Transformer block
- -> Modern Variants: MoE replaces single FFN with routed experts
- -> Training: FFN parameters dominate model size

### Pitfalls to Cover
- Dead ReLU neurons in deep Transformers
- SwiGLU parameter count: need to adjust d_ff to maintain params
- Numerical precision in GELU approximations
