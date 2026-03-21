# Processed: Ahmad Osman Recommended Reading List

**Source**: personal/learning/raw_notes/ahmad_osman_recommended.md
**Processed**: 2026-03-19
**Concepts extracted**: 3 (unique to this file; rest overlap with AI_that_matters)
**Resources processed**: 8
**Connections created**: 12

---

## Concepts

### Constitutional AI (`constitutional-ai`)
- **Depth**: intermediate
- **Cluster**: alignment-and-post-training
- **Key questions**:
  - How does Constitutional AI use AI feedback instead of human feedback?
  - What role do constitutional principles play in training harmless models?
- **Relationships**:
  - extends → rlhf
  - learned_from → res-constitutional-ai

### Multi-Latent Attention (`multi-latent-attention`)
- **Depth**: research
- **Clusters**: transformer-foundations, inference-optimization
- **Key questions**:
  - How does MLA reduce KV cache memory compared to standard MHA?
  - What is the latent compression bottleneck in MLA?
- **Relationships**:
  - extends → multi-head-attention
  - learned_from → res-deepseek-v3

### Sparse Autoencoders (`sparse-autoencoders`)
- **Depth**: research
- **Cluster**: mechanistic-interpretability
- **Key questions**:
  - How do sparse autoencoders extract monosemantic features?
  - What did scaling SAEs to Claude 3 Sonnet reveal?
- **Relationships**:
  - specializes → mechanistic-interpretability
  - learned_from → res-scaling-monosemanticity

---

## Resources

### Constitutional AI (`res-constitutional-ai`)
- **URL**: https://arxiv.org/abs/2212.08073
- **Type**: paper
- **Quality**: 5/5 — Anthropic alignment methodology using AI self-critique
- **Descriptiveness**: high
- **Teaches concepts**: constitutional-ai

### Mapping the Mind (`res-mapping-the-mind`)
- **URL**: https://www.anthropic.com/research/mapping-mind-language-model
- **Type**: blog
- **Quality**: 5/5 — Accessible overview of sparse autoencoder findings
- **Teaches concepts**: mechanistic-interpretability, sparse-autoencoders

### DeepSeek-V3 Technical Report (`res-deepseek-v3`)
- **URL**: https://arxiv.org/abs/2412.19437
- **Type**: paper
- **Quality**: 5/5 — MLA and MTP innovations
- **Teaches concepts**: multi-latent-attention

### Ahead of AI (`res-ahead-of-ai`)
- **URL**: https://magazine.sebastianraschka.com
- **Type**: blog/newsletter
- **Quality**: 5/5 — Deep technical analysis

### Interconnects (`res-interconnects`)
- **URL**: https://www.interconnects.ai
- **Type**: blog/newsletter
- **Quality**: 5/5 — RLHF and alignment analysis

### Karpathy's LLM.c (`res-karpathy-llm-c`)
- **URL**: https://github.com/karpathy/llm.c
- **Type**: repo
- **Quality**: 5/5 — Code-level mastery of LLM training

### Hugging Face Daily Papers (`res-hf-daily-papers`)
- **URL**: https://huggingface.co/papers
- **Type**: blog/tool
- **Quality**: 4/5 — Daily research pulse

---

## Personal Notes

### Open-source efficiency vs Anthropic conceptual control (`note-open-vs-proprietary`)
- **Context**: Section V analysis
- **Body**: Open-source is winning on structural efficiency (more smarts from less compute via MLA/MTP), while Anthropic is winning on conceptual control (internal feature mapping ensures complex multi-step agentic trajectories without veering off-track). Compare DeepSeek-V3 vs Anthropic Mapping the Mind.

---

## New Connections Discovered

- constitutional-ai **extends** rlhf — Uses AI feedback instead of human feedback
- multi-latent-attention **extends** multi-head-attention — Compresses KV cache via latent representations
- DeepSeek-V3 structural efficiency **contrasts_with** Anthropic conceptual control

---

## Graph Stats (after update)

- Total nodes: 98
- Total edges: 77
- Nodes by type: concept=34, resource=60, note=4
- Clusters: 9 total
