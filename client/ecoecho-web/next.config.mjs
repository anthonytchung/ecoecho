/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: ["www.patagonia.com", "cdn.shopify.com"], // Add the hostname here
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.shopify.com',
        port: '',
      },
      {
        protocol: 'https',
        hostname: 'www.patagonia.com',
        port: '',
      }
    ]
  },
};



export default nextConfig;
