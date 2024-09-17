"use client"
import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import Header from '@/components/Header';
import ImageUpload from '@/components/ImageUpload';
import ResultsDisplay from '@/components/ResultsDisplay';
import Footer from '@/components/Footer';
import { ResultItem } from '@/lib/types';
import { Upload, ArrowRight, Sun, Moon } from 'lucide-react';
import { Switch } from "@/components/ui/switch";
import { useDarkMode } from '@/hooks/useDarkMode';

export default function WearItApp() {
  const [results, setResults] = useState<ResultItem[] | null>(null);
  const { isDarkMode, toggleDarkMode } = useDarkMode();

  const handleUploadSuccess = (uploadedResults: ResultItem[]) => {
    setResults(uploadedResults);
  };

  useEffect(() => {
    // Reset display count whenever the imageInputId changes
    // setResults(null)
  }, [results]);

  return (
    <div className={`min-h-screen flex flex-col ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
      
      <Header isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
      <main className="flex-grow flex flex-col items-center justify-center p-4">
        <h1 className="text-4xl font-bold mb-6 text-center">
          Discover Eco-Friendly Fashion Alternatives
        </h1>
        {/* <p className="text-xl mb-8 text-center max-w-2xl">
          Upload an image of your favorite fashion item, and we&apos;ll find similar, environmentally conscious options for you.
        </p> */}
        <ImageUpload onUploadSuccess={handleUploadSuccess} isDarkMode={isDarkMode}/>
        {results && <ResultsDisplay results={results} />}
      </main>
      {/* <Footer /> */}
    </div>
  );
}
