Title: Handle approvals and user input

URL Source: https://platform.claude.com/docs/en/agent-sdk/user-input

Markdown Content:
Handle approvals and user input - Claude API Docs
===============

Loading...

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Fuser-input)

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

Guides User approvals and input

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

Handle approvals and user input
===============================

Copy page

Surface Claude's approval requests and clarifying questions to users, then return their decisions to the SDK.

Copy page

While working on a task, Claude sometimes needs to check in with users. It might need permission before deleting files, or need to ask which database to use for a new project. Your application needs to surface these requests to users so Claude can continue with their input.

Claude requests user input in two situations: when it needs **permission to use a tool** (like deleting files or running commands), and when it has **clarifying questions** (via the `AskUserQuestion` tool). Both trigger your `canUseTool` callback, which pauses execution until you return a response. This is different from normal conversation turns where Claude finishes and waits for your next message.

For clarifying questions, Claude generates the questions and options. Your role is to present them to users and return their selections. You can't add your own questions to this flow; if you need to ask users something yourself, do that separately in your application logic.

This guide shows you how to detect each type of request and respond appropriately.

Detect when Claude needs input
------------------------------

Pass a `canUseTool` callback in your query options. The callback fires whenever Claude needs user input, receiving the tool name and input as arguments:

Python

```
async def handle_tool_request(tool_name, input_data, context):
    # Prompt user and return allow or deny
    ...

options = ClaudeAgentOptions(can_use_tool=handle_tool_request)
```

The callback fires in two cases:

