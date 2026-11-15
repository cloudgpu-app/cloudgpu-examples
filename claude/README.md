# Historical Claude-format API examples

This directory preserves earlier request-format examples. Model identifiers, client behavior and prices in old scripts are not current availability or discount promises. No current paid inference acceptance is claimed by this directory.

Before sending a paid request, consult the [live model list](https://cloudgpu.app/v1/models), [current pricing](https://cloudgpu.app/pricing) and [API documentation](https://cloudgpu.app/api/docs). Choose an actually available model and confirm that the chosen API format and client are supported. Do not assume that a gateway implements every native-provider API feature.

- [`python/`](python/), [`node/`](node/) and [`curl/`](curl/) contain earlier OpenAI-compatible chat request examples.
- [`messages-api/`](messages-api/) preserves a Messages-format request example; verify current support before use.
- [`tools/claude-code.md`](tools/claude-code.md) explains the compatibility boundary for a native client.

Keep credentials in a secure environment or client credential store, never in chat or committed source. Account authorization does not approve unbounded inference spending.

For a currently tested no-spend compute discovery example, start with [`../agent-readiness/`](../agent-readiness/).
