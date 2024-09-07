"use client"
import React, { useState } from 'react';
import Head from 'next/head';
import ImageUpload from '@/components/ImageUpload';
import ResultsDisplay from '@/components/ResultsDisplay';
import Footer from '@/components/Footer';
import { ResultItem } from '../../types';

export default function WearItApp() {
  const [results, setResults] = useState<ResultItem[] | null>(null);

  const handleUploadSuccess = (uploadedResults: ResultItem[]) => {
    setResults(uploadedResults);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-400 to-gray-900">
      <Head>
        <title>WearIt</title>
        <meta name="description" content="Upload an image to find alternatives to your favorite fashion items" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex-grow container mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl sm:text-7xl font-extrabold text-white text-center mb-4 tracking-tight">
            Wear<span className="text-green-400">It</span>
          </h1>
          <p className="text-xl sm:text-2xl text-gray-200 text-center mb-12 font-light">
            Discover alternatives to your favorite fashion items.
          </p>

          <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-md rounded-3xl shadow-2xl p-8 mb-12">
            <ImageUpload onUploadSuccess={handleUploadSuccess} />
          </div>

          {results && <ResultsDisplay results={results} />}
        </div>
      </main>
      <Footer />
    </div>
  );
}