# Section Plan — Source Mapping
## Transformer Architecture Deep Dive

This document maps approved sources to specific sections in the master outline.

---

### Page 0: The Transformer — A Unified View

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 0.1 Introduction | S001 (original paper), S025 (Karpathy) | S003 (Alammar) |
| 0.2 Architecture Overview | S003 (Illustrated Transformer) | S001, S027 (3B1B) |
| 0.3 Big Picture: Processing Text | S025 (Karpathy GPT), S003 | S033 (Formal Algorithms) |
| 0.4 Navigation Guide | — (editorial) | — |

---

### Page 1: Self-Attention Mechanism

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 1.1.1 Fuzzy dictionary metaphor | S003 (Alammar), S026 (3B1B) | S050 (Weng Attention!) |
| 1.1.2 Why tokens talk | S027 (3B1B GPT intro) | S003 |
| 1.2.1 QKV framework | S001 (original paper) | S034 (Raschka), S044 (Bloem) |
| 1.2.2 Scaling factor | S001 | S034 (Raschka derivation) |
| 1.2.3 Softmax distribution | S001, S026 (3B1B) | S033 (Formal Algorithms) |
| 1.2.4 Multi-head attention | S001, S003 (Alammar diagrams) | S028 (Umar Jamil), S029 |
| 1.2.5 Self vs cross vs causal | S001, S002 (Annotated) | S025 (Karpathy: causal) |
| 1.2.6 Complexity analysis | S036 (Kipply), S008 (Tay survey) | S040 (EleutherAI math) |
| 1.3.1 Implement attention | S002 (Annotated), S034 (Raschka) | S025 (Karpathy) |
| 1.3.2 Implement MHA | S002, S049 (nanoGPT) | S029 (Umar Jamil) |
| 1.3.3 Causal mask | S025 (Karpathy), S049 | S002 |
| 1.3.4 KV cache | S036 (Kipply), S040 (EleutherAI) | S032 (Umar Jamil LLaMA) |
| 1.3.5 MQA and GQA | S060 (GQA paper) | S032 (Umar Jamil LLaMA) |
| 1.4 Going deeper | S035 (Nanda, interp) | S050 (Weng) |

---

### Page 2: Positional Encoding Deep Dive

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 2.1.1 Bag-of-words problem | S001 | S044 (Bloem) |
| 2.1.2 Permutation invariance | S044 (Bloem proof) | S004 (Weng) |
| 2.2.1 Sinusoidal PE | S001 | S030 (Umar Jamil), S051 (d2l.ai) |
| 2.2.2 Learned PE | S012 (BERT), S013 (GPT-2) | S002 (Annotated) |
| 2.2.3 Relative PE | S014 (T5) | S004 (Weng) |
| 2.2.4 RoPE | S005 (RoFormer), S006 (EleutherAI) | S032 (Umar Jamil LLaMA) |
| 2.2.5 ALiBi | S038 (ALiBi paper) | S004 (Weng) |
| 2.3.1 Implement sinusoidal | S002 (Annotated) | S051 (d2l.ai) |
| 2.3.2 Implement RoPE | S006 (EleutherAI code) | S032 (Umar Jamil) |
| 2.3.3 Length extrapolation | S038 (ALiBi experiments) | S005 (RoFormer) |

---

### Page 3: Normalization Techniques

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 3.1 Intuition | S047 (Ba LayerNorm) | S007 (Xiong) |
| 3.2.1 BN vs LN | S047 (Ba) | S004 (Weng) |
| 3.2.2 LayerNorm math | S047 (Ba) | S002 (Annotated) |
| 3.2.3 Post-LN | S001, S007 (Xiong analysis) | S002 |
| 3.2.4 Pre-LN | S007 (Xiong et al.) | S049 (nanoGPT code) |
| 3.2.5 RMSNorm | S021 (Zhang & Sennrich) | S032 (Umar Jamil LLaMA) |
| 3.3.1-3.3.3 Implementation | S049 (nanoGPT), S002 | S029 (Umar Jamil) |

---

### Page 4: FFN & Activation Functions

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 4.1 Intuition | S001 | S025 (Karpathy) |
| 4.2.1 FFN definition | S001 | S002 (Annotated), S033 |
| 4.2.2 Activations | S037 (GELU paper), S011 (SwiGLU) | S049 (nanoGPT) |
| 4.2.3 GLU family | S011 (Shazeer) | S032 (Umar Jamil LLaMA) |
| 4.2.4 FFN as memory | S062 (Geva et al.) | S035 (Nanda interp) |
| 4.3.1-4.3.2 Implementation | S002 (Annotated), S049 (nanoGPT) | S025 (Karpathy) |

---

### Page 5: Encoder-Decoder Architecture

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 5.1.1 Seq2seq to Transformer | S023 (Alammar seq2seq) | S050 (Weng) |
| 5.1.3 Architecture family tree | S012 (BERT), S013 (GPT-2), S014 (T5) | S039 (LLM survey) |
| 5.2.1 Transformer block | S001, S003 (Alammar) | S033 (Formal Alg.) |
| 5.2.2 Encoder stack | S001, S002 | S029 (Umar Jamil) |
| 5.2.3 Decoder stack | S001, S025 (Karpathy) | S024 (Alammar GPT-2) |
| 5.2.4 Residual stream | S035 (Nanda) | S044 (Bloem) |
| 5.2.5 Architecture variants | S012, S013, S014 | S043 (Alammar GPT-3), S039 |
| 5.3.1-5.3.3 Implementation | S002 (Annotated), S048 (minGPT), S049 (nanoGPT) | S025 (Karpathy), S029 |

---

### Page 6: Training Transformers

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 6.1 Intuition | S025 (Karpathy) | S001 |
| 6.2.1 LR schedules | S001 (inv sqrt), S015 (Kaplan) | S049 (nanoGPT cosine) |
| 6.2.2 Adam to AdamW | S022 (Loshchilov & Hutter) | S040 (EleutherAI math) |
| 6.2.3 Gradient clipping | S049 (nanoGPT) | S025 (Karpathy) |
| 6.2.4 Label smoothing | S001 | S002 (Annotated) |
| 6.2.5 Scaling laws | S015 (Kaplan), S016 (Chinchilla) | S039 (LLM survey) |
| 6.3.1-6.3.4 Implementation | S049 (nanoGPT) | S025 (Karpathy), S002 |
| 6.4 Going deeper | S039 (LLM survey), S036 (Kipply) | S061 (Weng distributed) |

---

### Page 7: Modern Transformer Variants

| Section | Primary Sources | Supporting Sources |
|---------|----------------|-------------------|
| 7.1 Intuition | S008 (Tay survey) | S004 (Weng) |
| 7.2.1 Taxonomy | S008 (Tay) | S004 (Weng) |
| 7.2.2 Sparse attention | S018 (Longformer), S042 (BigBird) | S004 (Weng) |
| 7.2.3 Linear attention | S041 (Performer) | S008 (Tay survey) |
| 7.2.4 FlashAttention | S009 (FA1), S010 (FA2) | S046 (Gordic explainer) |
| 7.2.5 MoE | S017 (Switch), S045 (HF blog) | S004 (Weng) |
| 7.2.6 ViT | S019 (ViT paper) | S059 (DeiT) |
| 7.2.7 SSM hybrids | S020 (Mamba), S058 (Jamba) | S004 (Weng) |
| 7.3.1-7.3.4 Implementation | S049 (nanoGPT FA), S054 (HF docs) | S045 (HF MoE blog) |
