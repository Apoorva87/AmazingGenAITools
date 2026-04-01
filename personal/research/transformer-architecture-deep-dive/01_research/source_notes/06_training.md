# Research Notes: Training Transformers
## Sub-topic 6 of 7

### Key Concepts to Cover

1. **Learning Rate Schedules**
   - **Linear Warmup**: gradually increase LR from 0 to peak over warmup_steps
     - Why: prevents early gradient explosion, especially with Post-LN
     - Typical: 1-5% of total training steps
   - **Cosine Decay**: after warmup, decay LR following cosine curve to min_lr
     - LR(t) = min_lr + 0.5 * (max_lr - min_lr) * (1 + cos(pi * t / T))
   - **Inverse Square Root**: LR = d_model^(-0.5) * min(step^(-0.5), step * warmup^(-1.5))
     - Used in original Transformer
   - Modern practice: warmup + cosine decay (GPT-3, LLaMA, etc.)

2. **Optimizers**
   - **Adam**: adaptive learning rate with momentum, standard for Transformers
     - m_t = beta1 * m_{t-1} + (1-beta1) * g_t (first moment)
     - v_t = beta2 * v_{t-1} + (1-beta2) * g_t^2 (second moment)
     - Standard: beta1=0.9, beta2=0.95 or 0.999, eps=1e-8
   - **AdamW**: decoupled weight decay (Loshchilov & Hutter 2019)
     - Key insight: L2 regularization != weight decay in adaptive optimizers
     - theta_t = theta_{t-1} - lr * (m_t / sqrt(v_t) + lambda * theta_{t-1})
     - Standard: lambda = 0.1 for LLMs
   - **LAMB**: layer-wise adaptive large batch optimizer
     - Enables very large batch sizes (32K+)

3. **Gradient Clipping**
   - Clip gradient norm to max value (typically 1.0)
   - Prevents gradient explosion in deep Transformers
   - Global norm clipping: scale all gradients if total norm exceeds threshold
   - Critical for training stability

4. **Mixed Precision Training**
   - FP16 (float16): 2x memory savings, faster matmul on modern GPUs
   - BF16 (bfloat16): same exponent range as FP32, less precision — preferred when available
   - Loss scaling: multiply loss by large constant to prevent gradient underflow in FP16
   - Master weights kept in FP32: accumulate small gradient updates accurately
   - Modern practice: BF16 on A100+/H100 (no loss scaling needed)

5. **Label Smoothing**
   - Instead of hard targets (0 or 1), use soft targets: (1-eps) for correct, eps/(V-1) for others
   - Typical eps = 0.1
   - Prevents overconfident predictions, acts as regularizer
   - Used in original Transformer, but less common in modern LLMs

6. **Gradient Accumulation**
   - Simulate large batch sizes on limited GPU memory
   - Accumulate gradients over N micro-batches, then update
   - effective_batch_size = micro_batch_size * accumulation_steps * n_gpus

7. **Scaling Laws**
   - **Kaplan et al. (2020)**: loss scales as power law with compute, data, and parameters
     - L(N) ~ N^(-0.076) for parameters
     - Larger models are more sample-efficient
   - **Chinchilla (Hoffmann et al. 2022)**: optimal allocation of compute budget
     - Params and tokens should scale equally: N_opt ~ C^0.5, D_opt ~ C^0.5
     - Most LLMs before Chinchilla were undertrained
     - LLaMA followed Chinchilla: smaller models, more data

8. **Training Instability at Scale**
   - Loss spikes: sudden increase in loss, often recoverable
   - Causes: bad data batches, gradient explosion, embedding norm growth
   - Mitigations: gradient clipping, z-loss, embedding norm regularization
   - PaLM paper: detailed discussion of training instabilities at scale

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S001 (Attention Is All You Need) | Original training recipe | LR schedule, optimizer, label smoothing |
| S022 (AdamW paper) | Optimizer | Weight decay decoupling derivation |
| S015 (Kaplan Scaling Laws) | Scaling | Power-law relationships |
| S016 (Chinchilla) | Optimal scaling | Compute-optimal training |
| S025 (Karpathy GPT) | Training loop | Complete implementation walkthrough |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S049 (nanoGPT) | Code | Full training loop with all tricks |
| S040 (EleutherAI Transformer Math) | Compute math | FLOP estimation, memory budgets |
| S036 (Kipply inference) | Performance | Arithmetic of training and inference |
| S039 (LLM Survey) | Overview | Training recipe comparison across models |
| S061 (Weng distributed) | Distributed training | Context for large-scale training |
| S002 (Annotated Transformer) | Code | Original training loop |

### Visual Resources Found
- Learning rate schedule plot: warmup + cosine decay
- Scaling law plots: loss vs compute/params/data
- Chinchilla optimal frontier
- Training loss curve with loss spikes
- Mixed precision training diagram: forward (FP16) + backward (FP16) + update (FP32)

### Code Examples Found
- nanoGPT: Complete training loop (gradient accumulation, mixed precision, cosine LR)
- Karpathy video: Training loop from scratch
- Annotated Transformer: Training with label smoothing
- PyTorch CosineAnnealingLR + linear warmup custom scheduler

### Key Equations

```
Cosine LR:
  LR(t) = min_lr + 0.5*(max_lr - min_lr)*(1 + cos(pi * t/T))

AdamW update:
  m = beta1*m + (1-beta1)*grad
  v = beta2*v + (1-beta2)*grad^2
  m_hat = m / (1 - beta1^t)
  v_hat = v / (1 - beta2^t)
  param = param - lr*(m_hat/(sqrt(v_hat)+eps) + wd*param)

Scaling law (Kaplan):
  L(N) = (N_c / N)^alpha_N  where alpha_N ≈ 0.076
  L(D) = (D_c / D)^alpha_D  where alpha_D ≈ 0.095

Chinchilla optimal:
  N_opt ≈ 0.6 * C^0.5
  D_opt ≈ 0.6 * C^0.5  (in appropriate units)
```

### Teaching Sequence (Recommended)
1. Why Transformers are hard to train: sensitivity to hyperparameters (intuition)
2. Learning rate warmup + cosine decay: the standard recipe
3. Adam and AdamW: why decoupled weight decay matters
4. Gradient clipping: preventing explosions
5. Mixed precision: FP16 vs BF16, loss scaling
6. Gradient accumulation: simulating large batches
7. Put it all together: implement a complete training loop
8. Scaling laws: how loss predictably decreases with compute
9. Chinchilla: how to spend your compute budget optimally
10. Training instabilities at scale: what goes wrong and how to fix it

### Cross-links to Other Sub-topics
- -> Self-Attention: attention can cause gradient issues (softmax saturation)
- -> Normalization: Pre-LN enables no-warmup training
- -> Encoder-Decoder: architecture determines objective (MLM vs CLM)
- -> Modern Variants: FlashAttention reduces training memory; MoE changes scaling dynamics

### Pitfalls to Cover
- Using Adam instead of AdamW (L2 reg != weight decay)
- Too short warmup causing early divergence
- FP16 gradient underflow without loss scaling
- Ignoring Chinchilla: training too-large models on too-little data
- Not monitoring gradient norms for early warning of instability