1.   **Tool needs approval**: Claude wants to use a tool that isn't auto-approved by [permission rules](https://platform.claude.com/docs/en/agent-sdk/permissions) or modes. Check `tool_name` for the tool (e.g., `"Bash"`, `"Write"`).
2.   **Claude asks a question**: Claude calls the `AskUserQuestion` tool. Check if `tool_name == "AskUserQuestion"` to handle it differently. If you specify a `tools` array, include `AskUserQuestion` for this to work. See [Handle clarifying questions](https://platform.claude.com/docs/en/agent-sdk/user-input#handle-clarifying-questions) for details.

To automatically allow or deny tools without prompting users, use [hooks](https://platform.claude.com/docs/en/agent-sdk/hooks) instead. Hooks execute before `canUseTool` and can allow, deny, or modify requests based on your own logic. You can also use the [`PermissionRequest` hook](https://platform.claude.com/docs/en/agent-sdk/hooks#available-hooks) to send external notifications (Slack, email, push) when Claude is waiting for approval.

Handle tool approval requests
-----------------------------

Once you've passed a `canUseTool` callback in your query options, it fires when Claude wants to use a tool that isn't auto-approved. Your callback receives two arguments:

| Argument | Description |
| --- | --- |
| `toolName` | The name of the tool Claude wants to use (e.g., `"Bash"`, `"Write"`, `"Edit"`) |
| `input` | The parameters Claude is passing to the tool. Contents vary by tool. |

The `input` object contains tool-specific parameters. Common examples:

| Tool | Input fields |
| --- | --- |
| `Bash` | `command`, `description`, `timeout` |
| `Write` | `file_path`, `content` |
| `Edit` | `file_path`, `old_string`, `new_string` |
| `Read` | `file_path`, `offset`, `limit` |

See the SDK reference for complete input schemas: [Python](https://platform.claude.com/docs/en/agent-sdk/python#tool-inputoutput-types) | [TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript#tool-input-types).

You can display this information to the user so they can decide whether to allow or reject the action, then return the appropriate response.

The following example asks Claude to create and delete a test file. When Claude attempts each operation, the callback prints the tool request to the terminal and prompts for y/n approval.

Python

```
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import (
    HookMatcher,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

async def can_use_tool(
    tool_name: str, input_data: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    # Display the tool request
    print(f"\nTool: {tool_name}")
    if tool_name == "Bash":
        print(f"Command: {input_data.get('command')}")
        if input_data.get("description"):
            print(f"Description: {input_data.get('description')}")
    else:
        print(f"Input: {input_data}")

    # Get user approval
    response = input("Allow this action? (y/n): ")

    # Return allow or deny based on user's response
    if response.lower() == "y":
        # Allow: tool executes with the original (or modified) input
        return PermissionResultAllow(updated_input=input_data)
    else:
        # Deny: tool doesn't execute, Claude sees the message
        return PermissionResultDeny(message="User denied this action")

# Required workaround: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}

async def prompt_stream():
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": "Create a test file in /tmp and then delete it",
        },
    }

async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

In Python, `can_use_tool` requires [streaming mode](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) and a `PreToolUse` hook that returns `{"continue_": True}` to keep the stream open. Without this hook, the stream closes before the permission callback can be invoked.

This example uses a `y/n` flow where any input other than `y` is treated as a denial. In practice, you might build a richer UI that lets users modify the request, provide feedback, or redirect Claude entirely. See [Respond to tool requests](https://platform.claude.com/docs/en/agent-sdk/user-input#respond-to-tool-requests) for all the ways you can respond.

### Respond to tool requests

Your callback returns one of two response types:

| Response | Python | TypeScript |
| --- | --- | --- |
| **Allow** | `PermissionResultAllow(updated_input=...)` | `{ behavior: "allow", updatedInput }` |
| **Deny** | `PermissionResultDeny(message=...)` | `{ behavior: "deny", message }` |

When allowing, pass the tool input (original or modified). When denying, provide a message explaining why. Claude sees this message and may adjust its approach.

Python

```
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

# Allow the tool to execute
return PermissionResultAllow(updated_input=input_data)

# Block the tool
return PermissionResultDeny(message="User rejected this action")
```

Beyond allowing or denying, you can modify the tool's input or provide context that helps Claude adjust its approach:

*   **Approve**: let the tool execute as Claude requested
*   **Approve with changes**: modify the input before execution (e.g., sanitize paths, add constraints)
*   **Reject**: block the tool and tell Claude why
*   **Suggest alternative**: block but guide Claude toward what the user wants instead
*   **Redirect entirely**: use [streaming input](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) to send Claude a completely new instruction

Approve

Approve

Approve with changes

Approve with changes

Reject

Reject

Suggest alternative

Suggest alternative

Redirect entirely

Redirect entirely

Handle clarifying questions
---------------------------

When Claude needs more direction on a task with multiple valid approaches, it calls the `AskUserQuestion` tool. This triggers your `canUseTool` callback with `toolName` set to `AskUserQuestion`. The input contains Claude's questions as multiple-choice options, which you display to the user and return their selections.

Clarifying questions are especially common in [`plan` mode](https://platform.claude.com/docs/en/agent-sdk/permissions#plan-mode-plan), where Claude explores the codebase and asks questions before proposing a plan. This makes plan mode ideal for interactive workflows where you want Claude to gather requirements before making changes.

The following steps show how to handle clarifying questions:

1.   1 
Pass a canUseTool callback  Pass a `canUseTool` callback in your query options. By default, `AskUserQuestion` is available. If you specify a `tools` array to restrict Claude's capabilities (for example, a read-only agent with only `Read`, `Glob`, and `Grep`), include `AskUserQuestion` in that array. Otherwise, Claude won't be able to ask clarifying questions:

Python      ```
async for message in query(
    prompt="Analyze this codebase",
    options=ClaudeAgentOptions(
        # Include AskUserQuestion in your tools list
        tools=["Read", "Glob", "Grep", "AskUserQuestion"],
        can_use_tool=can_use_tool,
    ),
):
    print(message)
```    
2.   2 
Detect AskUserQuestion  In your callback, check if `toolName` equals `AskUserQuestion` to handle it differently from other tools:

Python      ```
async def can_use_tool(tool_name: str, input_data: dict, context):
    if tool_name == "AskUserQuestion":
        # Your implementation to collect answers from the user
        return await handle_clarifying_questions(input_data)
    # Handle other tools normally
    return await prompt_for_approval(tool_name, input_data)
```    
3.   3 
Parse the question input  The input contains Claude's questions in a `questions` array. Each question has a `question` (the text to display), `options` (the choices), and `multiSelect` (whether multiple selections are allowed):

```
{
  "questions": [
    {
      "question": "How should I format the output?",
      "header": "Format",
      "options": [
        { "label": "Summary", "description": "Brief overview" },
        { "label": "Detailed", "description": "Full explanation" }
      ],
      "multiSelect": false
    },
    {
      "question": "Which sections should I include?",
      "header": "Sections",
      "options": [
        { "label": "Introduction", "description": "Opening context" },
        { "label": "Conclusion", "description": "Final summary" }
      ],
      "multiSelect": true
    }
  ]
}
```       
See [Question format](https://platform.claude.com/docs/en/agent-sdk/user-input#question-format) for full field descriptions. 
4.   4 
Collect answers from the user  Present the questions to the user and collect their selections. How you do this depends on your application: a terminal prompt, a web form, a mobile dialog, etc. 
5.   5 
Return answers to Claude  Build the `answers` object as a record where each key is the `question` text and each value is the selected option's `label`:

| From the question object | Use as |
| --- | --- |
| `question` field (e.g., `"How should I format the output?"`) | Key |
| Selected option's `label` field (e.g., `"Summary"`) | Value | 
For multi-select questions, join multiple labels with `", "`. If you [support free-text input](https://platform.claude.com/docs/en/agent-sdk/user-input#support-free-text-input), use the user's custom text as the value.

Python      ```
return PermissionResultAllow(
    updated_input={
        "questions": input_data.get("questions", []),
        "answers": {
            "How should I format the output?": "Summary",
            "Which sections should I include?": "Introduction, Conclusion",
        },
    }
)
```    

### Question format

The input contains Claude's generated questions in a `questions` array. Each question has these fields:

| Field | Description |
| --- | --- |
| `question` | The full question text to display |
| `header` | Short label for the question (max 12 characters) |
| `options` | Array of 2-4 choices, each with `label` and `description` |
| `multiSelect` | If `true`, users can select multiple options |

Here's an example of the structure you'll receive:

```
{
  "questions": [
    {
      "question": "How should I format the output?",
      "header": "Format",
      "options": [
        { "label": "Summary", "description": "Brief overview of key points" },
        { "label": "Detailed", "description": "Full explanation with examples" }
      ],
      "multiSelect": false
    }
  ]
}
```

### Response format

Return an `answers` object mapping each question's `question` field to the selected option's `label`:

| Field | Description |
| --- | --- |
| `questions` | Pass through the original questions array (required for tool processing) |
| `answers` | Object where keys are question text and values are selected labels |

For multi-select questions, join multiple labels with `", "`. For free-text input, use the user's custom text directly.

```
{
  "questions": [
    // ...
  ],
  "answers": {
    "How should I format the output?": "Summary",
    "Which sections should I include?": "Introduction, Conclusion"
  }
}
```

#### Support free-text input

Claude's predefined options won't always cover what users want. To let users type their own answer:

*   Display an additional "Other" choice after Claude's options that accepts text input
*   Use the user's custom text as the answer value (not the word "Other")

See the [complete example](https://platform.claude.com/docs/en/agent-sdk/user-input#complete-example) below for a full implementation.

### Complete example

Claude asks clarifying questions when it needs user input to proceed. For example, when asked to help decide on a tech stack for a mobile app, Claude might ask about cross-platform vs native, backend preferences, or target platforms. These questions help Claude make decisions that match the user's preferences rather than guessing.

This example handles those questions in a terminal application. Here's what happens at each step:

1.   **Route the request**: The `canUseTool` callback checks if the tool name is `"AskUserQuestion"` and routes to a dedicated handler
2.   **Display questions**: The handler loops through the `questions` array and prints each question with numbered options
3.   **Collect input**: The user can enter a number to select an option, or type free text directly (e.g., "jquery", "i don't know")
4.   **Map answers**: The code checks if input is numeric (uses the option's label) or free text (uses the text directly)
5.   **Return to Claude**: The response includes both the original `questions` array and the `answers` mapping

Python

```
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import HookMatcher, PermissionResultAllow

def parse_response(response: str, options: list) -> str:
    """Parse user input as option number(s) or free text."""
    try:
        indices = [int(s.strip()) - 1 for s in response.split(",")]
        labels = [options[i]["label"] for i in indices if 0 <= i < len(options)]
        return ", ".join(labels) if labels else response
    except ValueError:
        return response

async def handle_ask_user_question(input_data: dict) -> PermissionResultAllow:
    """Display Claude's questions and collect user answers."""
    answers = {}

    for q in input_data.get("questions", []):
        print(f"\n{q['header']}: {q['question']}")

        options = q["options"]
        for i, opt in enumerate(options):
            print(f"  {i + 1}. {opt['label']} - {opt['description']}")
        if q.get("multiSelect"):
            print("  (Enter numbers separated by commas, or type your own answer)")
        else:
            print("  (Enter a number, or type your own answer)")

        response = input("Your choice: ").strip()
        answers[q["question"]] = parse_response(response, options)

    return PermissionResultAllow(
        updated_input={
            "questions": input_data.get("questions", []),
            "answers": answers,
        }
    )

async def can_use_tool(
    tool_name: str, input_data: dict, context
) -> PermissionResultAllow:
    # Route AskUserQuestion to our question handler
    if tool_name == "AskUserQuestion":
        return await handle_ask_user_question(input_data)
    # Auto-approve other tools for this example
    return PermissionResultAllow(updated_input=input_data)

async def prompt_stream():
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": "Help me decide on the tech stack for a new mobile app",
        },
    }

# Required workaround: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}

async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

Limitations
-----------

*   **Subagents**: `AskUserQuestion` is not currently available in subagents spawned via the Task tool
*   **Question limits**: each `AskUserQuestion` call supports 1-4 questions with 2-4 options each

Other ways to get user input
----------------------------

The `canUseTool` callback and `AskUserQuestion` tool cover most approval and clarification scenarios, but the SDK offers other ways to get input from users:

### Streaming input

Use [streaming input](https://platform.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) when you need to:

*   **Interrupt the agent mid-task**: send a cancel signal or change direction while Claude is working
*   **Provide additional context**: add information Claude needs without waiting for it to ask
*   **Build chat interfaces**: let users send follow-up messages during long-running operations

Streaming input is ideal for conversational UIs where users interact with the agent throughout execution, not just at approval checkpoints.

### Custom tools

Use [custom tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools) when you need to:

*   **Collect structured input**: build forms, wizards, or multi-step workflows that go beyond `AskUserQuestion`'s multiple-choice format
*   **Integrate external approval systems**: connect to existing ticketing, workflow, or approval platforms
*   **Implement domain-specific interactions**: create tools tailored to your application's needs, like code review interfaces or deployment checklists

Custom tools give you full control over the interaction, but require more implementation work than using the built-in `canUseTool` callback.

Related resources
-----------------

*   [Configure permissions](https://platform.claude.com/docs/en/agent-sdk/permissions): set up permission modes and rules
*   [Control execution with hooks](https://platform.claude.com/docs/en/agent-sdk/hooks): run custom code at key points in the agent lifecycle
*   [TypeScript SDK reference](https://platform.claude.com/docs/en/agent-sdk/typescript#canusetool): full canUseTool API documentation

Was this page helpful?

*   [Detect when Claude needs input](https://platform.claude.com/docs/en/agent-sdk/user-input#detect-when-claude-needs-input)
*   [Handle tool approval requests](https://platform.claude.com/docs/en/agent-sdk/user-input#handle-tool-approval-requests)
*   [Respond to tool requests](https://platform.claude.com/docs/en/agent-sdk/user-input#respond-to-tool-requests)
*   [Handle clarifying questions](https://platform.claude.com/docs/en/agent-sdk/user-input#handle-clarifying-questions)
*   [Question format](https://platform.claude.com/docs/en/agent-sdk/user-input#question-format)
*   [Response format](https://platform.claude.com/docs/en/agent-sdk/user-input#response-format)
*   [Complete example](https://platform.claude.com/docs/en/agent-sdk/user-input#complete-example)
*   [Limitations](https://platform.claude.com/docs/en/agent-sdk/user-input#limitations)
*   [Other ways to get user input](https://platform.claude.com/docs/en/agent-sdk/user-input#other-ways-to-get-user-input)
*   [Streaming input](https://platform.claude.com/docs/en/agent-sdk/user-input#streaming-input)
*   [Custom tools](https://platform.claude.com/docs/en/agent-sdk/user-input#custom-tools)
*   [Related resources](https://platform.claude.com/docs/en/agent-sdk/user-input#related-resources)
