Title: Stream responses in real-time

URL Source: https://platform.claude.com/docs/en/agent-sdk/streaming-output

Markdown Content:
Stream responses in real-time - Claude API Docs
===============

Loading...

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Fstreaming-output)

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

Guides Stream responses in real-time

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

Loading...

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

Guides

Stream responses in real-time
=============================

Copy page

Get real-time responses from the Agent SDK as text and tool calls stream in

Copy page

By default, the Agent SDK yields complete `AssistantMessage` objects after Claude finishes generating each response. To receive incremental updates as text and tool calls are generated, enable partial message streaming by setting `include_partial_messages` (Python) or `includePartialMessages` (TypeScript) to `true` in your options.

This page covers output streaming (receiving tokens in real-time). For input modes (how you send messages), see [Send messages to agents](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode). You can also [stream responses using the Agent SDK via the CLI](https://code.claude.com/docs/en/headless).

Enable streaming output
-----------------------

To enable streaming, set `include_partial_messages` (Python) or `includePartialMessages` (TypeScript) to `true` in your options. This causes the SDK to yield `StreamEvent` messages containing raw API events as they arrive, in addition to the usual `AssistantMessage` and `ResultMessage`.

Your code then needs to:

1.   Check each message's type to distinguish `StreamEvent` from other message types
2.   For `StreamEvent`, extract the `event` field and check its `type`
3.   Look for `content_block_delta` events where `delta.type` is `text_delta`, which contain the actual text chunks

The example below enables streaming and prints text chunks as they arrive. Notice the nested type checks: first for `StreamEvent`, then for `content_block_delta`, then for `text_delta`:

Python

```
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent
import asyncio

async def stream_response():
    options = ClaudeAgentOptions(
        include_partial_messages=True,
        allowed_tools=["Bash", "Read"],
    )

    async for message in query(prompt="List the files in my project", options=options):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    print(delta.get("text", ""), end="", flush=True)

asyncio.run(stream_response())
```

StreamEvent reference
---------------------

When partial messages are enabled, you receive raw Claude API streaming events wrapped in an object. The type has different names in each SDK:

*   **Python**: `StreamEvent` (import from `claude_agent_sdk.types`)
*   **TypeScript**: `SDKPartialAssistantMessage` with `type: 'stream_event'`

Both contain raw Claude API events, not accumulated text. You need to extract and accumulate text deltas yourself. Here's the structure of each type:

Python

```
@dataclass
class StreamEvent:
    uuid: str  # Unique identifier for this event
    session_id: str  # Session identifier
    event: dict[str, Any]  # The raw Claude API stream event
    parent_tool_use_id: str | None  # Parent tool ID if from a subagent
```

The `event` field contains the raw streaming event from the [Claude API](https://platform.claude.com/docs/en/build-with-claude/streaming#event-types). Common event types include:

| Event Type | Description |
| --- | --- |
| `message_start` | Start of a new message |
| `content_block_start` | Start of a new content block (text or tool use) |
| `content_block_delta` | Incremental update to content |
| `content_block_stop` | End of a content block |
| `message_delta` | Message-level updates (stop reason, usage) |
| `message_stop` | End of the message |

Message flow
------------

With partial messages enabled, you receive messages in this order:

```
StreamEvent (message_start)
StreamEvent (content_block_start) - text block
StreamEvent (content_block_delta) - text chunks...
StreamEvent (content_block_stop)
StreamEvent (content_block_start) - tool_use block
StreamEvent (content_block_delta) - tool input chunks...
StreamEvent (content_block_stop)
StreamEvent (message_delta)
StreamEvent (message_stop)
AssistantMessage - complete message with all content
... tool executes ...
... more streaming events for next turn ...
ResultMessage - final result
```

Without partial messages enabled (`include_partial_messages` in Python, `includePartialMessages` in TypeScript), you receive all message types except `StreamEvent`. Common types include `SystemMessage` (session initialization), `AssistantMessage` (complete responses), `ResultMessage` (final result), and `CompactBoundaryMessage` (indicates when conversation history was compacted).

Stream text responses
---------------------

To display text as it's generated, look for `content_block_delta` events where `delta.type` is `text_delta`. These contain the incremental text chunks. The example below prints each chunk as it arrives:

Python

```
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent
import asyncio

async def stream_text():
    options = ClaudeAgentOptions(include_partial_messages=True)

    async for message in query(prompt="Explain how databases work", options=options):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    # Print each text chunk as it arrives
                    print(delta.get("text", ""), end="", flush=True)

    print()  # Final newline

asyncio.run(stream_text())
```

Stream tool calls
-----------------

Tool calls also stream incrementally. You can track when tools start, receive their input as it's generated, and see when they complete. The example below tracks the current tool being called and accumulates the JSON input as it streams in. It uses three event types:

*   `content_block_start`: tool begins
*   `content_block_delta` with `input_json_delta`: input chunks arrive
*   `content_block_stop`: tool call complete

Python

```
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent
import asyncio

async def stream_tool_calls():
    options = ClaudeAgentOptions(
        include_partial_messages=True,
        allowed_tools=["Read", "Bash"],
    )

    # Track the current tool and accumulate its input JSON
    current_tool = None
    tool_input = ""

    async for message in query(prompt="Read the README.md file", options=options):
        if isinstance(message, StreamEvent):
            event = message.event
            event_type = event.get("type")

            if event_type == "content_block_start":
                # New tool call is starting
                content_block = event.get("content_block", {})
                if content_block.get("type") == "tool_use":
                    current_tool = content_block.get("name")
                    tool_input = ""
                    print(f"Starting tool: {current_tool}")

            elif event_type == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "input_json_delta":
                    # Accumulate JSON input as it streams in
                    chunk = delta.get("partial_json", "")
                    tool_input += chunk
                    print(f"  Input chunk: {chunk}")

            elif event_type == "content_block_stop":
                # Tool call complete - show final input
                if current_tool:
                    print(f"Tool {current_tool} called with: {tool_input}")
                    current_tool = None

asyncio.run(stream_tool_calls())
```

Build a streaming UI
--------------------

This example combines text and tool streaming into a cohesive UI. It tracks whether the agent is currently executing a tool (using an `in_tool` flag) to show status indicators like `[Using Read...]` while tools run. Text streams normally when not in a tool, and tool completion triggers a "done" message. This pattern is useful for chat interfaces that need to show progress during multi-step agent tasks.

Python

```
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
from claude_agent_sdk.types import StreamEvent
import asyncio
import sys

async def streaming_ui():
    options = ClaudeAgentOptions(
        include_partial_messages=True,
        allowed_tools=["Read", "Bash", "Grep"],
    )

    # Track whether we're currently in a tool call
    in_tool = False

    async for message in query(
        prompt="Find all TODO comments in the codebase", options=options
    ):
        if isinstance(message, StreamEvent):
            event = message.event
            event_type = event.get("type")

            if event_type == "content_block_start":
                content_block = event.get("content_block", {})
                if content_block.get("type") == "tool_use":
                    # Tool call is starting - show status indicator
                    tool_name = content_block.get("name")
                    print(f"\n[Using {tool_name}...]", end="", flush=True)
                    in_tool = True

            elif event_type == "content_block_delta":
                delta = event.get("delta", {})
                # Only stream text when not executing a tool
                if delta.get("type") == "text_delta" and not in_tool:
                    sys.stdout.write(delta.get("text", ""))
                    sys.stdout.flush()

            elif event_type == "content_block_stop":
                if in_tool:
                    # Tool call finished
                    print(" done", flush=True)
                    in_tool = False

        elif isinstance(message, ResultMessage):
            # Agent finished all work
            print(f"\n\n--- Complete ---")

asyncio.run(streaming_ui())
```

Known limitations
-----------------

Some SDK features are incompatible with streaming:

*   **Extended thinking**: when you explicitly set `max_thinking_tokens` (Python) or `maxThinkingTokens` (TypeScript), `StreamEvent` messages are not emitted. You'll only receive complete messages after each turn. Note that thinking is disabled by default in the SDK, so streaming works unless you enable it.
*   **Structured output**: the JSON result appears only in the final `ResultMessage.structured_output`, not as streaming deltas. See [structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs) for details.

Next steps
----------

Now that you can stream text and tool calls in real-time, explore these related topics:

*   [Interactive vs one-shot queries](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode): choose between input modes for your use case
*   [Structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs): get typed JSON responses from the agent
*   [Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions): control which tools the agent can use

Was this page helpful?

*   [Enable streaming output](https://platform.claude.com/docs/en/agent-sdk/streaming-output#enable-streaming-output)
*   [StreamEvent reference](https://platform.claude.com/docs/en/agent-sdk/streaming-output#stream-event-reference)
*   [Message flow](https://platform.claude.com/docs/en/agent-sdk/streaming-output#message-flow)
*   [Stream text responses](https://platform.claude.com/docs/en/agent-sdk/streaming-output#stream-text-responses)
*   [Stream tool calls](https://platform.claude.com/docs/en/agent-sdk/streaming-output#stream-tool-calls)
*   [Build a streaming UI](https://platform.claude.com/docs/en/agent-sdk/streaming-output#build-a-streaming-ui)
*   [Known limitations](https://platform.claude.com/docs/en/agent-sdk/streaming-output#known-limitations)
*   [Next steps](https://platform.claude.com/docs/en/agent-sdk/streaming-output#next-steps)
