
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

add_user_message(messages,"茶喝咖啡那个好呢")


add_assistant_message(messages,"茶真的比咖啡好，因为")
console.log(messages)   
const stream = await model.messages.create({
    model: MODEL,
    max_tokens: 1024,
    messages,
    stream: true
})
let fullResponse = '';

for await (const chunk of stream) {
        // console.log(chunk);

        if (chunk.type === 'content_block_delta' && chunk.delta?.type === 'text_delta') {
            const text = chunk.delta.text;
            process.stdout.write(text);
            fullResponse += text;
        }
}


console.log("\n=================================");
console.log('\n完整响应内容:', fullResponse);