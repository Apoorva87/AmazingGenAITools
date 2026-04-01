# Research Notes: The Encoder-Decoder Architecture
## Sub-topic 5 of 7

### Key Concepts to Cover

1. **Full Transformer Architecture Walkthrough**
   - Input: tokenization -> embedding -> positional encoding
   - Encoder: N layers of [Self-Attention -> Add&Norm -> FFN -> Add&Norm]
   - Decoder: N layers of [Masked Self-Attention -> Add&Norm -> Cross-Attention -> Add&Norm -> FFN -> Add&Norm]
   - Output: linear projection -> softmax over vocabulary
   - Standard config: N=6, d_model=512, n_heads=8, d_ff=2048

2. **Residual Connections and the Residual Stream**
   - x + Sublayer(x): identity shortcut
   - Enables gradient flow through deep networks
   - "Residual stream" interpretation (mechanistic interp): each layer reads from and writes to a shared stream
   - Sublayers are additive contributions, not sequential transformations
   - This view clarifies how information flows through the network

3. **Encoder Stack**
   - Bidirectional self-attention: every token attends to every other token
   - No masking: full context available
   - Outputs contextual representations for each input token
   - Used for understanding tasks (classification, NER, retrieval)

4. **Decoder Stack**
   - Causal (masked) self-attention: triangular mask prevents future tokens
   - Cross-attention: decoder queries attend to encoder outputs
   - Autoregressive generation: one token at a time
   - Used for generation tasks (translation, summarization, text generation)

5. **Cross-Attention Mechanism**
   - Q from decoder, K and V from encoder output
   - Allows decoder to "look at" the input sequence
   - Analogous to attention in traditional seq2seq models
   - Only present in encoder-decoder models

6. **Architecture Variants**
   - **Encoder-Only (BERT)**: bidirectional, masked language modeling, good for understanding
   - **Decoder-Only (GPT)**: causal attention only, autoregressive, dominant for generation
   - **Encoder-Decoder (T5, BART)**: full architecture, good for seq2seq tasks
   - Modern trend: decoder-only dominates for LLMs (simpler, scales better)

7. **Information Flow and Dimensionality**
   - Token embeddings: vocab_size -> d_model
   - Position embeddings: added to token embeddings
   - Each layer preserves d_model dimensions
   - Final layer: d_model -> vocab_size (shared weight tying with embeddings)
   - Total parameters: approximately 12 * N * d_model^2 (rough estimate)

### Primary Sources (Tier 1)

| Source | Focus | Use For |
|--------|-------|---------|
| S001 (Attention Is All You Need) | Full architecture | Original encoder-decoder design |
| S002 (Annotated Transformer) | Code | Complete implementation |
| S003 (Illustrated Transformer) | Visualization | Architecture flow diagrams |
| S025 (Karpathy GPT) | Decoder-only | Building GPT from scratch |
| S012 (BERT) | Encoder-only | Bidirectional pretraining |
| S013 (GPT-2) | Decoder-only | Autoregressive architecture |
| S014 (T5) | Encoder-decoder | Modern enc-dec design |

### Secondary Sources (Tier 2)

| Source | Focus | Use For |
|--------|-------|---------|
| S023 (Alammar seq2seq) | Attention origins | Historical progression |
| S024 (Alammar GPT-2) | Decoder architecture | Visual walkthrough |
| S027 (3Blue1Brown GPT) | Visual intro | Embedding space intuition |
| S029 (Umar Jamil Transformer) | Full build | Code-along implementation |
| S033 (Formal Algorithms) | Pseudocode | Precise algorithmic specification |
| S043 (Alammar GPT-3) | Autoregressive gen | In-context learning visualization |
| S044 (Bloem guide) | Holistic view | Mathematical and conceptual |
| S048 (minGPT) | Code | Minimal decoder-only implementation |
| S049 (nanoGPT) | Code | Training-ready implementation |

### Visual Resources Found
- Jay Alammar: Full encoder-decoder flow diagram (the classic one)
- Jay Alammar: Decoder-only generation sequence
- 3Blue1Brown: Embedding space and token flow
- Architecture comparison: encoder-only vs decoder-only vs encoder-decoder (side-by-side)
- Residual stream diagram: how sublayers contribute to the stream

### Code Examples Found
- Annotated Transformer: EncoderLayer, DecoderLayer, full Transformer
- minGPT: Clean decoder-only Transformer
- nanoGPT: Production-quality decoder-only with training loop
- Karpathy video: Live build of decoder-only GPT
- Umar Jamil: Full encoder-decoder in PyTorch

### Teaching Sequence (Recommended)
1. High-level architecture diagram: input -> encoder -> decoder -> output (intuition)
2. Residual stream metaphor: think of it as a highway
3. Walk through encoder: self-attention + FFN, layer by layer
4. Walk through decoder: masked self-attention + cross-attention + FFN
5. Implement a single Transformer block in PyTorch
6. Stack blocks into full encoder and decoder
7. Compare three architecture variants with concrete examples
8. Discuss why decoder-only won for LLMs

### Cross-links to Other Sub-topics
- -> Self-Attention: self-attention and cross-attention are core building blocks
- -> Positional Encoding: added at input, before first layer
- -> Normalization: Pre-LN or Post-LN in each sublayer
- -> FFN: second sublayer in every block
- -> Training: architecture determines what objective to use
- -> Modern Variants: modifications to the basic architecture

### Historical Context
- 2017: Original Transformer (encoder-decoder, for translation)
- 2018: GPT-1 (decoder-only, language modeling)
- 2018: BERT (encoder-only, masked language modeling)
- 2019: GPT-2 (scaled decoder-only)
- 2020: T5 (text-to-text encoder-decoder)
- 2020+: Decoder-only becomes dominant (GPT-3, PaLM, LLaMA, etc.)
