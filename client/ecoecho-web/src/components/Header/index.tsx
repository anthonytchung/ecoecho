import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { Switch } from "@/components/ui/switch";

interface HeaderProps {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const Header: React.FC<HeaderProps> = ({ isDarkMode, toggleDarkMode }) => {
  return (
    <header className="p-4 flex justify-between items-center">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-blue-500 text-transparent bg-clip-text">
          EcoEcho
        </h1>
        <div className="flex items-center space-x-2">
          <Sun size={20} />
          <Switch
            checked={isDarkMode}
            onCheckedChange={toggleDarkMode}
            className="w-12 h-6 border-2 "
            id="darkModeSwitch"
          />
          <Moon size={20} />
        </div>
      </header>
  );
};

export default Header;