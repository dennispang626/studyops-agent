# Phase 7 - Evaluation and Submission Assets

Phase 7 packages StudyOps Agent for capstone judging and portfolio reuse.

## What Was Added

- StudyOps-specific eval dataset in `tests/eval/datasets/basic-dataset.json`.
- Additional capstone eval prompts in `tests/eval/datasets/studyops-capstone-dataset.json`.
- Custom eval config in `tests/eval/eval_config.yaml`.
- Kaggle writeup draft in `submission/kaggle-writeup-draft.md`.
- 5-minute video script in `submission/video-script.md`.
- Demo checklist in `submission/demo-checklist.md`.
- Mermaid architecture notes in `submission/architecture-for-writeup.md`.

## Eval Coverage

The eval cases cover:

- Running the AIF-C01 source-to-quiz workflow.
- Rejecting exam dumps and guaranteed-pass requests.
- Building a CLF-C02 study plan.
- Explaining wrong answers with per-option feedback.
- Handling learner uploads safely.

## Metrics

The eval config includes:

- `studyops_response_quality`: LLM-as-judge rubric for usefulness, safety, and StudyOps concept coverage.
- `studyops_safety_static`: local static check for unsafe exam-dump or guaranteed-pass language.
- `studyops_trace_completeness`: local trace concept check for source, trust, knowledge, study, practice, and remediation.

## Verification Note

The project currently verifies deterministic code and asset contracts through
unit tests. Full `agents-cli eval generate` / `agents-cli eval grade` should be
run after the ADK dependencies and model credentials are available.

