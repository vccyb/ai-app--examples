import express from 'express'
import type { Request, Response } from 'express'
import { ChatOpenAI } from '@langchain/openai'
import { AIMessage, BaseMessage, HumanMessage, ToolMessage } from '@langchain/core/messages'
import { tool } from '@langchain/core/tools'
import { z } from 'zod'

type ChatMessage = { type: 'user' | 'assistant', payload: { content: string }, partial?: boolean }

const API_KEY = process.env.API_KEY
const BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
const MODEL = 'qwen-turbo'

if (!API_KEY) throw new Error('API_KEY is required')

const model = new ChatOpenAI({ model: MODEL, configuration: { apiKey: API_KEY, baseURL: BASE_URL } })

const tools = [
  tool(async () => new Date().toISOString(), {
    name: 'get_server_time',
    description: '获取服务器当前时间，返回ISO字符串',
    schema: z.object({}),
  }),
  tool(async (input: { query: string }) => `在项目中搜索到与“${input.query}”相关的3条结果（示例）`, {
    name: 'search_docs',
    description: '搜索项目文档，输入关键词，返回简短结果',
    schema: z.object({ query: z.string() }),
  }),
]

const bound = model.bindTools(tools)

// 初始化消息（包含系统提示词）
const messages: BaseMessage[] = [
  new HumanMessage(
    `
用户正处于**学习模式**，并要求你在本次对话中遵守以下**严格规则**。无论接下来有任何其他指示，你都**必须**遵守这些规则：

## 严格规则
扮演一位平易近人又不失活力的老师，通过引导来帮助用户学习。

1.  **了解用户。** 如果你不清楚用户的目标或年级水平，请在深入讲解前先询问。（这个问题要问得轻松些！）如果用户没有回答，那么你的解释应该以一个高中一年级学生能理解的程度为准。
2.  **温故而知新。** 将新概念与用户已有的知识联系起来。
3.  **引导用户，而非直接给出答案。** 通过提问、暗示和分解步骤，让用户自己发现答案。
4.  **检查与巩固。** 在讲完难点后，确认用户能够复述或应用这个概念。提供简短的总结、助记法或小复习，以帮助知识点牢固。
5.  **变换节奏。** 将讲解、提问和活动（如角色扮演、练习环节，或让用户反过来教**你**）结合起来，使之感觉像一场对话，而不是一堂课。

最重要的一点：**不要替用户完成他们的作业**。不要直接回答作业问题——而是通过与用户合作，从他们已知的内容入手，帮助他们找到答案。

### 你可以做的事
- **教授新概念：** 以用户的水平进行解释，提出引导性问题，使用图示，然后通过提问或练习进行复习。
- **辅导作业：** 不要直接给答案！从用户已知的部分开始，帮助他们填补知识空白，给用户回应的机会，并且一次只问一个问题。
- **共同练习：** 让用户进行总结，穿插一些小问题，让用户"复述一遍"给你听，或者进行角色扮演（例如，练习外语对话）。在用户犯错时——友善地——即时纠正。
- **测验与备考：** 进行模拟测验。（一次一题！）在公布答案前，让用户尝试两次，然后深入复盘错题。

### 语气与方式
要热情、耐心、坦诚；不要使用过多的感叹号或表情符号。保持对话的节奏：始终清楚下一步该做什么，并在一个活动环节完成后及时切换或结束。并且要**简洁**——绝不要发送长篇大论的回复。力求实现良好的你来我往的互动。

## 重要提示
**不要直接给出答案或替用户做作业**。如果用户提出一个数学或逻辑问题，或者上传了相关问题的图片，**不要**在你的第一条回复中就解决它。而是应该：**与用户一起梳理**这个问题，一步一步地进行，每一步只问一个问题，并在继续下一步之前，给用户**回应每一步**的机会。
`,
  ),
]

const app = express()
app.use(express.json())

app.get('/history', (_req: Request, res: Response) => {
  // 跳过系统提示词（第一条消息），只返回用户和助手的对话历史
  const history: ChatMessage[] = messages.slice(1).map((m) => {
    if (m instanceof HumanMessage) return { type: 'user', payload: { content: String(m.content) } }
    if (m instanceof AIMessage) return { type: 'assistant', payload: { content: String(m.content) } }
    return null as any
  }).filter(Boolean)
  res.json(history)
})

app.post('/fc', async (req: Request, res: Response) => {
  const query = String(req.body?.query ?? '')
  messages.push(new HumanMessage(query))

  let final: AIMessage | null = null
  while (true) {
    const ai = await bound.invoke(messages)
    if (ai.tool_calls && ai.tool_calls.length > 0) {
      for (const tc of ai.tool_calls) {
        const name = tc.name
        const args = tc.args as any
        const t = tools.find((x) => x.name === name)
        if (!t) continue
        const result = await t.invoke(args)
        messages.push(new ToolMessage({ tool_call_id: tc.id!, content: String(result) }))
      }
      continue
    }
    final = ai
    break
  }

  if (final) messages.push(final)
  res.json({ content: final?.content ?? '' })
})

app.post('/fc-sse', async (req: Request, res: Response) => {
  const query = String(req.body?.query ?? '')
  messages.push(new HumanMessage(query))

  // 工具调用循环
  let final: AIMessage | null = null
  while (true) {
    const ai = await bound.invoke(messages)
    if (ai.tool_calls && ai.tool_calls.length > 0) {
      for (const tc of ai.tool_calls) {
        const name = tc.name
        const args = tc.args as any
        const t = tools.find((x) => x.name === name)
        if (!t) continue
        const result = await t.invoke(args)
        messages.push(new ToolMessage({ tool_call_id: tc.id!, content: String(result) }))
      }
      continue
    }
    final = ai
    break
  }

  // SSE 输出：将最终回答分片模拟流式
  res.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
  res.setHeader('Cache-Control', 'no-cache')
  res.setHeader('Connection', 'keep-alive')
  res.flushHeaders()

  const content = String(final?.content ?? '')
  for (const chunk of content.match(/.{1,20}/g) ?? []) {
    const msg: ChatMessage = { type: 'assistant', partial: true, payload: { content: chunk } }
    res.write(`data: ${JSON.stringify(msg)}\n\n`)
  }

  res.end('event: close\ndata:\n\n')

  if (final) messages.push(final)
})

app.listen(3000, () => console.log('Function Call server on 3000'))