import {cn} from "@/lib/utils.ts";
import {useEffect, useRef, useState} from "react";
import type {ChatMessage} from "../types";

import {ArrowRightIcon, Loader2Icon, SquareIcon} from 'lucide-react';
import {ssePost} from "@/lib/sse.ts";


function MessageItem(props: { message: ChatMessage }) {
    const message = props.message
    const isUserMessage = message.type === 'user'
    return (
        <div className={
            cn('flex', isUserMessage && 'justify-end')
        }>
            <p className={
                cn(
                    isUserMessage && 'rounded-full bg-neutral-100 px-4 py-1.5'
                )
            }>{
                message.payload.content
            }</p>
        </div>
    )
}

function App() {

    const [messages, setMessages] = useState<ChatMessage[]>([])
    const [isConnecting, setIsConnecting] = useState(false);
    const [isReplying, setIsReplying] = useState(false);
    const [error, setError] = useState('');
    const [input, setInput] = useState('');

    const inputRef = useRef<HTMLInputElement>(null);
    const abortControllerRef = useRef<AbortController | null>(null);


    const isWelcome = messages.length === 0


    useEffect(() => {
        const handleKeyPress = (e: KeyboardEvent) => {
            if (e.key === 'Enter' && document.activeElement === inputRef.current) {
                handleSend()
            }
        }


        window.addEventListener('keydown', handleKeyPress)
        return () => {
            window.removeEventListener('keydown', handleKeyPress)
        }


    }, [input, isConnecting, isReplying])

    useEffect(() => {
        const loadHistory = async () => {
            try {
                const response = await fetch('/api/history')
                const data = await response.json()
                setMessages(data)

                setTimeout(() => {
                    window.scrollTo({
                        top: document.body.scrollHeight,
                        behavior: 'smooth',
                    })
                }, 0)
            } catch (error) {
                console.error('Failed to load history', error)
            }
        }

        loadHistory();
    }, []);


    async function handleSend() {
        if (isConnecting) {
            return;
        }

        // 如果正在回复，再次点击按钮则中断流。
        if (isReplying) {
            abortControllerRef.current?.abort();
            return;
        }

        if (input.trim() === '') {
            inputRef.current?.focus();
            return;
        }

        try {
            setIsConnecting(true);
            setError('');

            abortControllerRef.current = new AbortController();

            const stream = await ssePost<ChatMessage>('/api/sse', {
                signal: abortControllerRef.current.signal,
                params: {
                    query: input.trim(),
                },
            });


            setMessages(prevMessages => [...prevMessages, {
                type: 'user',
                payload: {
                    content: input.trim(),
                }
            }])

            setInput('')
            setIsConnecting(false);
            setIsReplying(true);


            // 处理流式响应
            for await (const message of stream) {
                // 获取最新的消息列表状态
                setMessages(prevMessages => {
                    // 创建新数组避免直接修改原数组
                    const newMessages = [...prevMessages];
                    const lastMessage = newMessages[newMessages.length - 1];

                    // 合并不完全消息（实现打字机效果）
                    if (message.partial && lastMessage && lastMessage.type === 'assistant' && lastMessage.partial) {
                        // 更新最后一条消息的内容
                        lastMessage.payload.content += message.payload.content;
                        return newMessages;
                    } else {
                        // 添加新的助手消息
                        return [...newMessages, message];
                    }
                });

                // 滚动到底部显示最新消息
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth',
                });
            }

        } catch (error) {
            console.error('发送消息失败:', error);
            setError(error instanceof Error ? error.message : '发送消息失败');

        } finally {
            setIsConnecting(false);
            setIsReplying(false);
        }

    }


    return (
        <main

            className={cn(
                'pb-28  max-w-[70%] mx-auto',
                isWelcome && 'flex h-screen flex-col justify-center',
            )}>
            {/*  标题 */}
            <section className="sticky left-0 top-0 z-10 bg-background  mx-auto      ">
                <h1
                    className={cn(
                        'md:w-3xl mx-auto p-4 text-3xl font-medium text-center   mx-auto  ',
                    )}
                >
                    {isWelcome ? '有什么可以帮忙的？' : 'Chatbot UI'}
                </h1>
            </section>


            {/* 聊天消息*/}
            <section className='flex flex-col gap-4 flex-1'>
                {messages.map((message, index) => (
                    <MessageItem key={index} message={message}></MessageItem>
                ))}

                {/* 错误提示 */}
                {error && (
                    <div className="mt-4 rounded bg-red-50 p-4 py-3 text-sm text-red-500">
                        {error}
                    </div>
                )}
            </section>
            {/* 底部输入框 */}
            <section
                className={cn(
                    'bg-background md:w-3xl w-full p-4 pt-0',
                    isWelcome
                        ? 'relative left-0 mx-auto -translate-x-0'
                        : 'fixed bottom-0 left-1/2 -translate-x-1/2',
                )}
            >
                <div
                    className={cn(
                        'relative flex flex-col gap-2 rounded-xl border-2 pb-10',
                        'bg-background focus-within:border-primary',
                    )}
                >
                    <input
                        ref={inputRef}
                        className="h-11 resize-none px-3 outline-none"
                        autoFocus
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={isConnecting || isReplying}
                        placeholder="尽管问..."
                    />
                    <div
                        className={cn(
                            'absolute bottom-2 right-2 flex cursor-pointer justify-end rounded-full bg-black p-1.5 text-white',
                        )}
                        onClick={handleSend}
                    >
                        {/* 正在连接图标 */}
                        {isConnecting && (
                            <Loader2Icon size={16} className="animate-spin"/>
                        )}
                        {/* 中断图标 */}
                        {isReplying && <SquareIcon size={16}/>}
                        {/* 发送图标 */}
                        {!isConnecting && !isReplying && (
                            <ArrowRightIcon size={16} className="-rotate-90"/>
                        )}
                    </div>
                </div>
            </section>
        </main>
    )
}

export default App