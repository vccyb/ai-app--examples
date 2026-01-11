import {Anthropic} from "@anthropic-ai/sdk";
import type {MessageParam} from "@anthropic-ai/sdk/resources/messages";

const API_KEY = process.env.API_KEY;
const MODEL = 'glm-4.7'
const BASE_URL = 'https://open.bigmodel.cn/api/anthropic'

const model = new Anthropic({
    apiKey: API_KEY,
    baseURL: BASE_URL,
})

const messages: MessageParam[] = []

function add_user_message(messages: MessageParam[], content: string) {
    messages.push({
        role: 'user',
        content,
    })
}

function add_assistant_message(messages: MessageParam[], content: string) {
    messages.push({
        role: 'assistant',
        content,
    })
}

add_user_message(messages,"从一数到五")

async function chat(
    messages: MessageParam[],
    options: {
        sys_prompt?: string,
        temperature?: number,
        stop_sequences?: string[]
    } = {}
) {
    const { sys_prompt = "", temperature = 1.0, stop_sequences = [] } = options;

    const params: any = {
        model: MODEL,
        max_tokens: 1024,
        messages,
        temperature,
    };

    if (sys_prompt) {
        params.system = sys_prompt;
    }

    if (stop_sequences.length > 0) {
        params.stop_sequences = stop_sequences;
    }

    const msg = await model.messages.create(params)
    return msg.content[0].text
}

const stop_sequences = ['三']
const msg = await chat(messages, { stop_sequences }) // 只传递stop_sequences参数
console.log(msg)