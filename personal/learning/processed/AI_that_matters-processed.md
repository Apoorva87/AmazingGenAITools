# Processed: AI That Matters

**Source**: personal/learning/raw_notes/AI_that_matters.md
**Processed**: 2026-03-19
**Concepts extracted**: 26
**Resources processed**: 32
**Connections created**: 50+

---

## Concepts

### Self-Attention (`self-attention`)
- **Depth**: intro
- **Cluster**: transformer-foundations
- **Subtopics**: scaled-dot-product-attention, query-key-value
- **Key questions**:
  - How does self-attention compute relationships between all positions in a sequence?
  - Why is self-attention O(n^2) in sequence length?
- **Relationships**:
  - extended_by → multi-head-attention
  - learned_from → res-attention-is-all-you-need

### Multi-Head Attention (`multi-head-attention`)
- **Depth**: intro
- **Cluster**: transformer-foundations
- **Key questions**:
  - Why use multiple attention heads instead of a single one?
  - How do different heads learn different relationship patterns?
- **Relationships**:
  - extends → self-attention
  - extended_by → multi-latent-attention

### Transformer Architecture (`transformer-architecture`)
- **Depth**: intro
- **Cluster**: transformer-foundations
- **Subtopics**: encoder-decoder, layer-normalization, feed-forward-network, residual-connections
- **Key questions**:
  - What are the key components of the original Transformer?
  - Why did decoder-only architectures become dominant for LLMs?
- **Relationships**:
  - contains → multi-head-attention, positional-encoding
  - extended_by → mixture-of-experts

### Rotary Position Embedding (`rotary-position-embedding`)
- **Depth**: intermediate
- **Cluster**: transformer-foundations
- **Key questions**:
  - How does RoPE encode relative position via rotation matrices?
  - Why has RoPE become the default positional encoding for modern LLMs?
- **Relationships**:
  - specializes → positional-encoding
  - learned_from → res-roformer

### Masked Language Modeling (`masked-language-modeling`)
- **Depth**: intermediate
- **Cluster**: transformer-foundations
- **Relationships**:
  - depends_on → transformer-architecture
  - learned_from → res-bert

### In-Context Learning (`in-context-learning`)
- **Depth**: intermediate
- **Clusters**: scaling-and-training, reasoning-and-agents
- **Relationships**:
  - depends_on → scaling-laws
  - extended_by → chain-of-thought, retrieval-augmented-generation
  - learned_from → res-gpt3

### Neural Scaling Laws (`scaling-laws`)
- **Depth**: intermediate
- **Cluster**: scaling-and-training
- **Subtopics**: power-law, compute-optimal-training
- **Relationships**:
  - extended_by → compute-optimal-training
  - learned_from → res-scaling-laws

### Compute-Optimal Training (`compute-optimal-training`)
- **Depth**: intermediate
- **Cluster**: scaling-and-training
- **Relationships**:
  - extends → scaling-laws
  - learned_from → res-chinchilla

### FlashAttention (`flash-attention`)
- **Depth**: intermediate
- **Clusters**: inference-optimization, transformer-foundations
- **Relationships**:
  - extends → self-attention
  - related_to → gpu-memory-management
  - learned_from → res-flash-attention

### Retrieval-Augmented Generation (`retrieval-augmented-generation`)
- **Depth**: intermediate
- **Cluster**: representation-and-data
- **Relationships**:
  - extends → in-context-learning
  - learned_from → res-rag

### Instruction Tuning (`instruction-tuning`)
- **Depth**: intermediate
- **Cluster**: alignment-and-post-training
- **Relationships**:
  - enables → rlhf
  - learned_from → res-instructgpt

### RLHF (`rlhf`)
- **Depth**: intermediate
- **Cluster**: alignment-and-post-training
- **Subtopics**: reward-modeling, ppo, direct-preference-optimization
- **Relationships**:
  - contrasts_with ← direct-preference-optimization
  - extended_by → constitutional-ai, rl-for-reasoning
  - learned_from → res-instructgpt

### Direct Preference Optimization (`direct-preference-optimization`)
- **Depth**: intermediate
- **Cluster**: alignment-and-post-training
- **Relationships**:
  - contrasts_with → rlhf
  - learned_from → res-dpo

### Chain-of-Thought Prompting (`chain-of-thought`)
- **Depth**: intermediate
- **Cluster**: reasoning-and-agents
- **Relationships**:
  - extends → in-context-learning
  - extended_by → react-framework, rl-for-reasoning
  - learned_from → res-chain-of-thought

### ReAct Framework (`react-framework`)
- **Depth**: intermediate
- **Cluster**: reasoning-and-agents
- **Relationships**:
  - extends → chain-of-thought
  - learned_from → res-react

### RL for Reasoning (`rl-for-reasoning`)
- **Depth**: research
- **Cluster**: reasoning-and-agents
- **Relationships**:
  - extends → rlhf, chain-of-thought
  - learned_from → res-deepseek-r1

