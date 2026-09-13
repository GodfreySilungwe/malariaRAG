# Design and Evaluation

## Design and Architecture Decisions

### Retrieval-augmented generation

The application retrieves relevant chunks from malaria-policy documents before asking the language model to answer. This grounds responses in the supplied corpus and allows the application to return supporting sources rather than relying only on model memory.

### Document processing and storages

PDF files are loaded with LangChain document loaders, split with a recursive character splitter, embedded with `sentence-transformers/all-MiniLM-L6-v2`, and persisted in Chroma. Chroma was selected because it is simple to run locally and integrates with the LangChain retrieval workflow.

### Retrieval and prompting

The default retrieval depth is `TOP_K = 4`, balancing context coverage and prompt size. The prompt instructs the model to use only retrieved context, answer concisely, preserve inline citation markers, and avoid unsupported claims.

### Model integration

The model adapter uses the OpenAI-compatible OpenRouter API. This keeps the application provider-flexible while allowing a remote hosted model to generate answers without serving an LLM locally.

### Application interfaces

Flask provides the `/health`, `/chat`, and frontend-serving routes. React provides the browser UI. The optional Streamlit client remains available for local experimentation but is not required by the deployed Flask/React service.

### Deployment

Railway builds the repository using the Dockerfile and starts `python app.py`. Flask binds to Railway's injected `PORT`. GitHub Actions runs the test suite before deploying pushes to `main` with the Railway CLI.

## Evaluation Approach

The repository uses three layers of evaluation:

1. **Automated regression tests** in `tests/test_malaria_rag.py` cover source formatting, page extraction, response fields, Flask health/chat validation, and refusal configuration.
2. **Evaluation harness** in `evaluate.py` runs questions from `eval_questions.json`, records answers and source metadata, and calculates p50 and p95 latency.
3. **Human review** checks whether each answer is supported by its retrieved policy passages and whether citations identify the correct document and page.

Recommended review criteria are:

- Groundedness: claims are supported by retrieved policy text.
- Citation accuracy: citations identify the relevant document and page.
- Refusal behavior: unsupported questions receive the refusal response.
- Latency: compare p50 and p95 response times.

Run the automated checks with:

```bash
python -m pytest tests/ -v --cov=. --cov-report=xml --tb=short
python evaluate.py
```

The current automated suite contains 16 tests. Evaluation results are written to `eval_results.json`; model-dependent results require `OPENROUTER_API_KEY` and a populated vector store.

# MalariaAI RAG Evaluation Report

## Overview

This report evaluates seven malaria-policy questions using three measures:

- **Groundedness**: whether the response is supported by the retrieved context.
- **Citation accuracy**: whether the cited sources support the response.
- **Latency**: elapsed time for generating the response.

The gold answers and source documents were supplied as the reference standard for this review.

## Aggregate Results

| Metric | Result |
|---|---:|
| Questions evaluated | 7 |
| Mean groundedness | 95.7% |
| Mean citation accuracy | 97.1% |
| Groundedness scores | 90, 100, 100, 90, 100, 100, 90 |
| Citation accuracy scores | 90, 100, 100, 90, 100, 100, 100 |
| Reported latency range | 14-20 seconds |
| Mean reported latency | 17.6 seconds |

The groundedness and citation scores are strong overall. However, these scores do not by themselves guarantee that the final answer exactly matches the gold answer. The question-level review below identifies answer coverage and factual precision issues.

## Question-Level Results

### 1. First-line treatment for uncomplicated malaria in Malawi

- **Gold answer:** Lumefantrine-Artemether (LA)
- **Source:** Treatment Guidelines, 5th Edition
- **Response:** The system declined to provide the treatment and stated that the retrieved excerpts did not contain the protocol details.
- **Groundedness:** 90%
- **Citation accuracy:** 90%
- **Latency:** 18 seconds
- **Assessment:** The refusal was appropriately cautious given the retrieved context, but it did not answer the question. This is a retrieval or corpus-coverage failure for a central policy fact.

