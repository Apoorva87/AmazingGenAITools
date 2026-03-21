---
id: "self-attention"
type: concept
depth: intro
confidence: 1
clusters:
  - "transformer-foundations"
tags:
  - transformer
  - attention
  - core
status: unread
---

# Self-Attention

**Depth**: intro | **Confidence**: ⭐ | **Status**: #unread

**Clusters**: [[Clusters/Transformer Foundations|Transformer Foundations]]

---

## Key Questions

- [ ] How does self-attention compute relationships between all positions in a sequence?
- [ ] Why is self-attention O(n^2) in sequence length?

---

## Subtopics

- scaled-dot-product-attention
- query-key-value

---

## Relationships

- **learned_from** → [[Resources/Attention Is All You Need|Attention Is All You Need]]
  - _Self-attention introduced in original Transformer paper_
- **extends** ← [[Concepts/Multi-Head Attention|Multi-Head Attention]]
  - _MHA runs multiple self-attention heads in parallel_
- **extends** ← [[Concepts/FlashAttention|FlashAttention]]
  - _FlashAttention is an IO-aware implementation of exact attention_

---

## My Notes

_Add your notes here as you learn this concept..._

