import Image from "next/image";
import React from "react";
import { formatCost } from "@/lib/utils";
import { ResultItem } from "@/lib/types";
import { ExternalLink, Leaf } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
// import styles from "./ProductCard.module.css";

const ProductCard = ({ product }: { product: ResultItem }) => {
  return (
    <div
      key={product.id}
      className="group bg-gray-800 rounded-xl overflow-hidden shadow-lg transition duration-300 ease-in-out transform hover:scale-105 hover:bg-gray-700 focus-within:ring-2 focus-within:ring-green-400 {styles.productCard}"
    >
      <a href={product.product_url} target="_blank" rel="noopener noreferrer">
        <div className="relative aspect-w-16 aspect-h-9">
          {/* <img
            src={product.image_url}
            alt={product.title}
            className="w-full h-full object-cover"
          /> */}
          <Image
            src={product.image_url}
            alt={product.title}
            width={500}
            height={500}
            className="w-full h-full object-cover"
          />

          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity duration-300" />
          {/* <div className="absolute top-2 right-2 bg-green-500 rounded-full p-1.5">
                <Leaf className="w-4 h-4 text-white" />
              </div> */}
        </div>
        <div className="p-4 flex flex-col justify-between h-52">
          <div>
            <h3 className="font-bold text-xl mb-2 text-gray-100 group-hover:text-green-400 transition-colors duration-300 line-clamp-2 h-14 overflow-hidden">
              {product.title}
            </h3>
            <p className="text-lg font-semibold text-gray-300">
              {formatCost(product.price)}
            </p>
          </div>
          <div className="">
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm text-gray-400">Similarity</span>
              <span className="text-sm font-medium text-green-400">
                {(product.similarity * 100).toFixed(0)}%
              </span>
            </div>
            <Progress
              value={Number((product.similarity * 100).toFixed(0))}
              className="w-full h-2 bg-gray-700"
            />
          </div>
          <div className="flex flex-row justify-between">
            <p className="text-sm text-gray-400 line-clamp-1">
              Brand
              <span className=" font-semibold text-gray-100 ml-1">
                {product.brand}
              </span>
            </p>
            <p className="text-sm text-gray-400 line-clamp-1">
              Category
              <span className="font-semibold text-gray-100 ml-1">
                {product.category}
              </span>
            </p>
          </div>
        </div>
        <p className="block p-3 text-center bg-green-600 hover:bg-green-700 transition-colors duration-300 text-white font-semibold">
          View Product <ExternalLink className="inline-block w-4 h-4 ml-2" />
        </p>
      </a>
    </div>
  );
};

export default ProductCard;
