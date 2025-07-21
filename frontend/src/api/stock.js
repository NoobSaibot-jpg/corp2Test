import axios from 'axios';

const API_URL = '/api/stock/';

export async function getStock() {
  const res = await axios.get(API_URL);
  return res.data;
}

export async function getProductStock(productId) {
  const res = await axios.get(`${API_URL}${productId}`);
  return res.data;
}

export async function getAllBatches() {
  const res = await axios.get(`${API_URL}batches`);
  return res.data;
} 