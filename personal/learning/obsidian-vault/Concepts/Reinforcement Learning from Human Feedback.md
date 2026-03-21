---
id: "rlhf"
type: concept
depth: intermediate
confidence: 1
clusters:
  - "alignment-and-post-training"
tags:
  - alignment
  - ppo
  - reward-model
status: unread
---

# Reinforcement Learning from Human Feedback

**Depth**: intermediate | **Confidence**: ⭐ | **Status**: #unread

**Clusters**: [[Clusters/Alignment & Post-Training|Alignment & Post-Training]]

---

## Key Questions

- [ ] How does RLHF align model outputs with human preferences?
- [ ] What are the instability issues with PPO-based RLHF?

---

## Subtopics

- reward-modeling
- ppo
- direct-preference-optimization

---

## Relationships

- **learned_from** → [[Resources/Training Language Models to Follow Instructions (InstructGPT)|Training Language Models to Follow Instructions (InstructGPT)]]
  - _RLHF pipeline detailed in InstructGPT_
- **enables** ← [[Concepts/Instruction Tuning|Instruction Tuning]]
  - _SFT is the first step before RLHF in the alignment pipeline_
- **contrasts_with** ← [[Concepts/Direct Preference Optimization (DPO)|Direct Preference Optimization (DPO)]]
  - _DPO eliminates the reward model needed by RLHF/PPO_
- **extends** ← [[Concepts/Constitutional AI|Constitutional AI]]
  - _CAI uses AI feedback instead of human feedback for alignment_
- **extends** ← [[Concepts/RL for Reasoning (DeepSeek-R1 Style)|RL for Reasoning (DeepSeek-R1 Style)]]
  - _RL for reasoning applies RL to improve reasoning without SFT_

---

## My Notes

_Add your notes here as you learn this concept..._

