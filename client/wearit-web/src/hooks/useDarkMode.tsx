// src/hooks/useDarkMode.tsx
"use client"
import { useState, useEffect } from 'react';

export const useDarkMode = () => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      // Check if there's a saved preference in localStorage
      const savedMode = localStorage.getItem('darkMode');
      // Check if the user's system prefers dark mode
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      
      if (savedMode !== null) {
        try {
          // If savedMode is valid JSON, parse it
          return JSON.parse(savedMode);
        } catch (e) {
          console.error('Error parsing dark mode setting from localStorage', e);
        }
      }
      // Return system preference if no valid saved setting exists
      return prefersDark;
    }
    // Default to false if not in a browser environment
    return false;
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Save the current mode to localStorage whenever it changes
      localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
      
      // Apply or remove 'dark' class based on isDarkMode
      const classList = document.body.classList;
      const alreadyApplied = classList.contains('dark');
      if (isDarkMode && !alreadyApplied) {
        classList.add('dark');
      } else if (!isDarkMode && alreadyApplied) {
        classList.remove('dark');
      }
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  return { isDarkMode, toggleDarkMode };
};