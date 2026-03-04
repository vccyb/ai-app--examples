Title: Agent SDK overview

URL Source: https://platform.claude.com/docs/en/agent-sdk/overview

Markdown Content:
Agent SDK

Build production AI agents with Claude Code as a library

The Claude Code SDK has been renamed to the Claude Agent SDK. If you're migrating from the old SDK, see the [Migration Guide](https://platform.claude.com/docs/en/agent-sdk/migration-guide).

Build AI agents that autonomously read files, run commands, search the web, edit code, and more. The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript.

The Agent SDK includes built-in tools for reading files, running commands, and editing code, so your agent can start working immediately without you implementing tool execution. Dive into the quickstart or explore real agents built with the SDK:

Get started
-----------

1.   Install the SDK 
2.   Set your API key 

Get an API key from the [Console](https://platform.claude.com/), then set it as an environment variable:

The SDK also supports authentication via third-party API providers:

    *   **Amazon Bedrock**: set `CLAUDE_CODE_USE_BEDROCK=1` environment variable and configure AWS credentials
    *   **Google Vertex AI**: set `CLAUDE_CODE_USE_VERTEX=1` environment variable and configure Google Cloud credentials
    *   **Microsoft Azure**: set `CLAUDE_CODE_USE_FOUNDRY=1` environment variable and configure Azure credentials

See the setup guides for [Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), or [Azure AI Foundry](https://code.claude.com/docs/en/azure-ai-foundry) for details.

Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Please use the API key authentication methods described in this document instead.

3.   Run your first agent This example creates an agent that lists files in your current directory using built-in tools. 

**Ready to build?** Follow the [Quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart) to create an agent that finds and fixes bugs in minutes.

Capabilities
------------

Everything that makes Claude Code powerful is available in the SDK:

Your agent can read files, run commands, and search codebases out of the box. Key tools include:

| Tool | What it does |
| --- | --- |
| **Read** | Read any file in the working directory |
| **Write** | Create new files |
| **Edit** | Make precise edits to existing files |
| **Bash** | Run terminal commands, scripts, git operations |
| **Glob** | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| **Grep** | Search file contents with regex |
| **WebSearch** | Search the web for current information |
| **WebFetch** | Fetch and parse web page content |
| **[AskUserQuestion](https://platform.claude.com/docs/en/agent-sdk/user-input#handle-clarifying-questions)** | Ask the user clarifying questions with multiple choice options |

This example creates an agent that searches your codebase for TODO comments:

### Claude Code features

The SDK also supports Claude Code's filesystem-based configuration. To use these features, set `setting_sources=["project"]` (Python) or `settingSources: ['project']` (TypeScript) in your options.

| Feature | Description | Location |
| --- | --- | --- |
| [Skills](https://platform.claude.com/docs/en/agent-sdk/skills) | Specialized capabilities defined in Markdown | `.claude/skills/SKILL.md` |
| [Slash commands](https://platform.claude.com/docs/en/agent-sdk/slash-commands) | Custom commands for common tasks | `.claude/commands/*.md` |
| [Memory](https://platform.claude.com/docs/en/agent-sdk/modifying-system-prompts) | Project context and instructions | `CLAUDE.md` or `.claude/CLAUDE.md` |
| [Plugins](https://platform.claude.com/docs/en/agent-sdk/plugins) | Extend with custom commands, agents, and MCP servers | Programmatic via `plugins` option |

Compare the Agent SDK to other Claude tools
-------------------------------------------

The Claude platform offers multiple ways to build with Claude. Here's how the Agent SDK fits in:

The [Anthropic Client SDK](https://platform.claude.com/docs/en/api/client-sdks) gives you direct API access: you send prompts and implement tool execution yourself. The **Agent SDK** gives you Claude with built-in tool execution.

With the Client SDK, you implement a tool loop. With the Agent SDK, Claude handles it:

Changelog
---------

View the full changelog for SDK updates, bug fixes, and new features:

*   **TypeScript SDK**: [view CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md)
*   **Python SDK**: [view CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)

Reporting bugs
--------------

If you encounter bugs or issues with the Agent SDK:

*   **TypeScript SDK**: [report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
*   **Python SDK**: [report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-python/issues)

Branding guidelines
-------------------

For partners integrating the Claude Agent SDK, use of Claude branding is optional. When referencing Claude in your product:

**Allowed:**

*   "Claude Agent" (preferred for dropdown menus)
*   "Claude" (when within a menu already labeled "Agents")
*   "{YourAgentName} Powered by Claude" (if you have an existing agent name)

**Not permitted:**

*   "Claude Code" or "Claude Code Agent"
*   Claude Code-branded ASCII art or visual elements that mimic Claude Code

Your product should maintain its own branding and not appear to be Claude Code or any Anthropic product. For questions about branding compliance, contact the Anthropic [sales team](https://www.anthropic.com/contact-sales).

License and terms
-----------------

Use of the Claude Agent SDK is governed by [Anthropic's Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms), including when you use it to power products and services that you make available to your own customers and end users, except to the extent a specific component or dependency is covered by a different license as indicated in that component's LICENSE file.

Next steps
----------

Was this page helpful?
