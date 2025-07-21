import axios from 'axios';

const API_URL = '/api/goods_issues/';

export async function getGoodsIssues() {
  const res = await axios.get(API_URL);
  return res.data;
}

export async function createGoodsIssue(issue) {
  const res = await axios.post(API_URL, issue);
  return res.data;
}

export async function getGoodsIssue(id) {
  const res = await axios.get(`${API_URL}${id}`);
  return res.data;
}

export async function updateGoodsIssue(id, issue) {
  const res = await axios.put(`${API_URL}${id}`, issue);
  return res.data;
}

export async function deleteGoodsIssue(id) {
  const res = await axios.delete(`${API_URL}${id}`);
  return res.data;
} 