Title: TypeScript SDK V2 interface (preview)

URL Source: https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview

Markdown Content:
TypeScript SDK V2 interface (preview) - Claude API Docs
===============

Loading...

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Ftypescript-v2-preview)

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

Agent SDK TypeScript V2 (preview)

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

Agent SDK

TypeScript SDK V2 interface (preview)
=====================================

Copy page

Preview of the simplified V2 TypeScript Agent SDK, with session-based send/stream patterns for multi-turn conversations.

Copy page

The V2 interface is an **unstable preview**. APIs may change based on feedback before becoming stable. Some features like session forking are only available in the [V1 SDK](https://platform.claude.com/docs/en/agent-sdk/typescript).

The V2 Claude Agent TypeScript SDK removes the need for async generators and yield coordination. This makes multi-turn conversations simpler, instead of managing generator state across turns, each turn is a separate `send()`/`stream()` cycle. The API surface reduces to three concepts:

*   `createSession()` / `resumeSession()`: Start or continue a conversation
*   `session.send()`: Send a message
*   `session.stream()`: Get the response

Installation
------------

The V2 interface is included in the existing SDK package:

`npm install @anthropic-ai/claude-agent-sdk`

Quick start
-----------

### One-shot prompt

For simple single-turn queries where you don't need to maintain a session, use `unstable_v2_prompt()`. This example sends a math question and logs the answer:

```
import { unstable_v2_prompt } from "@anthropic-ai/claude-agent-sdk";

const result = await unstable_v2_prompt("What is 2 + 2?", {
  model: "claude-opus-4-6"
});
if (result.subtype === "success") {
  console.log(result.result);
}
```

See the same operation in V1

```
import { query } from "@anthropic-ai/claude-agent-sdk";

const q = query({
  prompt: "What is 2 + 2?",
  options: { model: "claude-opus-4-6" }
});

for await (const msg of q) {
  if (msg.type === "result") {
    console.log(msg.result);
  }
}
```

### Basic session

For interactions beyond a single prompt, create a session. V2 separates sending and streaming into distinct steps:

*   `send()` dispatches your message
*   `stream()` streams back the response

This explicit separation makes it easier to add logic between turns (like processing responses before sending follow-ups).

The example below creates a session, sends "Hello!" to Claude, and prints the text response. It uses [`await using`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html#using-declarations-and-explicit-resource-management) (TypeScript 5.2+) to automatically close the session when the block exits. You can also call `session.close()` manually.

```
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

await using session = unstable_v2_createSession({
  model: "claude-opus-4-6"
});

await session.send("Hello!");
for await (const msg of session.stream()) {
  // Filter for assistant messages to get human-readable output
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log(text);
  }
}
```

See the same operation in V1
In V1, both input and output flow through a single async generator. For a basic prompt this looks similar, but adding multi-turn logic requires restructuring to use an input generator.

```
import { query } from "@anthropic-ai/claude-agent-sdk";

const q = query({
  prompt: "Hello!",
  options: { model: "claude-opus-4-6" }
});

for await (const msg of q) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log(text);
  }
}
```

### Multi-turn conversation

Sessions persist context across multiple exchanges. To continue a conversation, call `send()` again on the same session. Claude remembers the previous turns.

This example asks a math question, then asks a follow-up that references the previous answer:

```
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

await using session = unstable_v2_createSession({
  model: "claude-opus-4-6"
});

// Turn 1
await session.send("What is 5 + 3?");
for await (const msg of session.stream()) {
  // Filter for assistant messages to get human-readable output
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log(text);
  }
}

// Turn 2
await session.send("Multiply that by 2");
for await (const msg of session.stream()) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log(text);
  }
}
```

See the same operation in V1

```
import { query } from "@anthropic-ai/claude-agent-sdk";

// Must create an async iterable to feed messages
async function* createInputStream() {
  yield {
    type: "user",
    session_id: "",
    message: { role: "user", content: [{ type: "text", text: "What is 5 + 3?" }] },
    parent_tool_use_id: null
  };
  // Must coordinate when to yield next message
  yield {
    type: "user",
    session_id: "",
    message: { role: "user", content: [{ type: "text", text: "Multiply by 2" }] },
    parent_tool_use_id: null
  };
}

const q = query({
  prompt: createInputStream(),
  options: { model: "claude-opus-4-6" }
});

for await (const msg of q) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log(text);
  }
}
```

### Session resume

If you have a session ID from a previous interaction, you can resume it later. This is useful for long-running workflows or when you need to persist conversations across application restarts.

This example creates a session, stores its ID, closes it, then resumes the conversation:

```
import {
  unstable_v2_createSession,
  unstable_v2_resumeSession,
  type SDKMessage
} from "@anthropic-ai/claude-agent-sdk";

// Helper to extract text from assistant messages
function getAssistantText(msg: SDKMessage): string | null {
  if (msg.type !== "assistant") return null;
  return msg.message.content
    .filter((block) => block.type === "text")
    .map((block) => block.text)
    .join("");
}

// Create initial session and have a conversation
const session = unstable_v2_createSession({
  model: "claude-opus-4-6"
});

await session.send("Remember this number: 42");

// Get the session ID from any received message
let sessionId: string | undefined;
for await (const msg of session.stream()) {
  sessionId = msg.session_id;
  const text = getAssistantText(msg);
  if (text) console.log("Initial response:", text);
}

console.log("Session ID:", sessionId);
session.close();

// Later: resume the session using the stored ID
await using resumedSession = unstable_v2_resumeSession(sessionId!, {
  model: "claude-opus-4-6"
});

await resumedSession.send("What number did I ask you to remember?");
for await (const msg of resumedSession.stream()) {
  const text = getAssistantText(msg);
  if (text) console.log("Resumed response:", text);
}
```

See the same operation in V1

```
import { query } from "@anthropic-ai/claude-agent-sdk";

// Create initial session
const initialQuery = query({
  prompt: "Remember this number: 42",
  options: { model: "claude-opus-4-6" }
});

// Get session ID from any message
let sessionId: string | undefined;
for await (const msg of initialQuery) {
  sessionId = msg.session_id;
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log("Initial response:", text);
  }
}

console.log("Session ID:", sessionId);

// Later: resume the session
const resumedQuery = query({
  prompt: "What number did I ask you to remember?",
  options: {
    model: "claude-opus-4-6",
    resume: sessionId
  }
});

for await (const msg of resumedQuery) {
  if (msg.type === "assistant") {
    const text = msg.message.content
      .filter((block) => block.type === "text")
      .map((block) => block.text)
      .join("");
    console.log("Resumed response:", text);
  }
}
```

### Cleanup

Sessions can be closed manually or automatically using [`await using`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html#using-declarations-and-explicit-resource-management), a TypeScript 5.2+ feature for automatic resource cleanup. If you're using an older TypeScript version or encounter compatibility issues, use manual cleanup instead.

**Automatic cleanup (TypeScript 5.2+):**

```
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

await using session = unstable_v2_createSession({
  model: "claude-opus-4-6"
});
// Session closes automatically when the block exits
```

**Manual cleanup:**

```
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

const session = unstable_v2_createSession({
  model: "claude-opus-4-6"
});
// ... use the session ...
session.close();
```

API reference
-------------

### `unstable_v2_createSession()`

Creates a new session for multi-turn conversations.

```
function unstable_v2_createSession(options: {
  model: string;
  // Additional options supported
}): SDKSession;
```

### `unstable_v2_resumeSession()`

Resumes an existing session by ID.

```
function unstable_v2_resumeSession(
  sessionId: string,
  options: {
    model: string;
    // Additional options supported
  }
): SDKSession;
```

### `unstable_v2_prompt()`

One-shot convenience function for single-turn queries.

```
function unstable_v2_prompt(
  prompt: string,
  options: {
    model: string;
    // Additional options supported
  }
): Promise<SDKResultMessage>;
```

### SDKSession interface

```
interface SDKSession {
  readonly sessionId: string;
  send(message: string | SDKUserMessage): Promise<void>;
  stream(): AsyncGenerator<SDKMessage, void>;
  close(): void;
}
```

Feature availability
--------------------

Not all V1 features are available in V2 yet. The following require using the [V1 SDK](https://platform.claude.com/docs/en/agent-sdk/typescript):

*   Session forking (`forkSession` option)
*   Some advanced streaming input patterns

Feedback
--------

Share your feedback on the V2 interface before it becomes stable. Report issues and suggestions through [GitHub Issues](https://github.com/anthropics/claude-code/issues).

See also
--------

*   [TypeScript SDK reference (V1)](https://platform.claude.com/docs/en/agent-sdk/typescript) - Full V1 SDK documentation
*   [SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) - General SDK concepts
*   [V2 examples on GitHub](https://github.com/anthropics/claude-agent-sdk-demos/tree/main/hello-world-v2) - Working code examples

Was this page helpful?

*   [Installation](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#installation)
*   [Quick start](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#quick-start)
*   [One-shot prompt](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#one-shot-prompt)
*   [Basic session](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#basic-session)
*   [Multi-turn conversation](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#multi-turn-conversation)
*   [Session resume](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#session-resume)
*   [Cleanup](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#cleanup)
*   [API reference](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#api-reference)
*   [unstable_v2_createSession()](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#unstable-v2-create-session)
*   [unstable_v2_resumeSession()](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#unstable-v2-resume-session)
*   [unstable_v2_prompt()](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#unstable-v2-prompt)
*   [SDKSession interface](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#sdk-session-interface)
*   [Feature availability](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#feature-availability)
*   [Feedback](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#feedback)
*   [See also](https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview#see-also)
