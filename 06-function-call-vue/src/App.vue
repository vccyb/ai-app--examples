<template>
  <main class="min-h-screen bg-white flex flex-col items-center px-4 py-8 sm:px-6">
    <h1 class="text-2xl font-semibold text-gray-800 mb-6">
      {{ isWelcome ? 'Function Call 助手' : 'Function Call Demo' }}
    </h1>

    <section ref="chatContainer" class="w-full max-w-2xl flex-1 flex flex-col gap-4 pb-24 sm:pb-32 overflow-y-auto max-h-[70vh]">
      <div v-for="(message, idx) in messages" :key="idx + message.type + (message.payload?.content?.length || 0)" class="flex items-center gap-3" :class="message.type === 'user' ? 'justify-end' : 'justify-start'">
        <template v-if="message.type === 'user'">
          <div class="max-w-[85%] rounded-xl px-3 py-2 text-sm leading-relaxed break-words bg-blue-500 text-white">
            {{ message.payload.content }}
          </div>
          <span class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
            <svg viewBox="0 0 24 24" class="w-4 h-4 block" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 21v-2a4 4 0 0 0-8 0v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </span>
        </template>
        <template v-else>
          <span class="w-8 h-8 rounded-full bg-gray-200 text-gray-700 flex items-center justify-center">
            <svg viewBox="0 0 24 24" class="w-4 h-4 block" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="8" width="16" height="10" rx="3"/>
              <circle cx="9" cy="13" r="1.5"/>
              <circle cx="15" cy="13" r="1.5"/>
              <path d="M12 8V5"/>
              <circle cx="12" cy="4" r="1"/>
            </svg>
          </span>
          <div class="max-w-[85%] rounded-xl px-3 py-2 text-sm leading-relaxed break-words bg-gray-100 text-gray-800">
            {{ message.payload.content }}
          </div>
        </template>
      </div>
    </section>

    <section class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-2xl px-4 pb-6">
      <div class="relative flex items-center gap-2 rounded-xl bg-white shadow p-2">
        <input ref="inputRef" v-model="input" class="h-12 w-full rounded-lg bg-gray-50 px-4 pr-14 outline-none placeholder:text-gray-400" placeholder="例如：查询今天时间、搜索文档" @keyup.enter="send" />
        <button class="absolute right-2 top-1/2 -translate-y-1/2 grid place-items-center w-10 h-10 rounded-full bg-white shadow hover:bg-gray-50" @click="isReplying ? stop() : send()" :disabled="isConnecting && !isReplying">
          <template v-if="isConnecting && !isReplying">
            <svg viewBox="0 0 24 24" class="w-5 h-5 block text-gray-700 animate-spin" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10" class="opacity-25"/><path d="M12 2a10 10 0 0 1 10 10" class="opacity-75"/></svg>
          </template>
          <template v-else-if="isReplying">
            <svg viewBox="0 0 24 24" class="w-5 h-5 block text-red-600" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
          </template>
          <template v-else>
            <svg viewBox="0 0 24 24" class="w-5 h-5 block text-blue-600" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5l7 7-7 7"/></svg>
          </template>
        </button>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { ssePost } from './api/sse'

type ChatMessage = { type: 'user' | 'assistant', payload: { content: string }, partial?: boolean }

const messages = ref<ChatMessage[]>([])
const input = ref('')
const isConnecting = ref(false)
const isReplying = ref(false)
const controller = ref<AbortController | null>(null)
const chatContainer = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

const isWelcome = computed(() => messages.value.length === 0)

async function fetchHistory() {
  try {
    const res = await fetch('/history')
    if (!res.ok) throw new Error('failed')
    const data = await res.json()
    messages.value = data as ChatMessage[]
    scrollToBottom()
  } catch (e) {
    // 可按需处理错误
  }
}

function scrollToBottom() {
  nextTick(() => { const el = chatContainer.value; if (el) el.scrollTop = el.scrollHeight })
}

async function send() {
  const text = input.value.trim()
  if (!text || isConnecting.value || isReplying.value) return

  messages.value.push({ type: 'user', payload: { content: text } })
  input.value = ''

  isConnecting.value = true
  isReplying.value = true

  controller.value?.abort()
  controller.value = new AbortController()

  try {
    const stream = await ssePost<ChatMessage>('/fc-sse', { params: { query: text }, signal: controller.value.signal })
    for await (const msg of stream) {
      const message = msg as ChatMessage
      const last = messages.value[messages.value.length - 1]
      if (message.partial && last?.partial) {
        last.payload.content += message.payload.content
      } else {
        messages.value.push(message)
      }
      isConnecting.value = false
      scrollToBottom()
    }
  } catch (e) {
  } finally {
    isConnecting.value = false
    isReplying.value = false
    controller.value = null
  }
}

function stop() {
  controller.value?.abort()
  controller.value = null
  isConnecting.value = false
  isReplying.value = false
}

onMounted(() => {
  fetchHistory()
  nextTick(() => inputRef.value?.focus())
})
</script>