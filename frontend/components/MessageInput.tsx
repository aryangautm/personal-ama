import React, { useState, useRef, useEffect } from 'react';

interface MessageInputProps {
    onSendMessage: (text: string) => void;
    disabled: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, disabled }) => {
    const [inputValue, setInputValue] = useState('');
    const [isFocused, setIsFocused] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);
    const scrollRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            // Scroll to the end to keep the caret visible
            scrollRef.current.scrollLeft = scrollRef.current.scrollWidth;
        }
    }, [inputValue]);

    // Handle focus to ensure input is visible when keyboard opens
    const handleFocus = () => {
        setIsFocused(true);

        // Scroll input into view on mobile when keyboard appears
        setTimeout(() => {
            if (containerRef.current) {
                containerRef.current.scrollIntoView({
                    behavior: 'smooth',
                    block: 'nearest'
                });
            }
        }, 300); // Delay to allow keyboard animation
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (inputValue.trim() && !disabled) {
            onSendMessage(inputValue);
            setInputValue('');
        }
    };

    const handleContainerClick = () => {
        inputRef.current?.focus();
    };

    return (
        <div ref={containerRef} className="flex-shrink-0 py-2">
            <form onSubmit={handleSubmit}>
                <div
                    className="relative bg-transparent border-[1px] border-[#383838] rounded-[9px] p-3 flex items-center cursor-text"
                    onClick={handleContainerClick}
                >
                    <span className="text-white select-none">&gt; </span>
                    <div ref={scrollRef} className="relative flex items-center flex-grow ml-2 overflow-x-auto no-scrollbar">
                        <span className="text-white whitespace-pre">{inputValue}</span>
                        {/* Blinking Caret */}
                        {isFocused && !disabled && <span className="w-2.5 h-5 bg-white inline-block blinking-caret"></span>}
                    </div>

                    {/* Hidden actual input */}
                    <input
                        ref={inputRef}
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onFocus={handleFocus}
                        onBlur={() => setIsFocused(false)}
                        disabled={disabled}
                        className="absolute top-0 left-0 w-full h-full bg-transparent border-none outline-none text-transparent opacity-0"
                        autoComplete="off"
                        autoCapitalize="off"
                        spellCheck="false"
                    />
                </div>
            </form>
        </div>
    );
};