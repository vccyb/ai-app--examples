Title: Migrate to Claude Agent SDK

URL Source: https://platform.claude.com/docs/en/agent-sdk/migration-guide

Markdown Content:
Migrate to Claude Agent SDK - Claude API Docs
===============

Loading...

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Fmigration-guide)

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

Agent SDK Migration Guide

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

Migrate to Claude Agent SDK
===========================

Copy page

Guide for migrating the Claude Code TypeScript and Python SDKs to the Claude Agent SDK

Copy page

Overview
--------

The Claude Code SDK has been renamed to the **Claude Agent SDK** and its documentation has been reorganized. This change reflects the SDK's broader capabilities for building AI agents beyond just coding tasks.

What's Changed
--------------

| Aspect | Old | New |
| --- | --- | --- |
| **Package Name (TS/JS)** | `@anthropic-ai/claude-code` | `@anthropic-ai/claude-agent-sdk` |
| **Python Package** | `claude-code-sdk` | `claude-agent-sdk` |
| **Documentation Location** | Claude Code docs | API Guide → Agent SDK section |

**Documentation Changes:** The Agent SDK documentation has moved from the Claude Code docs to the API Guide under a dedicated [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) section. The Claude Code docs now focus on the CLI tool and automation features.

Migration Steps
---------------

### For TypeScript/JavaScript Projects

**1. Uninstall the old package:**

`npm uninstall @anthropic-ai/claude-code`

**2. Install the new package:**

`npm install @anthropic-ai/claude-agent-sdk`

**3. Update your imports:**

Change all imports from `@anthropic-ai/claude-code` to `@anthropic-ai/claude-agent-sdk`:

```
// Before
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";

// After
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
```

**4. Update package.json dependencies:**

If you have the package listed in your `package.json`, update it:

Before:

```
{
  "dependencies": {
    "@anthropic-ai/claude-code": "^0.0.42"
  }
}
```

After:

```
{
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.2.0"
  }
}
```

That's it! No other code changes are required.

### For Python Projects

**1. Uninstall the old package:**

`pip uninstall claude-code-sdk`

**2. Install the new package:**

`pip install claude-agent-sdk`

**3. Update your imports:**

Change all imports from `claude_code_sdk` to `claude_agent_sdk`:

```
# Before
from claude_code_sdk import query, ClaudeCodeOptions

# After
from claude_agent_sdk import query, ClaudeAgentOptions
```

**4. Update type names:**

Change `ClaudeCodeOptions` to `ClaudeAgentOptions`:

```
# Before
from claude_code_sdk import query, ClaudeCodeOptions

options = ClaudeCodeOptions(model="claude-opus-4-6")

# After
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(model="claude-opus-4-6")
```

