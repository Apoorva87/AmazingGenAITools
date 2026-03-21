---
id: "flash-attention"
type: concept
depth: intermediate
confidence: 1
clusters:
  - "inference-optimization"
  - "transformer-foundations"
tags:
  - attention
  - memory
  - gpu
  - io-awareness
status: unread
---

# FlashAttention

**Depth**: intermediate | **Confidence**: ⭐ | **Status**: #unread

**Clusters**: [[Clusters/Inference Optimization|Inference Optimization]], [[Clusters/Transformer Foundations|Transformer Foundations]]

---

## Key Questions

- [ ] How does FlashAttention reduce memory from O(n^2) to O(n) via tiling?
- [ ] Why is IO-awareness key to FlashAttention performance on GPU?

---

## Subtopics

_None identified_

---

## Relationships

- **extends** → [[Concepts/Self-Attention|Self-Attention]]
  - _FlashAttention is an IO-aware implementation of exact attention_
- **related_to** → [[Concepts/GPU Memory Management|GPU Memory Management]]
  - _FlashAttention optimizes GPU memory access patterns_
- **learned_from** → [[Resources/FlashAttention - Fast and Memory-Efficient Exact Attention|FlashAttention: Fast and Memory-Efficient Exact Attention]]
  - _FlashAttention paper_
- **depends_on** ← [[Concepts/LLM Inference Engineering|LLM Inference Engineering]]
  - _FlashAttention is key to efficient inference_

---

## My Notes

_Add your notes here as you learn this concept..._

