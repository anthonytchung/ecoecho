import { ResultItem } from '../../../types'
import {useState, useEffect } from 'react'
import { ExternalLink } from 'lucide-react'

interface ResultsDisplayProps {
  results: ResultItem[];
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const [displayCount, setDisplayCount] = useState(3)

  useEffect(() => {
    // Reset display count whenever the imageInputId changes
    setDisplayCount(3);
  }, results);

  const loadMore = () =>{
    setDisplayCount(displayCount + 3)
  }


  return (
    <div className="mt-12 w-full max-w-4xl">
      <h2 className="text-3xl font-bold mb-8 text-white text-center">Alternatives</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {results.slice(displayCount-3, displayCount).map((product) => (
          <a 
            href={product.product_url}
            key={product.id}
            className="group bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-xl overflow-hidden shadow-lg transition duration-300 ease-in-out transform hover:scale-105 hover:bg-opacity-20 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-opacity-50"
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className="relative aspect-w-4 aspect-h-3">
              <img 
                src={product.image_url} 
                alt={product.title} 
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
            </div>
            <div className="p-4 flex justify-between flex-col h-32">
              <h3 className="font-bold text-xl mb-2 text-white group-hover:text-yellow-400 transition-colors duration-300 line-clamp-2">{product.title}</h3>
              <p className="text-lg font-semibold items-center text-red-400  flex justify-between">${product.price} 
                {/* <span className="linze-through text-gray-200">${product.original_price} </span> */}
                <span className="text-green-200 text-sm">{(product.similarity*100).toFixed(2)}% Similar</span>
              </p>
            </div>
            <div className="absolute top-2 right-2 bg-white bg-opacity-75 rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <ExternalLink className="w-4 h-4 text-gray-800" />
            </div>
          </a>
        ))}
        
      </div>
      <button 
          type="submit" 
          onClick={loadMore}
          className="w-6/12 mx-auto mt-6 px-4 py-3 font-bold text-white bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg hover:from-purple-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-opacity-50 transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed justify-center flex items-center"
        >
          Load More
        </button> 
    </div>
  )
}