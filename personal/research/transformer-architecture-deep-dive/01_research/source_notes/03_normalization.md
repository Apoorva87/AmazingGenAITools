# Research Notes: Normalization Techniques
## Sub-topic 3 of 7

### Key Concepts to Cover

1. **Why Normalization in Transformers**
   - Internal covariate shift: layer input distributions change during training
   - Gradient flow: normalization stabilizes gradient magnitudes across layers
   - Enables deeper networks and higher learning rates
   - Different from CNNs: batch dimension is not useful for variable-length sequences

2. **Layer Normalization (LayerNorm)**
   - Normalize across feature dimension (not batch dimension)
   - For input x of shape (batch, seq_len, d_model):
     - mu = mean(x, dim=-1), sigma = std(x, dim=-1)
     - x_norm = (x - mu) / (sigma + eps)
     - output = gamma * x_norm + beta (learnable affine parameters)
   - Batch-independent: same normalization at train and inference time
   - Contrast with BatchNorm: normalizes across batch + spatial, problematic for sequences

3. **Post-LN (Original Transformer)**
   - LayerNorm applied AFTER residual addition: LN(x + Sublayer(x))
   - Used in original "Attention Is All You Need"
   - Problem: gradient magnitudes vary across layers, requiring careful warmup
   - Can be unstable without learning rate warmup

4. **Pre-LN (GPT-2, Modern Standard)**
   - LayerNorm applied BEFORE sublayer: x + Sublayer(LN(x))
   - Gradient flows directly through residual path (identity shortcut)
   - Much more stable: can train without warmup
   - Xiong et al. (2020): formal analysis showing Pre-LN has well-behaved gradients
   - Trade-off: some evidence Pre-LN has slightly worse final quality at convergence

5. **RMSNorm (Root Mean Square Normalization)**
   - Simplifies LayerNorm by removing mean-centering:
     - RMS(x) = sqrt(mean(x^2))
     - x_norm = x / RMS(x)
     - output = gamma * x_norm
   - ~10-15% faster than LayerNorm (saves mean computation + shift)
   - Used in LLaMA, Gemma, Mistral, Qwen — standard in modern LLMs
   - Zhang & Sennrich (2019): shows mean centering is not necessary

6. **Other Normalization Variants**
   - GroupNorm: normalize within channel groups (less relevant for Transformers)
   - QK-Norm: normalize Q and K before dot product (prevents attention logit explosion)
   - DeepNorm: combination of Pre-LN with residual scaling for very deep models

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S007 (Xiong et al. 2020) | Pre-LN vs Post-LN analysis | Gradient flow proofs, warmup analysis |
| S021 (RMSNorm paper) | RMSNorm derivation | Mathematical justification, experiments |
| S047 (Ba et al. 2016) | Original LayerNorm | Foundation definition and motivation |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S032 (Umar Jamil LLaMA) | RMSNorm in practice | How modern LLMs use normalization |
| S029 (Umar Jamil Transformer) | Implementation | LayerNorm code walkthrough |
| S002 (Annotated Transformer) | Post-LN implementation | Original placement in code |
| S004 (Weng Transformer Family v2) | Taxonomy | Comparative overview |
| S049 (nanoGPT) | Pre-LN implementation | Modern LayerNorm placement |

### Visual Resources Found
- Pre-LN vs Post-LN: side-by-side architecture diagrams
- Gradient magnitude plots: showing Pre-LN stability advantage
- Normalization comparison table: BN vs LN vs RMSNorm
- Residual stream view: where normalization fits in information flow

### Code Examples Found
- PyTorch nn.LayerNorm: built-in implementation
- RMSNorm from scratch: ~10 lines of PyTorch
- nanoGPT: Pre-LN Transformer block
- Annotated Transformer: Post-LN block
- LLaMA implementation (HuggingFace): RMSNorm class

### Key Equations

```
LayerNorm:
  mu = (1/d) * sum(x_i)
  sigma = sqrt((1/d) * sum((x_i - mu)^2))
  LN(x) = gamma * (x - mu) / (sigma + eps) + beta

RMSNorm:
  RMS(x) = sqrt((1/d) * sum(x_i^2))
  RMSNorm(x) = gamma * x / RMS(x)

Post-LN block: output = LN(x + Attention(x))
Pre-LN block:  output = x + Attention(LN(x))
```

### Teaching Sequence (Recommended)
1. Why normalization? (intuition: keeping activations in a reasonable range)
2. Contrast BatchNorm vs LayerNorm — why batch dim is wrong for sequences
3. LayerNorm math and implementation
4. Post-LN: original Transformer placement + stability issues
5. Pre-LN: the fix, with gradient flow analysis from Xiong et al.
6. RMSNorm: simplification that works, with efficiency gains
7. Implement all three variants in PyTorch for comparison

### Cross-links to Other Sub-topics
- -> Self-Attention: normalization before attention in Pre-LN
- -> Encoder-Decoder: final LayerNorm after encoder stack
- -> Training: Pre-LN enables no-warmup training
- -> Modern Variants: RMSNorm in LLaMA-family models

### Pitfalls to Cover
- Post-LN without warmup: training divergence
- Numerical issues with small eps in mixed precision
- The Pre-LN vs Post-LN quality debate: stability vs final loss
