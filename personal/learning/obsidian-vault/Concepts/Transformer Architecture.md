---
id: "transformer-architecture"
type: concept
depth: intro
confidence: 1
clusters:
  - "transformer-foundations"
tags:
  - transformer
  - architecture
  - deep-learning
status: unread
---

# Transformer Architecture

**Depth**: intro | **Confidence**: ⭐ | **Status**: #unread

**Clusters**: [[Clusters/Transformer Foundations|Transformer Foundations]]

---

## Key Questions

- [ ] What are the key components of the original Transformer?
- [ ] Why did decoder-only architectures become dominant for LLMs?

---

## Subtopics

- encoder-decoder
- layer-normalization
- feed-forward-network
- residual-connections

---

## Relationships

- **contains** → [[Concepts/Multi-Head Attention|Multi-Head Attention]]
  - _MHA is a core component of the Transformer_
- **contains** → [[Concepts/Positional Encoding|Positional Encoding]]
  - _Transformers need positional encoding for sequence order_
- **learned_from** → [[Resources/Attention Is All You Need|Attention Is All You Need]]
  - _Transformer architecture introduced here_
- **learned_from** → [[Resources/The Illustrated Transformer|The Illustrated Transformer]]
  - _Visual intuition for Transformer internals_
- **learned_from** → [[Resources/Understanding Transformer by Step-by-Step Math|Understanding Transformer by Step-by-Step Math]]
  - _Matrix math walkthrough_
- **learned_from** → [[Resources/Transformers from Scratch (Brandon Rohrer)|Transformers from Scratch (Brandon Rohrer)]]
  - _Matrix multiplication flows_
- **learned_from** → [[Resources/LLM Transformer Model Visually Explained (Interactive)|LLM Transformer Model Visually Explained (Interactive)]]
  - _Interactive GPT visualization_
- **depends_on** ← [[Concepts/Masked Language Modeling|Masked Language Modeling]]
  - _MLM uses the encoder side of the Transformer_
- **extends** ← [[Concepts/Mixture of Experts (MoE)|Mixture of Experts (MoE)]]
  - _MoE replaces dense FFN with sparse expert layers_

---

## My Notes

_Add your notes here as you learn this concept..._