**5. Review [breaking changes](https://platform.claude.com/docs/en/agent-sdk/migration-guide#breaking-changes)**

Make any code changes needed to complete the migration.

Breaking changes
----------------

To improve isolation and explicit configuration, Claude Agent SDK v0.1.0 introduces breaking changes for users migrating from Claude Code SDK. Review this section carefully before migrating.

### Python: ClaudeCodeOptions renamed to ClaudeAgentOptions

**What changed:** The Python SDK type `ClaudeCodeOptions` has been renamed to `ClaudeAgentOptions`.

**Migration:**

```
# BEFORE (claude-code-sdk)
from claude_code_sdk import query, ClaudeCodeOptions

options = ClaudeCodeOptions(model="claude-opus-4-6", permission_mode="acceptEdits")

# AFTER (claude-agent-sdk)
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(model="claude-opus-4-6", permission_mode="acceptEdits")
```

**Why this changed:** The type name now matches the "Claude Agent SDK" branding and provides consistency across the SDK's naming conventions.

### System prompt no longer default

**What changed:** The SDK no longer uses Claude Code's system prompt by default.

**Migration:**

TypeScript

```
// BEFORE (v0.0.x) - Used Claude Code's system prompt by default
const result = query({ prompt: "Hello" });

// AFTER (v0.1.0) - Uses minimal system prompt by default
// To get the old behavior, explicitly request Claude Code's preset:
const result = query({
  prompt: "Hello",
  options: {
    systemPrompt: { type: "preset", preset: "claude_code" }
  }
});

// Or use a custom system prompt:
const result = query({
  prompt: "Hello",
  options: {
    systemPrompt: "You are a helpful coding assistant"
  }
});
```

**Why this changed:** Provides better control and isolation for SDK applications. You can now build agents with custom behavior without inheriting Claude Code's CLI-focused instructions.

### Settings Sources No Longer Loaded by Default

**What changed:** The SDK no longer reads from filesystem settings (CLAUDE.md, settings.json, slash commands, etc.) by default.

**Migration:**

TypeScript

```
// BEFORE (v0.0.x) - Loaded all settings automatically
const result = query({ prompt: "Hello" });
// Would read from:
// - ~/.claude/settings.json (user)
// - .claude/settings.json (project)
// - .claude/settings.local.json (local)
// - CLAUDE.md files
// - Custom slash commands

// AFTER (v0.1.0) - No settings loaded by default
// To get the old behavior:
const result = query({
  prompt: "Hello",
  options: {
    settingSources: ["user", "project", "local"]
  }
});

// Or load only specific sources:
const result = query({
  prompt: "Hello",
  options: {
    settingSources: ["project"] // Only project settings
  }
});
```

**Why this changed:** Ensures SDK applications have predictable behavior independent of local filesystem configurations. This is especially important for:

*   **CI/CD environments** - Consistent behavior without local customizations
*   **Deployed applications** - No dependency on filesystem settings
*   **Testing** - Isolated test environments
*   **Multi-tenant systems** - Prevent settings leakage between users

**Backward compatibility:** If your application relied on filesystem settings (custom slash commands, CLAUDE.md instructions, etc.), add `settingSources: ['user', 'project', 'local']` to your options.

Why the Rename?
---------------

The Claude Code SDK was originally designed for coding tasks, but it has evolved into a powerful framework for building all types of AI agents. The new name "Claude Agent SDK" better reflects its capabilities:

*   Building business agents (legal assistants, finance advisors, customer support)
*   Creating specialized coding agents (SRE bots, security reviewers, code review agents)
*   Developing custom agents for any domain with tool use, MCP integration, and more

Getting Help
------------

If you encounter any issues during migration:

**For TypeScript/JavaScript:**

1.   Check that all imports are updated to use `@anthropic-ai/claude-agent-sdk`
2.   Verify your package.json has the new package name
3.   Run `npm install` to ensure dependencies are updated

**For Python:**

1.   Check that all imports are updated to use `claude_agent_sdk`
2.   Verify your requirements.txt or pyproject.toml has the new package name
3.   Run `pip install claude-agent-sdk` to ensure the package is installed

Next Steps
----------

*   Explore the [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview) to learn about available features
*   Check out the [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript) for detailed API documentation
*   Review the [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python) for Python-specific documentation
*   Learn about [Custom Tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools) and [MCP Integration](https://platform.claude.com/docs/en/agent-sdk/mcp)

Was this page helpful?

*   [Overview](https://platform.claude.com/docs/en/agent-sdk/migration-guide#overview)
*   [What's Changed](https://platform.claude.com/docs/en/agent-sdk/migration-guide#whats-changed)
*   [Migration Steps](https://platform.claude.com/docs/en/agent-sdk/migration-guide#migration-steps)
*   [For TypeScript/JavaScript Projects](https://platform.claude.com/docs/en/agent-sdk/migration-guide#for-type-script-java-script-projects)
*   [For Python Projects](https://platform.claude.com/docs/en/agent-sdk/migration-guide#for-python-projects)
*   [Breaking changes](https://platform.claude.com/docs/en/agent-sdk/migration-guide#breaking-changes)
*   [Python: ClaudeCodeOptions renamed to ClaudeAgentOptions](https://platform.claude.com/docs/en/agent-sdk/migration-guide#python-claude-code-options-renamed-to-claude-agent-options)
*   [System prompt no longer default](https://platform.claude.com/docs/en/agent-sdk/migration-guide#system-prompt-no-longer-default)
*   [Settings Sources No Longer Loaded by Default](https://platform.claude.com/docs/en/agent-sdk/migration-guide#settings-sources-no-longer-loaded-by-default)
*   [Why the Rename?](https://platform.claude.com/docs/en/agent-sdk/migration-guide#why-the-rename)
*   [Getting Help](https://platform.claude.com/docs/en/agent-sdk/migration-guide#getting-help)
*   [Next Steps](https://platform.claude.com/docs/en/agent-sdk/migration-guide#next-steps)
