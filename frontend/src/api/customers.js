import axios from 'axios';

const API_URL = '/api/customers/';

export async function getCustomers() {
  const res = await axios.get(API_URL);
  return res.data;
}

export async function createCustomer(customer) {
  const res = await axios.post(API_URL, customer);
  return res.data;
}

export async function updateCustomer(id, customer) {
  const res = await axios.put(`${API_URL}${id}`, customer);
  return res.data;
} 