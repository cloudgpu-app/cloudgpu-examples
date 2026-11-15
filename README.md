# CloudGPU · compute examples for agents

Give an agent a way to discover compute, obtain explicit spending approval, run bounded work and verify its outputs. Service eligibility: developers outside mainland China; see [current terms](https://cloudgpu.app/terms).

## Start without an account

```sh
curl --fail --silent --show-error https://cloudgpu.app/v1/public/agent-self-check
```

This is read-only: no key, no GPU allocation, no charge. Read supported task types, actual billing rules, known issues and reliability sample sufficiency before planning a task. A responsive control plane does not guarantee generation or upstream capacity.

[Try the interactive Compute Lab](https://cloudgpu-app.github.io/cloudgpu-agent-skills/) · [Agent contract](https://cloudgpu.app/agent-contract.json) · [Live catalog](https://cloudgpu.app/v1/public/gpu-catalog)

## A real framework tool

[`agent-readiness/`](agent-readiness/) demonstrates CrewAI compute discovery using the actual tool interface. The smoke test invokes no LLM and creates no GPU. It preserves unknown reliability rates and fails closed on unavailable or changed contracts.

## Connect your agent

[CloudGPU MCP](https://github.com/cloudgpu-app/cloudgpu-mcp) provides local stdio and remote Streamable HTTP. See the current [client setup instructions](https://cloudgpu.app/docs/mcp), including Codex, Claude and compatible remote clients.

```sh
npx skills add cloudgpu-app/cloudgpu-agent-skills
```

An installed skill does not rent compute. Owner authorization and explicit paid-work approval are separate steps. Keep keys in your client's secure credential mechanism, not chat or copied source.

## Inspect three narrowly verified task recipes

The [published scripts and acceptance evidence](https://github.com/cloudgpu-app/cloudgpu-mcp/tree/main/examples/verified-tasks) cover:

| Small internal smoke test | Successful task elapsed | Final GPU fee for successful attempt |
| --- | ---: | ---: |
| GPU environment check | 191 seconds | $0.0048 |
| Wan2.1 1.3B ComfyUI video, 17 frames at 256×256 | 1,064 seconds | $0.1105 |
| SmolLM2-135M causal-LM LoRA, 8 steps | 190 seconds | $0.0097 |

These are historical internal tests, not price quotes, production success rates or arbitrary model guarantees. Video succeeded in 1 of 12 evolving development attempts (all attempts $0.8775); LoRA succeeded in 1 of 4 (all attempts $0.0339). The LoRA example is not image/diffusion LoRA. Read current evidence before execution.

## Billing and result persistence

Billing depends on the selected source. Minute-billed sources round partial minutes up. Whole-hour sources have a one-hour minimum and charge every started hour in full, including an early stop. Read the binding billing quote, minimum charge, start condition, expiry and hard spend/time limits before approving allocation. Do not infer billing from the GPU model.

Instance disks are erased on termination. Configure and verify saved Job outputs or Workspace storage before relying on persistence. Storage budgets, retention and transfer limits are separate from compute. Only choose Job-compatible inventory; reconcile uncertain creates instead of blindly retrying.

## Existing API examples

The `python/`, `node/`, `curl/`, `ai-sdk/`, `cursor/`, `claude/` and `ollama-on-rented-gpu/` directories contain earlier integration examples. Treat model identifiers, prices and availability in those files as historical examples; consult the live model catalog and pricing before use. Their presence is not a claim of a current discount, free GPU entitlement or validated end-to-end run.

[Agent API documentation](https://cloudgpu.app/docs/agents) · [Live model list](https://cloudgpu.app/v1/models) · [Pricing](https://cloudgpu.app/pricing)

MIT; third-party model and dataset licenses remain separate.
