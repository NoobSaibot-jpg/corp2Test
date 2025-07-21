import axios from 'axios';

const API_URL = '/api/products/';

export async function getProducts() {
  const res = await axios.get(API_URL);
  return res.data;
}

export async function createProduct(product) {
  const res = await axios.post(API_URL, product);
  return res.data;
} 