### 2. Second-line treatment for uncomplicated malaria

- **Gold answer:** Artesunate-Amodiaquine (ASAQ)
- **Source:** Treatment Guidelines, 5th Edition
- **Groundedness:** 100%
- **Citation accuracy:** 100%
- **Latency:** 17 seconds
- **Assessment:** Correct. The response identified ASAQ, explained when it is used, and cited the treatment guideline pages.

### 3. Treatment in the first trimester of pregnancy

- **Gold answer:** Oral quinine 600 mg every 8 hours for 7 days plus clindamycin 300 mg every 8 hours for 7 days
- **Source:** Treatment Guidelines, 5th Edition
- **Groundedness:** 100%
- **Citation accuracy:** 100%
- **Latency:** 20 seconds
- **Assessment:** The response correctly included oral quinine plus clindamycin and added an important guideline distinction about artemisinin-based treatment and confirmed treatment failure. The response should state the requested dosage and duration more explicitly to match the gold answer completely.

### 4. First-line inpatient treatment for severe malaria

- **Gold answer:** Parenteral artesunate
- **Source:** Treatment Guidelines, 5th Edition
- **Groundedness:** 90%
- **Citation accuracy:** 90%
- **Latency:** 14 seconds
- **Assessment:** Correct answer, but one cited passage relied partly on a table of contents rather than the substantive treatment recommendation. Retrieval should prioritize the definitive treatment page.

### 5. Community-level pre-referral treatment for severe malaria

- **Gold answer:** Rectal artesunate
- **Source:** Treatment Guidelines, 5th Edition
- **Groundedness:** 100%
- **Citation accuracy:** 100%
- **Latency:** 19 seconds
- **Assessment:** Correct and detailed. The response included dose, referral timing, repeat-dose guidance, and supporting citations.

### 6. IPTp doses of SP during pregnancy

- **Gold answer:** At least 3 doses
- **Source:** Treatment Guidelines, 5th Edition
- **Groundedness:** 100%
- **Citation accuracy:** 100%
- **Latency:** 18 seconds
- **Assessment:** The response reached the correct benchmark of three or more doses and cited monitoring reports. It appropriately noted that the retrieved context showed the target but did not contain a direct recommendation statement; the treatment guideline should be retrieved for the strongest evidence.

### 7. Malaria prevalence in children aged 6-59 months in the 2021 MIS

- **Gold answer:** 10.5%
- **Source:** MIS 2021
- **Groundedness:** 90%
- **Citation accuracy:** 100%
- **Latency:** 17 seconds
- **Assessment:** The response cited the correct MIS pages and reported 10%, while the gold answer is 10.5%. The evidence was relevant, but the numerical answer does not exactly match the reference value. This requires investigation of rounding, the measure used, or the retrieved table.

## Findings

### Strengths

- Responses were generally grounded in malaria-policy documents.
- Citations were highly accurate overall.
- The system provided useful supporting snippets and page references for treatment questions.
- The model showed appropriate uncertainty when retrieved evidence did not contain the requested fact.

### Improvement Areas

1. Improve retrieval for high-value treatment facts, especially first-line uncomplicated malaria treatment.
2. Prefer substantive guideline pages over table-of-contents or cover-page passages.
3. Preserve exact numeric values rather than rounding prevalence figures.
4. Include dosage and duration when the question asks for a treatment regimen.
5. Add answer-level correctness scoring to future evaluations, since groundedness and citation accuracy can remain high even when the final answer is incomplete or numerically different from the gold answer.

## Conclusion

The evaluated responses achieved strong evidence quality, with mean groundedness of **95.7%** and mean citation accuracy of **97.1%**. The main remaining risks are retrieval coverage and exact answer fidelity: one central treatment question received a refusal, one treatment response omitted the requested regimen details, and one prevalence response differed from the gold value. Future evaluation should combine groundedness and citation accuracy with exact-answer or expert-judged correctness.
