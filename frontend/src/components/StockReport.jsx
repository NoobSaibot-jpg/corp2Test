import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, TextField, Box, Typography } from '@mui/material';
import axios from 'axios';

const columns = [
  { field: 'product_name', headerName: 'Товар', flex: 1 },
  { field: 'available_quantity', headerName: 'Залишок', flex: 1 },
  { field: 'unit', headerName: 'Од. вим.', flex: 1 },
];

export default function StockReport() {
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchReport = async (reportDate) => {
    setLoading(true);
    try {
      const res = await axios.get(`/api/stock/report?date=${reportDate}`);
      setRows(res.data.map((row, idx) => ({ id: idx + 1, ...row })));
    } catch (e) {
      setRows([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchReport(date);
  }, [date]);

  const handlePrint = () => {
    console.log('[DEBUG] Нажата кнопка печати, дата:', date);
    const printUrl = `http://localhost:5000/api/stock/report/print?date=${date}`;
    console.log('[DEBUG] URL для печати:', printUrl);
    try {
      window.open(printUrl, '_blank');
      console.log('[DEBUG] Окно печати открыто');
    } catch (error) {
      console.error('[DEBUG] Ошибка при открытии печати:', error);
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>Звіт по залишках на складі</Typography>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          label="Дата"
          type="date"
          value={date}
          onChange={e => setDate(e.target.value)}
          InputLabelProps={{ shrink: true }}
        />
        <Button variant="contained" onClick={handlePrint} disabled={loading}>
          Друк
        </Button>
      </Box>
      <DataGrid
        autoHeight
        rows={rows}
        columns={columns}
        loading={loading}
        pageSize={20}
        rowsPerPageOptions={[20, 50, 100]}
        disableSelectionOnClick
      />
    </Box>
  );
} 