### Mixture of Experts (`mixture-of-experts`)
- **Depth**: intermediate
- **Cluster**: mixture-of-experts
- **Subtopics**: expert-routing, load-balancing, top-k-gating
- **Relationships**:
  - extends → transformer-architecture
  - learned_from → res-sparse-gated-moe, res-switch-transformers, res-mixtral, res-glam

### Sparse Upcycling (`sparse-upcycling`)
- **Depth**: research
- **Cluster**: mixture-of-experts
- **Relationships**:
  - enables → mixture-of-experts
  - learned_from → res-sparse-upcycling

### Platonic Representation Hypothesis (`platonic-representation`)
- **Depth**: research
- **Cluster**: representation-and-data
- **Relationships**:
  - related_to → scaling-laws
  - learned_from → res-platonic-representation

### Synthetic Data Training (`synthetic-data-training`)
- **Depth**: intermediate
- **Cluster**: representation-and-data
- **Relationships**:
  - related_to → compute-optimal-training
  - learned_from → res-textbooks-all-you-need

### Mechanistic Interpretability (`mechanistic-interpretability`)
- **Depth**: intermediate
- **Cluster**: mechanistic-interpretability
- **Subtopics**: sparse-autoencoders, feature-circuits, polysemanticity
- **Relationships**:
  - learned_from → res-scaling-monosemanticity, res-mapping-the-mind

### Large-Scale Training Orchestration (`large-scale-training`)
- **Depth**: intermediate
- **Cluster**: scaling-and-training
- **Relationships**:
  - related_to → model-sharding
  - learned_from → res-palm

---

## Resources

### Attention Is All You Need (`res-attention-is-all-you-need`)
- **URL**: https://arxiv.org/abs/1706.03762
- **Type**: paper
- **Quality**: 5/5 — Foundational paper that introduced the Transformer architecture
- **Descriptiveness**: high — Detailed architecture description with equations
- **Teaches concepts**: self-attention, multi-head-attention, transformer-architecture

### The Illustrated Transformer (`res-illustrated-transformer`)
- **URL**: https://jalammar.github.io/illustrated-transformer/
- **Type**: blog
- **Quality**: 5/5 — Excellent visual explanations of transformer internals
- **Descriptiveness**: high — Step-by-step visual walkthrough with diagrams
- **Teaches concepts**: transformer-architecture

### BERT (`res-bert`)
- **URL**: https://arxiv.org/abs/1810.04805
- **Type**: paper
- **Quality**: 5/5 — Introduced masked language modeling and bidirectional pre-training
- **Teaches concepts**: masked-language-modeling

### GPT-3 (`res-gpt3`)
- **URL**: https://arxiv.org/abs/2005.14165
- **Type**: paper
- **Quality**: 5/5 — Established in-context learning as a paradigm
- **Teaches concepts**: in-context-learning

### Scaling Laws (`res-scaling-laws`)
- **URL**: https://arxiv.org/abs/2001.08361
- **Type**: paper
- **Quality**: 5/5 — First clean empirical scaling framework
- **Teaches concepts**: scaling-laws

### Chinchilla (`res-chinchilla`)
- **URL**: https://arxiv.org/abs/2203.15556
- **Type**: paper
- **Quality**: 5/5 — Changed how the field thinks about data vs parameters
- **Teaches concepts**: compute-optimal-training

### LLaMA (`res-llama`)
- **URL**: https://arxiv.org/abs/2302.13971
- **Type**: paper
- **Quality**: 5/5 — Triggered the open-weight era

### RoFormer (`res-roformer`)
- **URL**: https://arxiv.org/abs/2104.09864
- **Type**: paper
- **Quality**: 4/5 — Introduced the now-standard RoPE positional encoding
- **Teaches concepts**: rotary-position-embedding

### FlashAttention (`res-flash-attention`)
- **URL**: https://arxiv.org/abs/2205.14135
- **Type**: paper
- **Quality**: 5/5 — Enabled long context windows and efficient inference
- **Teaches concepts**: flash-attention

### RAG (`res-rag`)
- **URL**: https://arxiv.org/abs/2005.11401
- **Type**: paper
- **Quality**: 4/5 — Foundational RAG paper
- **Teaches concepts**: retrieval-augmented-generation

### InstructGPT (`res-instructgpt`)
- **URL**: https://arxiv.org/abs/2203.02155
- **Type**: paper
- **Quality**: 5/5 — The modern alignment blueprint
- **Teaches concepts**: instruction-tuning, rlhf

### DPO (`res-dpo`)
- **URL**: https://arxiv.org/abs/2305.18290
- **Type**: paper
- **Quality**: 4/5 — Simplified RLHF to a single loss function
- **Teaches concepts**: direct-preference-optimization

### Chain-of-Thought (`res-chain-of-thought`)
- **URL**: https://arxiv.org/abs/2201.11903
- **Type**: paper
- **Quality**: 5/5 — Reasoning through prompting
- **Teaches concepts**: chain-of-thought

### ReAct (`res-react`)
- **URL**: https://arxiv.org/abs/2210.03629
- **Type**: paper
- **Quality**: 5/5 — Foundation of agentic systems
- **Teaches concepts**: react-framework

