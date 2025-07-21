import React from 'react';
import { Snackbar, Alert } from '@mui/material';

export default function GlobalErrorSnackbar({ error, onClose }) {
  return (
    <Snackbar open={!!error} autoHideDuration={8000} onClose={onClose} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
      <Alert onClose={onClose} severity="error" sx={{ width: '100%' }}>
        {error?.error || error?.message || 'Сталася помилка.'}
        {error?.details && Array.isArray(error.details) && (
          <ul style={{ margin: 0, paddingLeft: 20 }}>
            {error.details.map((d, idx) => (
              <li key={idx}>
                {d.product_id ? `Товар ID ${d.product_id}: ` : ''}
                {d.required !== undefined ? `потрібно ${d.required}, ` : ''}
                {d.available !== undefined ? `доступно ${d.available}, ` : ''}
                {d.shortage !== undefined ? `не вистачає ${d.shortage}` : ''}
              </li>
            ))}
          </ul>
        )}
      </Alert>
    </Snackbar>
  );
} 