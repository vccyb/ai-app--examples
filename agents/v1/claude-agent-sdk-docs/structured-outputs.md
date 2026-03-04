Title: Get structured output from agents

URL Source: https://platform.claude.com/docs/en/agent-sdk/structured-outputs

Markdown Content:
Get structured output from agents - Claude API Docs
===============

Loading...

[](https://platform.claude.com/docs/en/home)
*   [Developer Guide](https://platform.claude.com/docs/en/intro)
*   [API Reference](https://platform.claude.com/docs/en/api/overview)
*   [MCP](https://modelcontextprotocol.io/)
*   [Resources](https://platform.claude.com/docs/en/resources/overview)
*   [Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

English[Log in](https://platform.claude.com/login?returnTo=%2Fdocs%2Fen%2Fagent-sdk%2Fstructured-outputs)

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

Guides Structured outputs in the SDK

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

Get structured output from agents
=================================

Copy page

Return validated JSON from agent workflows using JSON Schema, Zod, or Pydantic. Get type-safe, structured data after multi-turn tool use.

Copy page

Structured outputs let you define the exact shape of data you want back from an agent. The agent can use any tools it needs to complete the task, and you still get validated JSON matching your schema at the end. Define a [JSON Schema](https://json-schema.org/understanding-json-schema/about) for the structure you need, and the SDK guarantees the output matches it.

For full type safety, use [Zod](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#type-safe-schemas-with-zod-and-pydantic) (TypeScript) or [Pydantic](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#type-safe-schemas-with-zod-and-pydantic) (Python) to define your schema and get strongly-typed objects back.

Why structured outputs?
-----------------------

Agents return free-form text by default, which works for chat but not when you need to use the output programmatically. Structured outputs give you typed data you can pass directly to your application logic, database, or UI components.

Consider a recipe app where an agent searches the web and brings back recipes. Without structured outputs, you get free-form text that you'd need to parse yourself. With structured outputs, you define the shape you want and get typed data you can use directly in your app.

### Without structured outputs

### With structured outputs

Quick start
-----------

To use structured outputs, define a [JSON Schema](https://json-schema.org/understanding-json-schema/about) describing the shape of data you want, then pass it to `query()` via the `outputFormat` option (TypeScript) or `output_format` option (Python). When the agent finishes, the result message includes a `structured_output` field with validated data matching your schema.

The example below asks the agent to research Anthropic and return the company name, year founded, and headquarters as structured output.

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

// Define the shape of data you want back
const schema = {
  type: "object",
  properties: {
    company_name: { type: "string" },
    founded_year: { type: "number" },
    headquarters: { type: "string" }
  },
  required: ["company_name"]
};

for await (const message of query({
  prompt: "Research Anthropic and provide key company information",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: schema
    }
  }
})) {
  // The result message contains structured_output with validated data
  if (message.type === "result" && message.structured_output) {
    console.log(message.structured_output);
    // { company_name: "Anthropic", founded_year: 2021, headquarters: "San Francisco, CA" }
  }
}
```

Type-safe schemas with Zod and Pydantic
---------------------------------------

Instead of writing JSON Schema by hand, you can use [Zod](https://zod.dev/) (TypeScript) or [Pydantic](https://docs.pydantic.dev/latest/) (Python) to define your schema. These libraries generate the JSON Schema for you and let you parse the response into a fully-typed object you can use throughout your codebase with autocomplete and type checking.

The example below defines a schema for a feature implementation plan with a summary, list of steps (each with complexity level), and potential risks. The agent plans the feature and returns a typed `FeaturePlan` object. You can then access properties like `plan.summary` and iterate over `plan.steps` with full type safety.

TypeScript

```
import { z } from "zod";
import { query } from "@anthropic-ai/claude-agent-sdk";

// Define schema with Zod
const FeaturePlan = z.object({
  feature_name: z.string(),
  summary: z.string(),
  steps: z.array(
    z.object({
      step_number: z.number(),
      description: z.string(),
      estimated_complexity: z.enum(["low", "medium", "high"])
    })
  ),
  risks: z.array(z.string())
});

type FeaturePlan = z.infer<typeof FeaturePlan>;

// Convert to JSON Schema
const schema = z.toJSONSchema(FeaturePlan);

// Use in query
for await (const message of query({
  prompt:
    "Plan how to add dark mode support to a React app. Break it into implementation steps.",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: schema
    }
  }
})) {
  if (message.type === "result" && message.structured_output) {
    // Validate and get fully typed result
    const parsed = FeaturePlan.safeParse(message.structured_output);
    if (parsed.success) {
      const plan: FeaturePlan = parsed.data;
      console.log(`Feature: ${plan.feature_name}`);
      console.log(`Summary: ${plan.summary}`);
      plan.steps.forEach((step) => {
        console.log(`${step.step_number}. [${step.estimated_complexity}] ${step.description}`);
      });
    }
  }
}
```

**Benefits:**

*   Full type inference (TypeScript) and type hints (Python)
*   Runtime validation with `safeParse()` or `model_validate()`
*   Better error messages
*   Composable, reusable schemas

Output format configuration
---------------------------

The `outputFormat` (TypeScript) or `output_format` (Python) option accepts an object with:

*   `type`: Set to `"json_schema"` for structured outputs
*   `schema`: A [JSON Schema](https://json-schema.org/understanding-json-schema/about) object defining your output structure. You can generate this from a Zod schema with `z.toJSONSchema()` or a Pydantic model with `.model_json_schema()`

The SDK supports standard JSON Schema features including all basic types (object, array, string, number, boolean, null), `enum`, `const`, `required`, nested objects, and `$ref` definitions. For the full list of supported features and limitations, see [JSON Schema limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations).

Example: TODO tracking agent
----------------------------

This example demonstrates how structured outputs work with multi-step tool use. The agent needs to find TODO comments in the codebase, then look up git blame information for each one. It autonomously decides which tools to use (Grep to search, Bash to run git commands) and combines the results into a single structured response.

The schema includes optional fields (`author` and `date`) since git blame information might not be available for all files. The agent fills in what it can find and omits the rest.

TypeScript

```
import { query } from "@anthropic-ai/claude-agent-sdk";

// Define structure for TODO extraction
const todoSchema = {
  type: "object",
  properties: {
    todos: {
      type: "array",
      items: {
        type: "object",
        properties: {
          text: { type: "string" },
          file: { type: "string" },
          line: { type: "number" },
          author: { type: "string" },
          date: { type: "string" }
        },
        required: ["text", "file", "line"]
      }
    },
    total_count: { type: "number" }
  },
  required: ["todos", "total_count"]
};

// Agent uses Grep to find TODOs, Bash to get git blame info
for await (const message of query({
  prompt: "Find all TODO comments in this codebase and identify who added them",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: todoSchema
    }
  }
})) {
  if (message.type === "result" && message.structured_output) {
    const data = message.structured_output;
    console.log(`Found ${data.total_count} TODOs`);
    data.todos.forEach((todo) => {
      console.log(`${todo.file}:${todo.line} - ${todo.text}`);
      if (todo.author) {
        console.log(`  Added by ${todo.author} on ${todo.date}`);
      }
    });
  }
}
```

Error handling
--------------

Structured output generation can fail when the agent cannot produce valid JSON matching your schema. This typically happens when the schema is too complex for the task, the task itself is ambiguous, or the agent hits its retry limit trying to fix validation errors.

When an error occurs, the result message has a `subtype` indicating what went wrong:

| Subtype | Meaning |
| --- | --- |
| `success` | Output was generated and validated successfully |
| `error_max_structured_output_retries` | Agent couldn't produce valid output after multiple attempts |

The example below checks the `subtype` field to determine whether the output was generated successfully or if you need to handle a failure:

TypeScript

```
for await (const msg of query({
  prompt: "Extract contact info from the document",
  options: {
    outputFormat: {
      type: "json_schema",
      schema: contactSchema
    }
  }
})) {
  if (msg.type === "result") {
    if (msg.subtype === "success" && msg.structured_output) {
      // Use the validated output
      console.log(msg.structured_output);
    } else if (msg.subtype === "error_max_structured_output_retries") {
      // Handle the failure - retry with simpler prompt, fall back to unstructured, etc.
      console.error("Could not produce valid output");
    }
  }
}
```

**Tips for avoiding errors:**

*   **Keep schemas focused.** Deeply nested schemas with many required fields are harder to satisfy. Start simple and add complexity as needed.
*   **Match schema to task.** If the task might not have all the information your schema requires, make those fields optional.
*   **Use clear prompts.** Ambiguous prompts make it harder for the agent to know what output to produce.

Related resources
-----------------

*   [JSON Schema documentation](https://json-schema.org/): learn JSON Schema syntax for defining complex schemas with nested objects, arrays, enums, and validation constraints
*   [API Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): use structured outputs with the Claude API directly for single-turn requests without tool use
*   [Custom tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools): give your agent custom tools to call during execution before returning structured output

Was this page helpful?

*   [Why structured outputs?](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#why-structured-outputs)
*   [Quick start](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#quick-start)
*   [Type-safe schemas with Zod and Pydantic](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#type-safe-schemas-with-zod-and-pydantic)
*   [Output format configuration](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#output-format-configuration)
*   [Example: TODO tracking agent](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#example-todo-tracking-agent)
*   [Error handling](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#error-handling)
*   [Related resources](https://platform.claude.com/docs/en/agent-sdk/structured-outputs#related-resources)
