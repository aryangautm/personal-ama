import React from 'react';

export const TypingIndicator: React.FC = () => {
    return (
        <div className="flex items-center space-x-1.5">
            <span 
                className="w-2 h-2 bg-gray-500 rounded-full animate-[wave_1.5s_ease-in-out_infinite]"
                style={{ animationDelay: '0s' }}
            ></span>
            <span 
                className="w-2 h-2 bg-gray-500 rounded-full animate-[wave_1.5s_ease-in-out_infinite]"
                style={{ animationDelay: '0.3s' }}
            ></span>
            <span 
                className="w-2 h-2 bg-gray-500 rounded-full animate-[wave_1.5s_ease-in-out_infinite]"
                style={{ animationDelay: '0.6s' }}
            ></span>
        </div>
    );
};