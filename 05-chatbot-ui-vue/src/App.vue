<template>

  <main class="min-h-screen bg-background flex flex-col items-center gap-10 px-6 py-10">

    <section class="flex flex-col items-center justify-center">
      <h1 class=" text-3xl font-bold text-primary"> {{ isWelcome ? 'Welcome' : 'Chatbot UI' }}</h1>
    </section>

    <section class="flex flex-col gap-5 bg-background/60 backdrop-blur-sm rounded-2xl border border-neutral-200 shadow-sm lg:max-w-4xl w-full p-6 chat-scroll max-h-[70vh] overflow-y-auto">
      <div class="flex items-center gap-3" :class="message.type === 'user' ? 'justify-end' : 'justify-start'"
           v-for="message in messages" :key="message.type + message.payload.content">
        <template v-if="message.type === 'user'">
          <p class="max-w-[80%] rounded-2xl bg-primary/10 text-primary px-4 py-2 leading-relaxed break-words">
            {{ message.payload.content }}
          </p>
          <span class="w-10 h-10 rounded-full bg-primary/10 text-primary grid place-items-center ring-2 ring-primary/20 shadow-sm">
            <iconify-icon icon="lucide:user" class="w-5 h-5"></iconify-icon>
          </span>
        </template>
        <template v-else>
          <span class="w-10 h-10 rounded-full bg-neutral-200 text-neutral-700 grid place-items-center ring-2 ring-neutral-300 shadow-sm">
            <iconify-icon icon="lucide:bot" class="w-5 h-5"></iconify-icon>
          </span>
          <p class="max-w-[80%] rounded-2xl bg-neutral-100 text-neutral-800 px-4 py-2 leading-relaxed break-words">
            {{ message.payload.content }}
          </p>
        </template>
      </div>
    </section>


    <section
        :class="[
      'bg-background md:max-w-3xl w-full p-4 mb-12 pt-0',
      isWelcome
        ? 'relative left-0 mx-auto -translate-x-0'
        : 'fixed bottom-0 left-1/2 -translate-x-1/2'
    ]"
    >
      <div
          :class="[
        'relative flex items-center gap-2 rounded-2xl border border-neutral-200 shadow-sm p-2',
        'bg-background focus-within:border-primary'
      ]"
      >
        <input
            ref="inputRef"
            class="h-14 w-full rounded-xl bg-neutral-50 px-4 pr-20 outline-none placeholder:text-neutral-400 focus:ring-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed"
            autofocus
            v-model="input"
            :disabled="isConnecting || isReplying"
            placeholder="尽管问..."
        />
        <div
            :class="[
          'absolute right-3 top-1/2 -translate-y-1/2 grid place-items-center w-12 h-12 cursor-pointer rounded-full transition-colors shadow bg-white hover:bg-neutral-50 ring-4 ring-neutral-200 border border-neutral-200'
        ]"
            @click="handleSend"
        >
          <iconify-icon v-if="isConnecting" icon="lucide:loader-2" class="w-6 h-6 text-neutral-700 animate-spin block leading-none"></iconify-icon>
          <iconify-icon v-else-if="isReplying" icon="lucide:stop-circle" class="w-6 h-6 text-red-600 block leading-none"></iconify-icon>
          <iconify-icon v-else icon="lucide:send" class="text-xl   w-6 h-6 text-primary block leading-none translate-y-[1px]"></iconify-icon>
        </div>
      </div>
    </section>

  </main>

</template>

<script setup lang="ts">


import type {ChatMessage} from "../types";
import {computed, ref} from "vue";


const messages = ref<Array<ChatMessage>>([
  {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI',
    },
  },
  {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI ，有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗 ',
    },
  },
  {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI ，有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗 ',
    },
  },
    {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI ，有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗 ',
    },
  },  {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI ，有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗 ',
    },
  },  {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI ，有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗 ',
    },
  },  {
    type: 'user',
    payload: {
      content: '你好',
    },
  },
  {
    type: 'assistant',
    payload: {
      content: '你好，我是 Chatbot UI ，有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什有什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗什么我可以帮助你的吗 ',
    },
  },

])

const isWelcome = computed(() => {
  return messages.value.length === 0
})


</script>

<style scoped>
.chat-scroll::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
.chat-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.12);
  border-radius: 9999px;
}
.chat-scroll {
  scrollbar-color: rgba(0, 0, 0, 0.12) transparent;
  scrollbar-width: thin;
}
</style>