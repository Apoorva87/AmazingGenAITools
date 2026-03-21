---
id: "mixture-of-experts"
type: concept
depth: intermediate
confidence: 1
clusters:
  - "mixture-of-experts"
tags:
  - moe
  - sparse
  - conditional-computation
status: unread
---

# Mixture of Experts (MoE)

**Depth**: intermediate | **Confidence**: ⭐ | **Status**: #unread

**Clusters**: [[Clusters/Mixture of Experts|Mixture of Experts]]

---

## Key Questions

- [ ] How does MoE achieve large model capacity with constant inference cost?
- [ ] What is the routing problem in MoE and how is load balancing handled?

---

## Subtopics

- expert-routing
- load-balancing
- top-k-gating

---

## Relationships

- **extends** → [[Concepts/Transformer Architecture|Transformer Architecture]]
  - _MoE replaces dense FFN with sparse expert layers_
- **learned_from** → [[Resources/Outrageously Large Neural Networks - Sparsely-Gated MoE|Outrageously Large Neural Networks: Sparsely-Gated MoE]]
  - _Original modern MoE paper_
- **learned_from** → [[Resources/Switch Transformers|Switch Transformers]]
  - _Switch Transformers simplified MoE_
- **learned_from** → [[Resources/Mixtral of Experts|Mixtral of Experts]]
  - _Mixtral demonstrated open-weight MoE_
- **learned_from** → [[Resources/GLaM - Efficient Scaling with Mixture-of-Experts|GLaM: Efficient Scaling with Mixture-of-Experts]]
  - _GLaM MoE scaling economics_
- **enables** ← [[Concepts/Sparse Upcycling|Sparse Upcycling]]
  - _Upcycling converts dense models into MoE efficiently_

---

## My Notes

_Add your notes here as you learn this concept..._

