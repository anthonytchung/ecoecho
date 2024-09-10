// src/hooks/useDarkMode.tsx
import { useState, useEffect } from 'react';

export const useDarkMode = () => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    // Check if there's a saved preference in localStorage
    const savedMode = localStorage.getItem('darkMode');
    // Check if the user's system prefers dark mode
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Return true if there's a saved preference for dark mode,
    // or if the system prefers dark mode and there's no saved preference
    return savedMode ? JSON.parse(savedMode) : prefersDark;
  });

  useEffect(() => {
    // Save the current mode to localStorage whenever it changes
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
    
    // Apply the appropriate class to the body element
    if (isDarkMode) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  return { isDarkMode, toggleDarkMode };
};