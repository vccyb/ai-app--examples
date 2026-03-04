Title: Streaming Input

URL Source: https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode

Markdown Content:
Streaming Input - Claude API Docs
===============

Loading...

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Fstreaming-vs-single-mode)

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

Guides Streaming Input

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

Streaming Input
===============

Copy page

Understanding the two input modes for Claude Agent SDK and when to use each

Copy page

Overview
--------

The Claude Agent SDK supports two distinct input modes for interacting with agents:

*   **Streaming Input Mode** (Default & Recommended) - A persistent, interactive session
*   **Single Message Input** - One-shot queries that use session state and resuming

This guide explains the differences, benefits, and use cases for each mode to help you choose the right approach for your application.

Streaming Input Mode (Recommended)
----------------------------------

Streaming input mode is the **preferred** way to use the Claude Agent SDK. It provides full access to the agent's capabilities and enables rich, interactive experiences.

It allows the agent to operate as a long lived process that takes in user input, handles interruptions, surfaces permission requests, and handles session management.

### How It Works

### Benefits

Image Uploads

Attach images directly to messages for visual analysis and understanding

Queued Messages

Send multiple messages that process sequentially, with ability to interrupt

Tool Integration

Full access to all tools and custom MCP servers during the session

Hooks Support

Use lifecycle hooks to customize behavior at various points

Real-time Feedback

See responses as they're generated, not just final results

Context Persistence

Maintain conversation context across multiple turns naturally

### Implementation Example

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";
import { readFile } from "fs/promises";

async function* generateMessages() {
  // First message
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "Analyze this codebase for security issues"
    }
  };

  // Wait for conditions or user input
  await new Promise((resolve) => setTimeout(resolve, 2000));

  // Follow-up with image
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: [
        {
          type: "text",
          text: "Review this architecture diagram"
        },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: await readFile("diagram.png", "base64")
          }
        }
      ]
    }
  };
}

// Process streaming responses
for await (const message of query({
  prompt: generateMessages(),
  options: {
    maxTurns: 10,
    allowedTools: ["Read", "Grep"]
  }
})) {
  if (message.type === "result") {
    console.log(message.result);
  }
}
```

Single Message Input
--------------------

Single message input is simpler but more limited.

### When to Use Single Message Input

Use single message input when:

*   You need a one-shot response
*   You do not need image attachments, hooks, etc.
*   You need to operate in a stateless environment, such as a lambda function

### Limitations

Single message input mode does **not** support:

*   Direct image attachments in messages
*   Dynamic message queueing
*   Real-time interruption
*   Hook integration
*   Natural multi-turn conversations

### Implementation Example

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

// Simple one-shot query
for await (const message of query({
  prompt: "Explain the authentication flow",
  options: {
    maxTurns: 1,
    allowedTools: ["Read", "Grep"]
  }
})) {
  if (message.type === "result") {
    console.log(message.result);
  }
}

// Continue conversation with session management
for await (const message of query({
  prompt: "Now explain the authorization process",
  options: {
    continue: true,
    maxTurns: 1
  }
})) {
  if (message.type === "result") {
    console.log(message.result);
  }
}
```

Was this page helpful?

*   [Overview](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#overview)
*   [Streaming Input Mode (Recommended)](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#streaming-input-mode-recommended)
*   [How It Works](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#how-it-works)
*   [Benefits](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#benefits)
*   [Implementation Example](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#implementation-example)
*   [Single Message Input](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#single-message-input)
*   [When to Use Single Message Input](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#when-to-use-single-message-input)
*   [Limitations](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#limitations)
*   [Implementation Example](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode#implementation-example-2)
