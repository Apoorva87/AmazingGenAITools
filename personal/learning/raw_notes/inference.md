lot of courses out there teach AI & LLMs, but very few touch on Inference

Sure, it's easy to grasp the fundamentals of what LLMs are and how to build systems around them, but scaling out an LLM out of a lab of 1-2 H100s running it and a single concurrent user session is a big challenge.

Efficient inference is one of the largest barriers to LLMs in production.

Batching, managing memory, concurrent user sessions, GPU saturation, and sharding with/or MIG (Multi-Instance GPUs), parallelisation are key concepts for engineers to know, understand, and work with or around them.

I've had this list of resources saved for a while, which fills some of those gaps.

1. Good Courses / Videos
- CS336 Stanford (Lecture 5-11): https://buff.ly/9o4jRxl
- GPU MODE: https://buff.ly/bPEHYL0 
- LLM Inference Patterns: https://buff.ly/4ASDS5c
- LLM Inference (NVIDIA): https://buff.ly/muDMcor 

2. Repositories / Blogs
- GPU Performance Engineering (E.Andere): https://buff.ly/sfGJNMK 
- AI Performance Engineering (C.Fregly) https://buff.ly/8ey3GPa 
- Inside NVIDIA GPUs (A.Gordic): https://buff.ly/wmgNwMg 
- Understanding LLM Inference (my article): https://buff.ly/NrNU3Qz 

I don't think there's a clear, step-by-step guide on how to master AI Perf Engineering.
The best bet is to study the core pieces of the models and the hardware they run on.
