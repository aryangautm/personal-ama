import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../types';
import { TypingIndicator } from './TypingIndicator';

interface ChatLogProps {
    messages: Message[];
    streamingMessage: string;
    isLoading: boolean;
}

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
    // User message: right-aligned, white, ends with '<'
    if (message.sender === 'user') {
        return (
            <div className="flex justify-end">
                <p className="text-white font-light max-w-[80%] text-right break-words">
                    {message.text}<span className="select-none"> &lt;</span>
                </p>
            </div>
        );
    }

    // Bot message: left-aligned, yellow, starts with '>', renders markdown
    return (
        <div className="flex justify-start">
            <div className="text-[#D6A549] font-light max-w-[80%] break-words markdown-content">
                <span className="select-none">&gt; </span>
                <ReactMarkdown
                    components={{
                        p: ({ children }) => <span>{children}</span>,
                        code: ({ children, className }) => {
                            const isInline = !className;
                            return isInline ? (
                                <code className="bg-[#1a1a1a] px-1 py-0.5 rounded text-[#D6A549] font-mono text-sm">
                                    {children}
                                </code>
                            ) : (
                                <code className="block bg-[#1a1a1a] p-2 rounded my-2 text-[#D6A549] font-mono text-sm overflow-x-auto">
                                    {children}
                                </code>
                            );
                        },
                        pre: ({ children }) => <div className="my-2">{children}</div>,
                        a: ({ children, href }) => (
                            <a href={href} target="_blank" rel="noopener noreferrer" className="underline hover:text-[#E5B955]">
                                {children}
                            </a>
                        ),
                        ul: ({ children }) => <ul className="list-disc ml-4 my-1">{children}</ul>,
                        ol: ({ children }) => <ol className="list-decimal ml-4 my-1">{children}</ol>,
                        li: ({ children }) => <li className="my-0.5">{children}</li>,
                        strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                        em: ({ children }) => <em className="italic">{children}</em>,
                        h1: ({ children }) => <h1 className="text-xl font-bold my-2">{children}</h1>,
                        h2: ({ children }) => <h2 className="text-lg font-bold my-2">{children}</h2>,
                        h3: ({ children }) => <h3 className="text-base font-bold my-1">{children}</h3>,
                        blockquote: ({ children }) => (
                            <blockquote className="border-l-2 border-[#D6A549] pl-2 my-1 italic">
                                {children}
                            </blockquote>
                        ),
                    }}
                >
                    {message.text}
                </ReactMarkdown>
            </div>
        </div>
    );
};

export const ChatLog: React.FC<ChatLogProps> = ({ messages, streamingMessage, isLoading }) => {
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, streamingMessage]);

    // Keep scrolled to bottom on viewport/container size changes (e.g., mobile keyboard open)
    useEffect(() => {
        const scrollToBottom = () => {
            const el = scrollRef.current;
            if (!el) return;
            // Use rAF to ensure layout has settled after resize
            requestAnimationFrame(() => {
                el.scrollTop = el.scrollHeight;
            });
        };

        // Window resize and orientation changes
        window.addEventListener('resize', scrollToBottom);
        window.addEventListener('orientationchange', scrollToBottom as any);

        // VisualViewport changes (mobile keyboards)
        const vv = (window as any).visualViewport as VisualViewport | undefined;
        if (vv) {
            vv.addEventListener('resize', scrollToBottom);
            vv.addEventListener('scroll', scrollToBottom);
        }

        // Observe the scroll container size changes
        let resizeObserver: ResizeObserver | null = null;
        if (scrollRef.current && typeof ResizeObserver !== 'undefined') {
            resizeObserver = new ResizeObserver(() => scrollToBottom());
            resizeObserver.observe(scrollRef.current);
        }

        // Initial adjustment
        scrollToBottom();

        return () => {
            window.removeEventListener('resize', scrollToBottom);
            window.removeEventListener('orientationchange', scrollToBottom as any);
            if (vv) {
                vv.removeEventListener('resize', scrollToBottom);
                vv.removeEventListener('scroll', scrollToBottom);
            }
            if (resizeObserver) resizeObserver.disconnect();
        };
    }, []);

    return (
        <div ref={scrollRef} className="h-full overflow-y-auto py-6 space-y-4 pr-2">
            {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
            ))}

            {/* Typing indicator is left-aligned as it represents the bot typing */}
            {isLoading && !streamingMessage && (
                <div className="flex justify-start">
                    <TypingIndicator />
                </div>
            )}

            {/* Streaming message is a bot message */}
            {streamingMessage && (
                <div className="flex justify-start">
                    <p className="text-[#D6A549] font-medium max-w-[50%] break-words">
                        <span className="select-none">&gt; </span>{streamingMessage}
                    </p>
                </div>
            )}
        </div>
    );
};