import axios from 'axios';

const API_URL = '/api/goods_receipts/';

export async function getGoodsReceipts() {
  const res = await axios.get(API_URL);
  return res.data;
}

export async function createGoodsReceipt(receipt) {
  const res = await axios.post(API_URL, receipt);
  return res.data;
} 