### DeepSeek-R1 (`res-deepseek-r1`)
- **URL**: https://arxiv.org/abs/2501.12948
- **Type**: paper
- **Quality**: 5/5 — Pure RL can induce structured reasoning
- **Teaches concepts**: rl-for-reasoning

### Qwen3 Technical Report (`res-qwen3`)
- **URL**: https://arxiv.org/abs/2505.09388
- **Type**: paper
- **Quality**: 4/5 — Modern MoE with thinking/non-thinking modes

### Sparse-Gated MoE (`res-sparse-gated-moe`)
- **URL**: https://arxiv.org/abs/1701.06538
- **Type**: paper
- **Quality**: 5/5 — Modern MoE ignition point
- **Teaches concepts**: mixture-of-experts

### Switch Transformers (`res-switch-transformers`)
- **URL**: https://arxiv.org/abs/2101.03961
- **Type**: paper
- **Quality**: 4/5 — Simplified MoE routing
- **Teaches concepts**: mixture-of-experts

### Mixtral (`res-mixtral`)
- **URL**: https://arxiv.org/abs/2401.04088
- **Type**: paper
- **Quality**: 4/5 — Open-weight MoE at dense quality
- **Teaches concepts**: mixture-of-experts

### Sparse Upcycling (`res-sparse-upcycling`)
- **URL**: https://arxiv.org/abs/2212.05055
- **Type**: paper
- **Quality**: 4/5 — Dense-to-MoE conversion
- **Teaches concepts**: sparse-upcycling

### Platonic Representation (`res-platonic-representation`)
- **URL**: https://arxiv.org/abs/2405.07987
- **Type**: paper
- **Quality**: 4/5 — Representational convergence hypothesis

### Textbooks Are All You Need (`res-textbooks-all-you-need`)
- **URL**: https://arxiv.org/abs/2306.11644
- **Type**: paper
- **Quality**: 4/5 — Data quality > quantity

### Scaling Monosemanticity (`res-scaling-monosemanticity`)
- **URL**: https://transformer-circuits.pub/2024/scaling-monosemanticity/
- **Type**: paper
- **Quality**: 5/5 — Biggest leap in mechanistic interpretability

### PaLM (`res-palm`)
- **URL**: https://arxiv.org/abs/2204.02311
- **Type**: paper
- **Quality**: 4/5 — Large-scale training orchestration masterclass

### GLaM (`res-glam`)
- **URL**: https://arxiv.org/abs/2112.06905
- **Type**: paper
- **Quality**: 4/5 — MoE scaling economics validated

### Smol Training Playbook (`res-smol-playbook`)
- **URL**: https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook
- **Type**: blog
- **Quality**: 4/5 — Practical training handbook

### Bonus: T5 (`res-t5`)
- **URL**: https://arxiv.org/abs/1910.10683

### Bonus: Toolformer (`res-toolformer`)
- **URL**: https://arxiv.org/abs/2302.04761

### Bonus: GShard (`res-gshard`)
- **URL**: https://arxiv.org/abs/2006.16668

### Bonus: Adaptive Mixtures of Local Experts (`res-adaptive-mixtures`)
- **URL**: https://www.cs.toronto.edu/~hinton/absps/jjnh91.pdf

### Bonus: Hierarchical Mixtures of Experts (`res-hierarchical-moe`)
- **URL**: https://doi.org/10.1162/neco.1994.6.2.181

### MIT 6.7960 Deep Learning Fall 2024 (`res-mit-deep-learning-2024`)
- **URL**: https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/download/
- **Type**: course
- **Quality**: 5/5

---

## Personal Notes

### AI That Matters — curated reading order (`note-reading-order-intro`)
- **Context**: File intro
- **Body**: Implement these 26 papers and you have captured ~90% of the alpha behind modern LLMs. The list bridges Transformer foundations with reasoning, MoE, and the agentic shift.

### Read Scaling Laws alongside Chinchilla (`note-chinchilla-insight`)
- **Context**: Papers 5-6
- **Body**: Read Scaling Laws (Kaplan 2020) alongside Chinchilla (Hoffmann 2022) to understand why most models were undertrained on tokens.

---

## New Connections Discovered

- chain-of-thought **extends** in-context-learning — CoT is a specific prompting strategy within ICL
- react-framework **extends** chain-of-thought — ReAct interleaves reasoning traces with actions
- rl-for-reasoning **extends** rlhf + chain-of-thought — RL induces structured reasoning without SFT
- direct-preference-optimization **contrasts_with** rlhf — DPO eliminates the reward model
- sparse-upcycling **enables** mixture-of-experts — Dense-to-MoE conversion
- flash-attention **extends** self-attention — IO-aware exact attention implementation
- multi-latent-attention **extends** multi-head-attention — KV cache compression via latent representations

---

## Graph Stats (after update)

- Total nodes: 98
- Total edges: 77
- Nodes by type: concept=34, resource=60, note=4
- Clusters: transformer-foundations (20), inference-optimization (21), scaling-and-training (17), reasoning-and-agents (9), representation-and-data (6), alignment-and-post-training (8), mixture-of-experts (11), llm-hardware (9), mechanistic-interpretability (10)
