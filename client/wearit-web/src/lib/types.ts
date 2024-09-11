export 

declare type ResultItem = {
    id: number;
    brand: string;
    title: string;
    price: number;
    original_price: string;
    image_url: string;
    product_url: string;
    category: string;
    type: string;
    available_sizes: string[];
    similarity: number;
  }