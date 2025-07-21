import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { getStock } from '../api/stock';
import { Box, TextField, Stack } from '@mui/material';

const columns = [
  { field: 'product_name', headerName: 'Товар', width: 200 },
  { field: 'available_quantity', headerName: 'Залишок', width: 120 },
  { field: 'unit', headerName: 'Од. вим.', width: 120 },
];

export default function StockList() {
  const [rows, setRows] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    getStock().then(data => setRows(data.map(item => ({ ...item, id: item.product_id }))));
  }, []);

  const filteredRows = rows.filter(row =>
    row.product_name?.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <Box sx={{ height: 600, width: '100%', mt: 4 }}>
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField
          label="Товар"
          value={filter}
          onChange={e => setFilter(e.target.value)}
        />
      </Stack>
      <DataGrid
        rows={filteredRows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 20, 50]}
        disableSelectionOnClick
        autoHeight
      />
    </Box>
  );
} 