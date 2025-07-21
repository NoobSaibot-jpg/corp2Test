const API_BASE_URL = 'http://localhost:5000/api';

export const getInvoices = async () => {
  const response = await fetch(`${API_BASE_URL}/invoices`);
  if (!response.ok) {
    throw new Error('Failed to fetch invoices');
  }
  return response.json();
};

export const getInvoice = async (id) => {
  const response = await fetch(`${API_BASE_URL}/invoices/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch invoice');
  }
  return response.json();
};

export const createInvoice = async (invoiceData) => {
  const response = await fetch(`${API_BASE_URL}/invoices`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(invoiceData),
  });
  if (!response.ok) {
    throw new Error('Failed to create invoice');
  }
  return response.json();
};

export const updateInvoice = async (id, invoiceData) => {
  const response = await fetch(`${API_BASE_URL}/invoices/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(invoiceData),
  });
  if (!response.ok) {
    throw new Error('Failed to update invoice');
  }
  return response.json();
};

export const deleteInvoice = async (id) => {
  const response = await fetch(`${API_BASE_URL}/invoices/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete invoice');
  }
  return response.json();
}; 