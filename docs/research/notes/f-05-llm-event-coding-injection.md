# F-05: LLM extraction of political events and claims; grounding; prompt-injection defences

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 28 tool uses

## Answer (verbatim; read 2026-10-20; numbers are from abstracts/landing pages unless noted)

1. LLM event coding.
- Halterman and Keith, arXiv 2407.10747 (v1 Jul 2024; v2 retitled "Codebook LLMs: Evaluating LLMs as Measurement Tools for Political Science Concepts"; Political Analysis 2025/26). Task: apply codebooks for US protest events, Pakistan political violence and party manifestos, using open-weight 7-12B models. Zero-shot, open models follow codebooks poorly. Supervised instruction tuning helps a lot; the v1 abstract (via search snippet) gives Mistral 7B at 0.76 vs 0.53 micro-F1. Caveat: only small open models, no "best model" claim, no dictionary baseline seen.
- Halterman, Schrodt, Beger, Bagozzi, Scarborough, "Creating Custom Event Data Without Dictionaries: A Bag-of-Tricks", arXiv 2304.01331 (2023). Task: build POLECAT-style event data with active-learning classifiers, LLM/QA actor-recipient extraction and Wikipedia actor linking. Accuracy figures: not found (abstract only). It argues dictionary coders are costly and context-blind.
- Ornstein, Blasingame, Truscott, Political Science Research and Methods (online 14 Jan 2025). Few-shot GPT-3/4 on tweet sentiment: 88.4% correct vs 64.3% fine-tuned RoBERTa, 57.7% Naive Bayes, 38.3% dictionary. Manifesto ideology correlation with experts 0.92 (economic) and 0.80 (social). GPT-4 was overconfident and slightly worse than GPT-3 on sentiment. Caveats: prompt design matters, validate against human codes, GPT-3 was retired in Jan 2024 (reproducibility). Not event coding.
- Gilardi, Alizadeh, Kubli, PNAS 120:e2305016120 (2023), arXiv 2303.15056. ChatGPT zero-shot accuracy beat MTurk crowd workers by about 25 points on average (n=6,183 tweets and news) at under $0.003 per annotation. arXiv v2 reports a smaller sample (2,382 tweets) and beating crowd workers on 4 of 5 tasks. I did not open the PDF. Caveat: it compares against crowd workers, not trained coders or dictionaries, and uses closed-model prompts.
- Follow-ups: He, Murugesan, Brandt, Hu, arXiv 2606.06781 (v2 Aug 2026), PLOVER relation coding. Enriched codebook guidance raised macro-F1 from 0.457 to 0.633, but after label-definition remapping no method exceeded 0.20 weighted F1, so accuracy does not show the model follows the codebook. Its abstract does not mention Universal PETRARCH, although a search snippet said it was a baseline. ICBeLLM, arXiv 2401.10558, codes ICBe crisis events with local open LLMs and no fine-tuning; metrics not seen. Not found: an LLM-vs-ACLED/UCDP paper with accuracy numbers. Only UCDP-AEC (KONVENS 2025) and Braun/Oswald ACLED-abduction extraction surfaced, unread. Not found: a Halterman paper on LLM coding for PLOVER/POLECAT.
2. Grounding. ALCE (Gao et al., arXiv 2305.14627): on ELI5 "even the best models lack complete citation support 50% of the time"; measure with automatic citation recall/precision. FActScore (Min et al., arXiv 2305.14251): split output into atomic facts and score the share supported by a source. ChatGPT scored 58% on biographies, and the automated estimator has under 2% error.
3. Prompt injection.
- OWASP LLM01 lists seven mitigations: constrain behavior; validate output formats with deterministic code; input/output filtering with the RAG triad; least privilege; human approval for high-risk actions; segregate and label external content; adversarial testing.
- Anthropic: put untrusted content only in tool_result blocks, state its source, add a system-prompt untrusted-content policy, and JSON-encode it. Also apply least privilege, screen tool output with a small classifier using structured outputs, and red-team.
- CaMeL (arXiv 2503.18813): untrusted data can never impact program flow, and capabilities gate tool calls. It solved 77% of AgentDojo tasks with provable security vs 84% undefended.
- Beurer-Kellner et al. (arXiv 2506.08837): design patterns for "provable resistance", trading utility for security.
- Willison dual LLM (2023): a privileged LLM with tools never sees untrusted text. A quarantined LLM with no tools reads it, and a non-LLM controller passes variable references. The lethal trifecta (2025) is private data plus untrusted content plus external communication; avoid combining all three.

## Evidence

- https://arxiv.org/abs/2407.10747v2
- https://arxiv.org/abs/2304.01331
- https://www.cambridge.org/core/product/8EAA8096779B5C9DDBDF1BFC71C63AEC
- https://arxiv.org/abs/2303.15056 (via search summary)
- https://arxiv.org/abs/2606.06781
- https://arxiv.org/abs/2401.10558
- https://arxiv.org/abs/2305.14627
- https://arxiv.org/abs/2305.14251
- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks (docs.anthropic.com 301s here)
- https://arxiv.org/abs/2503.18813
- https://arxiv.org/abs/2506.08837
- https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/

## Caveats (verbatim)

Most figures come from abstracts or landing pages, not full texts. The Codebook LLMs 0.76 vs 0.53 figure and the Gilardi version differences come from search snippets. The Anthropic page names "Claude Haiku 5.5", which may not match your model set. The OWASP page version (2025) was not confirmed on the page. The Willison trifecta page does not discuss dual LLM, so it is cited separately.

## Orchestrator note

Three design rules follow. First, LLM extraction is a measurement instrument that must be validated against a hand-coded sample per task and per model version (the He et al. result that headline F1 can rise while codebook-following stays near 0.20 is the warning). Second, every extracted claim carries a quoted span from the source and is checked for support by a second, cheaper pass (the FActScore pattern) before it is shown. Third, the extraction model is quarantined: it reads untrusted documents and returns structured output only; it has no tools, no network, and its output goes through deterministic validation; the system never lets document text influence control flow (the CaMeL and dual-LLM rules).
