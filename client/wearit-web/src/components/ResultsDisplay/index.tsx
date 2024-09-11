import { ResultItem } from "../../../types";
import { useState, useEffect } from "react";
import { ExternalLink, Leaf } from "lucide-react";
import { formatCost } from "@/lib/utils";
import { Button, } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

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
        {results.slice(0, displayCount).map((product) => (
          <div
            key={product.id}
            className="group bg-gray-800 rounded-xl overflow-hidden shadow-lg transition duration-300 ease-in-out transform hover:scale-105 hover:bg-gray-700 focus-within:ring-2 focus-within:ring-green-400"
          >
            <a
              href={product.product_url}
              target="_blank"
              rel="noopener noreferrer">
            <div className="relative aspect-w-16 aspect-h-9">
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity duration-300" />
              {/* <div className="absolute top-2 right-2 bg-green-500 rounded-full p-1.5">
                <Leaf className="w-4 h-4 text-white" />
              </div> */}
            </div>
            <div className="p-4 flex flex-col justify-between h-48">
              <div>
                <h3 className="font-bold text-xl mb-2 text-gray-100 group-hover:text-green-400 transition-colors duration-300 line-clamp-2">
                  {product.title}
                </h3>
                <p className="text-lg font-semibold text-gray-300">
                  {formatCost(product.price)}
                </p>
              </div>
              <div className="mt-2">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm text-gray-400">Similarity</span>
                  <span className="text-sm font-medium text-green-400">
                    {(product.similarity * 100).toFixed(0)}%
                  </span>
                </div>
                <Progress value={Number((product.similarity * 100).toFixed(0))} max={100} className="h-2 bg-white w-[60%]" />
              </div>
            </div>
            <p
              className="block p-3 text-center bg-green-600 hover:bg-green-700 transition-colors duration-300 text-white font-semibold"
            >
              View Product <ExternalLink className="inline-block w-4 h-4 ml-2" />
            </p>
            </a>
          </div>
        ))}
        
      </div>
      <div className="flex justify-center mt-8 space-x-4">
        <Button
          onClick={showLess}
          disabled={displayCount <= 3}
          className="px-6 py-2 font-semibold text-gray-200 bg-gray-700 rounded-lg transition duration-300 ease-in-out hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
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
