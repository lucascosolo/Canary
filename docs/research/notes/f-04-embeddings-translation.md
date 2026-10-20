# F-04: Multilingual embeddings, machine translation and language identification options

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 32 tool uses

## Answer (verbatim; read 2026-10-20)

At 50k items/day (~500-1000 tokens each, ~25-50M tokens/day) hosted embeddings cost roughly $0.50-1/day with OpenAI small, so cost is not the constraint. Local CPU embedding is feasible with Qwen3-Embedding-0.6B, bge-m3 or multilingual-e5, though throughput is undocumented. Translation is the real cost: DeepL and Google are about $20/M characters (unverified), so run local MADLAD-400 or NLLB through CTranslate2, or use Claude.

1. HOSTED EMBEDDINGS
- OpenAI: text-embedding-3-small $0.02/M tokens, -large $0.13/M (standard). Not on the page I could read: dimensions (1536 and 3072 from memory, unverified) and a language list.
- Voyage: voyage-4-large $0.12/M, voyage-4 $0.06/M, voyage-4-lite $0.02/M. Each has 200M free tokens per account. Older models: voyage-3.5 and voyage-3 $0.06/M, voyage-multilingual-2 $0.12/M, with no free tokens. The Batch API is 33% off. Dimensions: not found.
- Google: gemini-embedding-2 text is free on the free tier, $0.20/M paid, $0.10/M batch. The page gave no gemini-embedding-001 price. Dimensions: not found.
- Cohere: per-token embed-v4 and embed-multilingual-v3 prices not found. The pricing page shows only Model Vault instance pricing ($3-5/hour, $2,000-3,250/month).

2. OPEN-WEIGHT EMBEDDINGS (CPU-runnable)
- bge-m3: MIT, 1024 dimensions, 100+ languages, 8192 tokens. The card gives no parameter count (about 568M from memory) and no CPU throughput.
- multilingual-e5-large: MIT, 24 layers, 1024 dimensions, 100 languages (about 560M parameters from memory). e5-small license and size: not found. I believe it is MIT, 118M parameters and 384 dimensions, but I did not read it.
- nomic-embed-text-v2-moe: Apache-2.0, 475M total and 305M active parameters, 768 dimensions (Matryoshka down to 256), about 100 languages.
- Qwen3-Embedding-0.6B: Apache-2.0, 0.6B parameters, dimensions 32-1024, 100+ languages. MTEB multilingual mean 64.33.
- EmbeddingGemma-300m: Gemma license (gated, custom terms), 0.3B parameters, 768 dimensions (down to 128), 100+ languages. MTEB multilingual v2 mean 61.15.
- I could not load the MTEB leaderboard, so there is no verified "top small open model". Qwen3-Embedding-0.6B and EmbeddingGemma are the strongest small candidates I could read.

3. MACHINE TRANSLATION
- NLLB-200-distilled-600M: CC-BY-NC-4.0 (verified), so non-commercial only. A non-profit use probably qualifies, but check.
- MADLAD-400: Apache-2.0 (verified). google/madlad400-3b-mt is 3B parameters and covers 400+ languages. A GGUF build is 1.65 GB.
- Seed-X-PPO-7B: OpenMDW license. The card says 7B, though the file metadata shows 8B. It covers only 28 languages, so it is too narrow for "many languages".
- CTranslate2: MIT. It supports NLLB and MADLAD-400. Its README benchmarks (4 threads, c5.2xlarge, int8) show 696-860 tokens/s for small OPUS-MT and WMT14 models. There are no NLLB or MADLAD figures.
- DeepL API: the pricing page did not render. I found only the consumer plans (Free 50k characters/month; Team €24.99/user/month for 1M characters). The API Free tier (500k) and Pro rate (about $25/M plus a base fee, from memory) are not found.
- Google Cloud Translation: the price table did not load. Not found; from memory about $20/M characters with 500k free per month.
- Microsoft Translator: F0 free tier is 2M characters/month (verified). The S1 price showed as "$-", so not found.
- Claude: an option, no prices needed here.

4. LANGUAGE ID
- fastText lid.176: CC-BY-SA-3.0 (verified). The page gives no accuracy figures. The full model is 126 MB and the compressed one is 917 kB.
- Lingua (lingua-py): Apache-2.0. Its README reports German accuracy of 74.2% on single words, 93.9% on word pairs and 99.7% on sentences. It claims to beat CLD2 and CLD3 on short text, but the comparison is only in images.
- CLD3: license and accuracy not fetched. I believe it is Apache-2.0 and weak on short text.

## Evidence

- https://developers.openai.com/api/docs/pricing — $0.02 and $0.13 per M tokens
- https://docs.voyageai.com/docs/pricing — Voyage price table and free tokens
- https://ai.google.dev/gemini-api/docs/pricing — gemini-embedding-2 prices
- https://cohere.com/pricing — Model Vault pricing only
- https://huggingface.co/BAAI/bge-m3, https://huggingface.co/intfloat/multilingual-e5-large, https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe, https://huggingface.co/Qwen/Qwen3-Embedding-0.6B, https://huggingface.co/google/embeddinggemma-300m — model cards
- https://huggingface.co/facebook/nllb-200-distilled-600M, https://huggingface.co/google/madlad400-3b-mt, https://huggingface.co/ByteDance-Seed/Seed-X-PPO-7B — translation model cards
- https://github.com/OpenNMT/CTranslate2 — MIT license and CPU benchmarks
- https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator/ — 2M free characters
- https://fasttext.cc/docs/en/language-identification.html — license
- https://github.com/pemistahl/lingua-py — license and accuracy

## Caveats (verbatim)

The fetcher is a summarizer, and the OpenAI pricing page was 403 on the first URL. Not found: DeepL API pricing, Google Translate prices, Microsoft S1 price, Cohere per-token prices, the MTEB leaderboard, any CPU throughput for bge-m3, NLLB or MADLAD, and the e5-small card. Every figure marked "from memory" must be checked before use.

## Orchestrator note

The agent's opening arithmetic (25-50M tokens a day at $0.02 per million is $0.50-1.00 a day) is consistent with the prices it read; it is reproduced in `docs/07` with the computation shown. The design consequence: embeddings are cheap either way, so the choice is driven by reproducibility (an open-weight model with a pinned version can be re-run on the archive; a hosted model can be deprecated), which favours a local bge-m3 or Qwen3-Embedding-0.6B on this PC with a hosted fallback. Translation is done selectively (titles and extracted claims, not full text) with MADLAD-400 locally, and Claude for the small fraction that needs quality.
