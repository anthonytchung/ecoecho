import { ResultItem } from "@/lib/types";
import { useState, useEffect } from "react";
import { ExternalLink, Leaf } from "lucide-react";
import { formatCost } from "@/lib/utils";
import Image from 'next/image';
import { Button, } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import ProductCard from "@/components/ResultsDisplay/ProductCard";

interface ResultsDisplayProps {
  results: ResultItem[];
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const [displayCount, setDisplayCount] = useState(3);

  useEffect(() => {
    // Reset display count whenever the imageInputId changes
    setDisplayCount(3);
  }, [results]);

  const loadMore = () => {setDisplayCount(displayCount + 3);};
  const showLess = () => {if (displayCount > 3) {setDisplayCount(displayCount - 3);}};

  return (
    <div className="mt-12 w-full max-w-6xl mx-auto px-4">
      <h2 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
        Eco-Friendly Alternatives
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {results.slice(displayCount-3, displayCount).map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
        
      </div>
      <div className="flex justify-center mt-8 space-x-4">
        <Button
          onClick={showLess}
          disabled={displayCount <= 3}
          className="px-6 py-2 font-semibold text-white bg-green-600 rounded-lg transition duration-300 ease-in-out hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Show Less
        </Button>
        <Button
          onClick={loadMore}
          disabled={displayCount >= results.length}
          className="px-6 py-2 font-semibold text-white bg-green-600 rounded-lg transition duration-300 ease-in-out hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Load More
        </Button>
      </div>
    </div>
  );
}
