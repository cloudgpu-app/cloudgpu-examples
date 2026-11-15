# Read-only GPU task discovery with CrewAI

Give a CrewAI agent a compute-discovery tool without granting it payment or allocation privileges. It uses a fixed public GET endpoint, validates the response contract and preserves known issues and insufficient reliability samples. No model inference is invoked by the smoke test.

## Run

Requires Python 3.10–3.13 and internet access.

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python readiness.py
```

Expected: a JSON summary with `read_only: true`, task types, source-specific billing, known issues and `paid_work_approved: false`. On network/contract failure, the result says `status: unavailable`; it does not substitute a successful response.

## Add to an existing CrewAI agent

```python
from crewai import Agent
from readiness import CloudGPUReadinessTool

# Your existing LLM configuration may incur that provider's charges.
planner = Agent(
    role="Compute planner",
    goal="Assess task fit and limitations; never allocate without owner approval",
    backstory="Compare workload requirements with the public compute contract.",
    tools=[CloudGPUReadinessTool()],
)
```

This example only discovers compute. Account authorization, binding quotes, spending approval, execution and export/release belong to a separate reviewed integration. Connecting an account is not approval to spend. Minute- and whole-hour sources have different minimums. Do not infer task fit from a GPU model alone or treat internal smoke-test results as a customer SLA.

Service eligibility and current terms: https://cloudgpu.app/terms . The example author is affiliated with CloudGPU. No referral links or install tracking are included.

## Verification

Tested by directly invoking the actual CrewAI tool against the anonymous endpoint; no LLM calls or GPU allocations. Tested failure handling for invalid and oversized responses. This is not a paid-Job or end-to-end Crew execution acceptance test.
