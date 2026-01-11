# Function Call Demo - Vue 3

基于 Vue 3 + TypeScript + Vite 的 AI 聊天应用，演示了 LangChain Function Calling 功能。

## 功能特点

- **Function Calling**: 集成 LangChain 的工具调用能力
- **实时流式响应**: 使用 SSE (Server-Sent Events) 实现流式输出
- **对话历史**: 自动保存和加载对话历史
- **现代 UI**: 基于 Tailwind CSS 4.x 的简洁界面

## 可用工具

1. **get_server_time**: 获取服务器当前时间
2. **search_docs**: 搜索项目文档（示例）

## 开发

### 环境准备

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 DashScope API Key：
```
API_KEY=your_dashscope_api_key_here
```

### 安装依赖

```bash
pnpm install
```

### 启动开发服务器

在两个终端中分别运行：

```bash
# 终端 1: 启动前端开发服务器
pnpm run dev:ui

# 终端 2: 启动后端服务器
pnpm run dev:server
```

访问 http://localhost:5173 查看应用。

### 构建

```bash
pnpm run build
```

## 技术栈

- **前端**: Vue 3 (Composition API + `<script setup>`), TypeScript, Vite, Tailwind CSS 4.x
- **后端**: Express.js, Node.js
- **AI**: LangChain, Qwen (通义千问) via DashScope API
- **流式通信**: Server-Sent Events (SSE)
- **Schema 验证**: Zod
