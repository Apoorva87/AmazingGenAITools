---
id: "llm-inference"
type: concept
depth: intermediate
confidence: 1
clusters:
  - "inference-optimization"
tags:
  - inference
  - production
  - latency
status: unread
---

# LLM Inference Engineering

**Depth**: intermediate | **Confidence**: ⭐ | **Status**: #unread

**Clusters**: [[Clusters/Inference Optimization|Inference Optimization]]

---

## Key Questions

- [ ] What are the key bottlenecks in serving LLMs at scale?
- [ ] How do batching strategies affect throughput vs latency trade-offs?

---

## Subtopics

- batching-strategies
- kv-cache
- model-sharding
- gpu-parallelization

---

## Relationships

- **depends_on** → [[Concepts/FlashAttention|FlashAttention]]
  - _FlashAttention is key to efficient inference_
- **contains** → [[Concepts/Batching Strategies|Batching Strategies]]
  - _Batching is a core inference optimization_
- **contains** → [[Concepts/Model Sharding & Parallelism|Model Sharding & Parallelism]]
  - _Sharding enables serving large models_
- **depends_on** → [[Concepts/GPU Memory Management|GPU Memory Management]]
  - _Memory management is critical for inference_
- **learned_from** → [[Resources/CS336 Stanford (Lectures 5-11)|CS336 Stanford (Lectures 5-11)]]
  - _Stanford inference lectures_
- **learned_from** → [[Resources/Understanding LLM Inference (article)|Understanding LLM Inference (article)]]
  - _LLM inference article_
- **enables** ← [[Concepts/Model Distillation|Model Distillation]]
  - _Distillation creates smaller models for faster inference_

---

## My Notes

_Add your notes here as you learn this concept..._

