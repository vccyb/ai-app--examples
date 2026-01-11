# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a learning lab for building AI chatbot applications, demonstrating progressive evolution from CLI tools to modern web applications with real-time streaming and function calling capabilities. The repository contains 6 independent sub-projects.

## Sub-Project Structure

```
01-chatbot-cli/          # Basic CLI chatbot (TypeScript + Node.js readline)
02-chatbot-cli-stream/    # CLI with streaming (TypeScript + LangChain)
03-chatbot-cli-langchain/ # Advanced CLI patterns (TypeScript + LangChain)
04-chatbot-ui/            # React 19 web app with SSE streaming
05-chatbot-ui-vue/        # Vue 3 web app with SSE streaming
06-function-call-vue/     # Vue app with LangChain function calling
```

## Common Development Commands

### CLI Projects (01-03)
```bash
# From project directory (e.g., 01-chatbot-cli/)
npm start              # Run the CLI application
```

### Web Projects (04-06)
```bash
# From project directory (e.g., 04-chatbot-ui/)
npm run dev:ui         # Start Vite dev server (frontend)
npm run dev:server     # Start Express server with watch mode (backend)
npm run build          # Build for production
npm run preview        # Preview production build
```

Note: Run `npm run dev:ui` and `npm run dev:server` in separate terminals for full-stack development.

## Environment Configuration

All projects require a `.env` file in the project root:
```
API_KEY=your_dashscope_api_key
```

The API key is for Alibaba's DashScope API (Qwen model).

## Technology Stack

### Core Technologies
- **LangChain** (`@langchain/core`, `@langchain/openai`): AI orchestration framework used across all projects
- **Qwen Model** (`qwen-turbo`): Alibaba's AI model accessed via DashScope API
- **TypeScript**: Type safety throughout

### Frontend
- **04-chatbot-ui**: React 19, Vite, Tailwind CSS 4.x
- **05-chatbot-ui-vue**: Vue 3 (Composition API with `<script setup>`), Vite, Tailwind CSS 4.x
- **06-function-call-vue**: Vue 3, Vite, Tailwind CSS 4.x, Zod (schema validation)

### Backend
- **Express.js**: Web server for web projects (04-06)
- **SSE (Server-Sent Events)**: Real-time streaming protocol for chat responses
- **Node.js**: Runtime with `--env-file` flag for `.env` loading

## Architecture Patterns

### Message Structure
```typescript
type Message = {
  role: 'system' | 'user' | 'assistant';
  content: string;
}
```

### API Configuration
```typescript
const BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1';
const MODEL = 'qwen-turbo'; // or 'qwen-plus'
```

### LangChain Integration
- All projects use `ChatOpenAI` from `@langchain/openai` configured for DashScope
- Message types: `HumanMessage`, `AIMessage`, `ToolMessage` (for function calls)
- Streaming via `.stream()` method for CLI, SSE for web apps

### SSE Implementation (Web Projects)
- **Endpoints**: `GET /sse` and `POST /sse`
- **Frontend**: `EventSource` for GET, `fetch` with readable stream for POST
- **Response Format**: `data: {JSON}\n\n`
- **Termination**: `event: close\ndata:\n\n`
- **Headers**: `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive`

### Function Calling (06-function-call-vue)
- Tools defined using LangChain's `tool()` function with Zod schemas
- Model bound to tools: `const bound = model.bindTools(tools)`
- Tool invocation loop:
  1. Invoke model → check for `ai.tool_calls`
  2. Execute tools → append `ToolMessage` results
  3. Repeat until no more tool calls
  4. Final response streamed via SSE

## Code Organization

### CLI Projects
- Single `main.ts` file with all logic
- Direct API interaction via LangChain

### Web Projects
```
04-chatbot-ui/
├── src/              # React components
├── server/           # Express server
├── types/            # TypeScript type definitions

05-chatbot-ui-vue/ & 06-function-call-vue/
├── src/
│   └── App.vue       # Single Vue component with all logic
└── server/
    └── main.ts       # Express server with SSE/function call endpoints
```

## System Prompt

All applications use a Chinese system prompt instructing the AI to act as an educational tutor that:
- Guides students rather than giving direct answers
- Adapts to the student's level
- Uses interactive teaching methods (Socratic method, examples)
- Avoids doing homework for students

## Package Manager

This project uses **pnpm** as the package manager (evidenced by `node_modules/.pnpm/` structure).

## Key Implementation Details

1. **Auto-scrolling**: Web apps implement chat container auto-scroll for new messages
2. **Message History**: Server-side message array maintained across requests
3. **Type Safety**: All projects use TypeScript with strict mode
4. **Streaming**: CLI uses natural iteration; web apps use SSE with partial chunks
5. **Tool Definitions**: In project 06, tools are simple async functions wrapped with `tool()` decorator
