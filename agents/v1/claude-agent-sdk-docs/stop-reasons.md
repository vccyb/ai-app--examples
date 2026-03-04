Title: Handle stop reasons

URL Source: https://platform.claude.com/docs/en/agent-sdk/stop-reasons

Markdown Content:
Handle stop reasons - Claude API Docs
===============

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Fstop-reasons)

Search...

⌘K

First steps

[Intro to Claude](https://platform.claude.com/docs/en/intro)[Quickstart](https://platform.claude.com/docs/en/get-started)

Models & pricing

[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)[Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)[What's new in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6)[Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)[Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)[Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

Build with Claude

[Features overview](https://platform.claude.com/docs/en/build-with-claude/overview)[Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)[Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)[Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

Model capabilities

[Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)[Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)[Effort](https://platform.claude.com/docs/en/build-with-claude/effort)[Fast mode (research preview)](https://platform.claude.com/docs/en/build-with-claude/fast-mode)[Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)[Citations](https://platform.claude.com/docs/en/build-with-claude/citations)[Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)[Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)[PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)[Search results](https://platform.claude.com/docs/en/build-with-claude/search-results)[Multilingual support](https://platform.claude.com/docs/en/build-with-claude/multilingual-support)[Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings)[Vision](https://platform.claude.com/docs/en/build-with-claude/vision)

Tools

[Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)[How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)[Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)[Web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)[Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)[Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)[Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool)[Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)[Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool)

Tool infrastructure

[Tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)[Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)[Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming)

Context management

[Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)[Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)[Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)[Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

Files & assets

[Files API](https://platform.claude.com/docs/en/build-with-claude/files)

Agent Skills

[Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)[Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)[Best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)[Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)[Using Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide)

Agent SDK

[Overview](https://platform.claude.com/docs/en/agent-sdk/overview)[Quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)[TypeScript SDK](https://platform.claude.com/docs/en/agent-sdk/typescript)[TypeScript V2 (preview)](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview)[Python SDK](https://platform.claude.com/docs/en/agent-sdk/python)[Migration Guide](https://platform.claude.com/docs/en/agent-sdk/migration-guide)

Guides

[Streaming Input](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)[Stream responses in real-time](https://platform.claude.com/docs/en/agent-sdk/streaming-output)[Handling stop reasons](https://platform.claude.com/docs/en/agent-sdk/stop-reasons)[Handling Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)[User approvals and input](https://platform.claude.com/docs/en/agent-sdk/user-input)[Control execution with hooks](https://platform.claude.com/docs/en/agent-sdk/hooks)[Session Management](https://platform.claude.com/docs/en/agent-sdk/sessions)[File checkpointing](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing)[Structured outputs in the SDK](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)[Hosting the Agent SDK](https://platform.claude.com/docs/en/agent-sdk/hosting)[Securely deploying AI agents](https://platform.claude.com/docs/en/agent-sdk/secure-deployment)[Modifying system prompts](https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts)[MCP in the SDK](https://platform.claude.com/docs/en/agent-sdk/mcp)[Custom Tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools)[Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)[Slash Commands in the SDK](https://platform.claude.com/docs/en/agent-sdk/slash-commands)[Agent Skills in the SDK](https://platform.claude.com/docs/en/agent-sdk/skills)[Track cost and usage](https://platform.claude.com/docs/en/agent-sdk/cost-tracking)[Todo Lists](https://platform.claude.com/docs/en/agent-sdk/todo-tracking)[Plugins in the SDK](https://platform.claude.com/docs/en/agent-sdk/plugins)

MCP in the API

[MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)[Remote MCP servers](https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers)

Claude on 3rd-party platforms

[Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock)[Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry)[Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)

Prompt engineering

[Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)[Console prompting tools](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools)

Test & evaluate

[Define success and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)[Using the Evaluation Tool](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool)[Reducing latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency)

Strengthen guardrails

[Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)[Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)[Mitigate jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)[Streaming refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals)[Reduce prompt leak](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak)

Administration and monitoring

[Admin API overview](https://platform.claude.com/docs/en/build-with-claude/administration-api)[Data residency](https://platform.claude.com/docs/en/build-with-claude/data-residency)[Workspaces](https://platform.claude.com/docs/en/build-with-claude/workspaces)[Usage and Cost API](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)[Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api)[Zero Data Retention](https://platform.claude.com/docs/en/build-with-claude/zero-data-retention)

[Console](https://platform.claude.com/)

[Log in](https://platform.claude.com/login)

Guides Handling stop reasons

Guides

Handle stop reasons
===================

Copy page

Understand why Claude stopped generating and handle refusals, token limits, and other termination conditions

Copy page

When Claude finishes generating a response, the underlying API reports a `stop_reason` indicating why: the response completed normally, hit a token limit, was declined as a refusal, or ended for another reason. This is useful for building robust agents that can distinguish between a successful completion and an early termination that might need a retry or a reformulated prompt.

The Agent SDK surfaces `stop_reason` on the final result message so you can check it without parsing individual stream events. Common use cases include detecting refusals (to log or surface a friendlier error to end users), catching `max_tokens` cutoffs (to retry with a higher limit or ask Claude to continue), and logging termination types for observability.

This guide covers:

*   [Read `stop_reason`](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#read-stop_reason) from result messages in TypeScript
*   The [full list of possible values](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#available-stop-reasons) and what each means
*   How `stop_reason`[interacts with error result subtypes](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#stop-reasons-on-error-results) like `error_max_turns`
*   A [Python workaround](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#read-stop_reason-in-python) using stream events, since `ResultMessage` doesn't include this field yet

Direct `stop_reason` access on result messages is currently **TypeScript-only**. The Python SDK's `ResultMessage` does not include this field. For Python, see [Read stop_reason in Python](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#read-stop_reason-in-python) for a workaround using stream events.

Read stop_reason
----------------

The `stop_reason` field is present on both success and error result messages. Check it after iterating through the message stream:

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Write a poem about the ocean"
})) {
  if (message.type === "result") {
    console.log("Stop reason:", message.stop_reason);
    if (message.stop_reason === "refusal") {
      console.log("The model declined this request.");
    }
  }
}
```

Available stop reasons
----------------------

| Stop reason | Meaning |
| --- | --- |
| `end_turn` | The model finished generating its response normally. |
| `max_tokens` | The response reached the maximum output token limit. |
| `stop_sequence` | The model generated a configured stop sequence. |
| `refusal` | The model declined to fulfill the request. |
| `tool_use` | The model's final output was a tool call. This is uncommon in SDK results because tool calls are normally executed before the result is returned. |
| `null` | No API response was received; for example, an error occurred before the first request, or the result was replayed from a cached session. |

Stop reasons on error results
-----------------------------

Error results (such as `error_max_turns` or `error_during_execution`) also carry `stop_reason`. The value reflects the last assistant message received before the error occurred:

| Result variant | `stop_reason` value |
| --- | --- |
| `success` | The stop reason from the final assistant message. |
| `error_max_turns` | The stop reason from the last assistant message before the turn limit was hit. |
| `error_max_budget_usd` | The stop reason from the last assistant message before the budget was exceeded. |
| `error_max_structured_output_retries` | The stop reason from the last assistant message before the retry limit was hit. |
| `error_during_execution` | The last stop reason seen, or `null` if the error occurred before any API response. |

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Refactor this module",
  options: { maxTurns: 3 }
})) {
  if (message.type === "result" && message.subtype === "error_max_turns") {
    console.log("Hit turn limit. Last stop reason:", message.stop_reason);
    // stop_reason might be "end_turn" or "tool_use"
    // depending on what the model was doing when the limit hit
  }
}
```

Detect refusals
---------------

Check `stop_reason === "refusal"` to detect when the model declines a request. Previously, detecting refusals required enabling partial message streaming and manually scanning stream events for `message_delta` events. With `stop_reason` on the result message, you can check directly:

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

async function safeQuery(prompt: string): Promise<string | null> {
  for await (const message of query({ prompt })) {
    if (message.type === "result") {
      if (message.stop_reason === "refusal") {
        console.log("Request was declined. Please revise your prompt.");
        return null;
      }
      if (message.subtype === "success") {
        return message.result;
      }
      return null;
    }
  }
  return null;
}
```

Read stop_reason in Python
--------------------------

The Python SDK doesn't expose `stop_reason` on `ResultMessage` directly. To access it, enable partial message streaming and scan `StreamEvent` messages for `message_delta` events:

Python

```
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
from claude_agent_sdk.types import StreamEvent
import asyncio

async def get_stop_reason(prompt: str):
    stop_reason = None
    result = None
    options = ClaudeAgentOptions(include_partial_messages=True)

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, StreamEvent):
            if message.event.get("type") == "message_delta":
                delta = message.event.get("delta", {})
                if "stop_reason" in delta:
                    stop_reason = delta["stop_reason"]
        elif isinstance(message, ResultMessage):
            result = message.result

    return stop_reason, result

stop_reason, result = asyncio.run(get_stop_reason("Summarize this article"))
print(f"stop_reason: {stop_reason}")  # e.g. "end_turn", "refusal", "tool_use"
print(result)
```

Next steps
----------

*   [Stream responses in real-time](https://platform.claude.com/docs/en/agent-sdk/streaming-output): access raw API events including `message_delta` as they arrive
*   [Structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs): get typed JSON responses from the agent
*   [Tracking costs and usage](https://platform.claude.com/docs/en/agent-sdk/cost-tracking): understand token usage and billing from result messages

Was this page helpful?

*   [Read stop_reason](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#read-stop-reason)
*   [Available stop reasons](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#available-stop-reasons)
*   [Stop reasons on error results](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#stop-reasons-on-error-results)
*   [Detect refusals](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#detect-refusals)
*   [Read stop_reason in Python](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#read-stop-reason-in-python)
*   [Next steps](https://platform.claude.com/docs/en/agent-sdk/stop-reasons#next-steps)

[](https://platform.claude.com/docs)

[](https://x.com/claudeai)[](https://www.linkedin.com/showcase/claude)[](https://instagram.com/claudeai)

### Solutions

*   [AI agents](https://claude.com/solutions/agents)
*   [Code modernization](https://claude.com/solutions/code-modernization)
*   [Coding](https://claude.com/solutions/coding)
*   [Customer support](https://claude.com/solutions/customer-support)
*   [Education](https://claude.com/solutions/education)
*   [Financial services](https://claude.com/solutions/financial-services)
*   [Government](https://claude.com/solutions/government)
*   [Life sciences](https://claude.com/solutions/life-sciences)

### Partners

*   [Amazon Bedrock](https://claude.com/partners/amazon-bedrock)
*   [Google Cloud's Vertex AI](https://claude.com/partners/google-cloud-vertex-ai)

### Learn

*   [Blog](https://claude.com/blog)
*   [Catalog](https://claude.ai/catalog/artifacts)
*   [Courses](https://www.anthropic.com/learn)
*   [Use cases](https://claude.com/resources/use-cases)
*   [Connectors](https://claude.com/partners/mcp)
*   [Customer stories](https://claude.com/customers)
*   [Engineering at Anthropic](https://www.anthropic.com/engineering)
*   [Events](https://www.anthropic.com/events)
*   [Powered by Claude](https://claude.com/partners/powered-by-claude)
*   [Service partners](https://claude.com/partners/services)
*   [Startups program](https://claude.com/programs/startups)

### Company

*   [Anthropic](https://www.anthropic.com/company)
*   [Careers](https://www.anthropic.com/careers)
*   [Economic Futures](https://www.anthropic.com/economic-futures)
*   [Research](https://www.anthropic.com/research)
*   [News](https://www.anthropic.com/news)
*   [Responsible Scaling Policy](https://www.anthropic.com/news/announcing-our-updated-responsible-scaling-policy)
*   [Security and compliance](https://trust.anthropic.com/)
*   [Transparency](https://www.anthropic.com/transparency)

### Learn

*   [Blog](https://claude.com/blog)
*   [Catalog](https://claude.ai/catalog/artifacts)
*   [Courses](https://www.anthropic.com/learn)
*   [Use cases](https://claude.com/resources/use-cases)
*   [Connectors](https://claude.com/partners/mcp)
*   [Customer stories](https://claude.com/customers)
*   [Engineering at Anthropic](https://www.anthropic.com/engineering)
*   [Events](https://www.anthropic.com/events)
*   [Powered by Claude](https://claude.com/partners/powered-by-claude)
*   [Service partners](https://claude.com/partners/services)
*   [Startups program](https://claude.com/programs/startups)

### Help and security

*   [Availability](https://www.anthropic.com/supported-countries)
*   [Status](https://status.claude.com/)
*   [Support](https://support.claude.com/)
*   [Discord](https://www.anthropic.com/discord)

### Terms and policies

*   [Privacy policy](https://www.anthropic.com/legal/privacy)
*   [Responsible disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)
*   [Terms of service: Commercial](https://www.anthropic.com/legal/commercial-terms)
*   [Terms of service: Consumer](https://www.anthropic.com/legal/consumer-terms)
*   [Usage policy](https://www.anthropic.com/legal/aup)
