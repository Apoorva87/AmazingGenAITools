# Processed: Inference Engineering Notes

**Source**: personal/learning/raw_notes/inference.md
**Processed**: 2026-03-19
**Concepts extracted**: 7
**Resources processed**: 8
**Connections created**: 15

---

## Concepts

### LLM Inference Engineering (`llm-inference`)
- **Depth**: intermediate
- **Cluster**: inference-optimization
- **Subtopics**: batching-strategies, kv-cache, model-sharding, gpu-parallelization
- **Key questions**:
  - What are the key bottlenecks in serving LLMs at scale?
  - How do batching strategies affect throughput vs latency trade-offs?
- **Relationships**:
  - depends_on → flash-attention, gpu-memory-management
  - contains → batching-strategies, model-sharding
  - learned_from → res-cs336-stanford, res-understanding-llm-inference

### Batching Strategies (`batching-strategies`)
- **Depth**: intermediate
- **Cluster**: inference-optimization
- **Key questions**:
  - How does continuous batching improve GPU utilization?
  - What is the difference between static and dynamic batching?
- **Relationships**:
  - part_of → llm-inference

### GPU Memory Management (`gpu-memory-management`)
- **Depth**: intermediate
- **Clusters**: inference-optimization, llm-hardware
- **Key questions**:
  - How does KV cache size affect concurrent session limits?
  - What strategies exist for managing VRAM during multi-user inference?
- **Relationships**:
  - related_to ← flash-attention
  - learned_from → res-gpu-perf-engineering, res-inside-nvidia-gpus

### Model Sharding & Parallelism (`model-sharding`)
- **Depth**: intermediate
- **Cluster**: inference-optimization
- **Key questions**:
  - When should you use tensor parallelism vs pipeline parallelism?
  - How does model sharding across GPUs affect inference latency?

### Model Distillation (`model-distillation`)
- **Depth**: intermediate
- **Cluster**: inference-optimization
- **Key questions**:
  - How does knowledge distillation transfer capabilities from large to small models?
  - What are the trade-offs between distillation and quantization?
- **Relationships**:
  - enables → llm-inference

---

## Resources

### CS336 Stanford (`res-cs336-stanford`)
- **URL**: https://buff.ly/9o4jRxl (shortened — unfetched)
- **Type**: course
- **Quality**: 4/5 — Stanford course covering inference engineering
- **Teaches concepts**: llm-inference

### GPU MODE (`res-gpu-mode`)
- **URL**: https://buff.ly/bPEHYL0 (shortened — unfetched)
- **Type**: course
- **Quality**: 4/5 — GPU programming community
- **Teaches concepts**: gpu-memory-management

### LLM Inference Patterns (`res-llm-inference-patterns`)
- **URL**: https://buff.ly/4ASDS5c (shortened — unfetched)
- **Type**: video
- **Teaches concepts**: llm-inference

### LLM Inference NVIDIA (`res-llm-inference-nvidia`)
- **URL**: https://buff.ly/muDMcor (shortened — unfetched)
- **Type**: video
- **Quality**: 4/5 — Official NVIDIA inference guide
- **Teaches concepts**: llm-inference

### GPU Performance Engineering (`res-gpu-perf-engineering`)
- **URL**: https://buff.ly/sfGJNMK (shortened — unfetched)
- **Type**: blog
- **Teaches concepts**: gpu-memory-management

### AI Performance Engineering (`res-ai-perf-engineering`)
- **URL**: https://buff.ly/8ey3GPa (shortened — unfetched)
- **Type**: blog
- **Teaches concepts**: llm-inference

### Inside NVIDIA GPUs (`res-inside-nvidia-gpus`)
- **URL**: https://buff.ly/wmgNwMg (shortened — unfetched)
- **Type**: blog
- **Teaches concepts**: gpu-memory-management

### Understanding LLM Inference (`res-understanding-llm-inference`)
- **URL**: https://buff.ly/NrNU3Qz (shortened — unfetched)
- **Type**: blog
- **Teaches concepts**: llm-inference

---

## Personal Notes

### Inference is the underserved skill (`note-inference-gap`)
- **Context**: File intro
- **Body**: Many courses teach AI & LLMs but very few touch on inference. Efficient inference is one of the largest barriers to LLMs in production. Batching, memory management, concurrent sessions, GPU saturation, sharding, MIG, and parallelization are key concepts. There is no clear step-by-step guide on AI perf engineering — best bet is to study core model pieces and the hardware they run on.

---

## New Connections Discovered

- llm-inference **depends_on** flash-attention — FlashAttention is key to efficient inference
- llm-inference **depends_on** gpu-memory-management — Memory management is critical
- model-distillation **enables** llm-inference — Smaller models for faster inference
- gpu-memory-management **related_to** flash-attention — FlashAttention optimizes GPU memory access
- model-sharding **related_to** large-scale-training — Both involve distributed computation

---

## Graph Stats (after update)

- Total nodes: 98
- Total edges: 77
- Nodes by type: concept=34, resource=60, note=4
- Clusters: inference-optimization (21 nodes), llm-hardware (9 nodes)

---

## Note on Unfetched URLs

All 8 URLs in this file use buff.ly shorteners and could not be resolved. The resource nodes contain inferred metadata from the surrounding notes context. Consider visiting these URLs manually to verify the final destinations and update the graph.
