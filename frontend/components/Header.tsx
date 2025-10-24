import React from 'react';
import { Persona } from '../types';

interface HeaderProps {
    persona: Persona | null;
    isOnline: boolean;
}

export const Header: React.FC<HeaderProps> = ({ persona, isOnline }) => {
    const displayName = persona?.public_name || "";
    const profileImage = persona?.profile_image_url || "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZTfeZyVr7GyW1ygsIqMmADllxP3iwG1h6gw&s";

    return (
        <header className="w-full">
            <div className="flex items-center space-x-4">
                <img
                    src={profileImage}
                    alt={displayName}
                    className="w-12 h-12 rounded-full border-2 border-slate-200 dark:border-slate-800 object-cover shadow-sm hover:[transform:rotateY(180deg)] [transform-style:preserve-3d]"
                />
                <div>
                    <h1 className="text-lg font-normal font-jetbrains-mono">{displayName}</h1>
                    <div className="flex items-center space-x-1.5">
                        <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-[#1CAB17]' : 'bg-red-500'}`}></span>
                        <p className="text-xs text-gray-400">{isOnline ? 'online' : 'offline'}</p>
                    </div>
                </div>
            </div>
            <div className="mt-4 h-[1px] w-full bg-[#383838]"></div>
        </header>
    );
};