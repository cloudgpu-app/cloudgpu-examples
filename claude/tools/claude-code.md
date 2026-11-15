# Native-client compatibility check

This is a historical integration path, not a claim that every current Claude Code feature or Claude model is supported by CloudGPU. Consult current client terms, the [API documentation](https://cloudgpu.app/api/docs), [model list](https://cloudgpu.app/v1/models) and [pricing](https://cloudgpu.app/pricing) before configuring it.

Claude Code uses a Messages-format API. An OpenAI-compatible chat endpoint alone does not establish compatibility with that format, authentication method, model aliases, streaming, tools or other native-client features. Verify each required capability before running an agentic session that may send many requests.

Use the client's supported secure credential mechanism. Do not paste keys into chat or commit them into settings. Select actual currently available model IDs rather than copying historical aliases from older examples. No fixed discount, model availability or successful current native-client session is asserted here.

For GPU orchestration using MCP instead of a model-provider substitution, use the [current MCP client setup instructions](https://cloudgpu.app/docs/mcp), the [Agent Skills](https://github.com/cloudgpu-app/cloudgpu-agent-skills), or the [read-only compute discovery example](../../agent-readiness/).
