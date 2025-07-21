import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { 
  Button, 
  TextField, 
  Box, 
  Typography, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Stack, 
  MenuItem, 
  Tabs, 
  Tab, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Grid, 
  Chip, 
  IconButton, 
  FormControl, 
  InputLabel, 
  Select 
} from '@mui/material';
import { getInvoices, createInvoice } from '../api/invoices';
import { getCustomers } from '../api/customers';
import { getProducts } from '../api/products';
import { 
  Add as AddIcon, 
  Delete as DeleteIcon, 
  Save as SaveIcon,
  CheckCircle as CheckCircleIcon,
  Star as StarIcon,
  Help as HelpIcon,
  Link as LinkIcon,
  Close as CloseIcon,
  ArrowBack as ArrowBackIcon,
  ArrowForward as ArrowForwardIcon
} from '@mui/icons-material';

const columns = [
  { field: 'date', headerName: 'Дата', width: 120 },
  { field: 'id', headerName: 'Номер', width: 100 },
  { field: 'order_id', headerName: 'Замовлення', width: 100 },
  { field: 'customer_name', headerName: 'Покупець', width: 200 },
  { field: 'total', headerName: 'Сума', width: 120 },
  {
    field: 'print',
    headerName: '',
    width: 80,
    renderCell: (params) => (
      <Button
        variant="outlined"
        size="small"
        onClick={(e) => {
          e.stopPropagation();
          window.open(`http://localhost:5000/api/invoices/${params.row.id}/print`, '_blank');
        }}
      >
        Друк
      </Button>
    )
  },
  {
    field: 'xml',
    headerName: '',
    width: 80,
    renderCell: (params) => (
      <Button
        variant="outlined"
        size="small"
        onClick={(e) => {
          e.stopPropagation();
          window.open(`http://localhost:5000/api/invoices/${params.row.id}/xml`, '_blank');
        }}
      >
        XML
      </Button>
    )
  }
];

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function InvoiceList() {
  const [rows, setRows] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [open, setOpen] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    date: new Date().toISOString().slice(0, 10),
    time: '12:00:00',
    number: '',
    customer_id: '',
    contract: '',
    organization: 'Добро',
    warehouse: 'Головний склад',
    operation_type: 'Продаж, комісія',
    pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
    comment: '',
    responsible: 'Абдулов Юрій Володимирович',
    items: [{ 
      product_id: '', 
      quantity: 1, 
      unit: 'шт',
      coefficient: 1.000,
      price_with_vat: 0,
      vat_rate: 20,
      account: '201'
    }]
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [invoices, customersData, productsData] = await Promise.all([
        getInvoices(),
        getCustomers(),
        getProducts()
      ]);
      
      setRows(invoices.map(invoice => ({
        ...invoice,
        id: invoice.id,
        customer_name: invoice.order?.customer?.name || 'Не вказано',
        customer_id: invoice.order?.customer_id,
        items: invoice.order?.items || []
      })));
      setCustomers(customersData);
      setProducts(productsData.filter(p => p.type === 'product'));
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const handleRowClick = (params) => {
    const invoice = rows.find(r => r.id === params.id);
    if (invoice) {
      setIsEditing(true);
      setEditingId(invoice.id);
      setForm({
        date: invoice.date,
        time: '12:00:00',
        number: invoice.id.toString(),
        customer_id: invoice.customer_id || '',
        contract: invoice.contract || '',
        organization: 'Добро',
        warehouse: 'Головний склад',
        operation_type: 'Продаж, комісія',
        pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
        comment: '',
        responsible: 'Абдулов Юрій Володимирович',
        items: invoice.items?.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          unit: item.product?.unit || 'шт',
          coefficient: 1.000,
          price_with_vat: item.price,
          vat_rate: 20,
          account: '201',
          sum_with_vat: item.price * item.quantity,
          vat_sum: (item.price * item.quantity) * 0.2 / 1.2,
          total: item.price * item.quantity
        })) || [{ 
          product_id: '', 
          quantity: 1, 
          unit: 'шт',
          coefficient: 1.000,
          price_with_vat: 0,
          vat_rate: 20,
          account: '201'
        }]
      });
      setOpen(true);
    }
  };

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value });
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...form.items];
    newItems[index] = { ...newItems[index], [field]: value };
    
    // Автоматически устанавливаем цену из продукта
    if (field === 'product_id') {
      const product = products.find(p => p.id === parseInt(value));
      if (product) {
        newItems[index].price_with_vat = product.price || 0;
      }
    }
    
    // Автоматически рассчитываем суммы
    if (field === 'quantity' || field === 'price_with_vat') {
      const item = newItems[index];
      if (item.quantity && item.price_with_vat) {
        const quantity = parseFloat(item.quantity);
        const priceWithVat = parseFloat(item.price_with_vat);
        const sumWithVat = quantity * priceWithVat;
        const vatSum = sumWithVat * 0.2 / 1.2;
        
        newItems[index] = {
          ...item,
          sum_with_vat: sumWithVat,
          vat_sum: vatSum,
          total: sumWithVat
        };
      }
    }
    
    setForm({ ...form, items: newItems });
  };

  const addItem = () => {
    setForm({
      ...form,
      items: [...form.items, { 
        product_id: '', 
        quantity: 1, 
        unit: 'шт',
        coefficient: 1.000,
        price_with_vat: 0,
        vat_rate: 20,
        account: '201'
      }]
    });
  };

  const removeItem = (index) => {
    const newItems = form.items.filter((_, i) => i !== index);
    setForm({ ...form, items: newItems });
  };

  const calculateTotals = () => {
    return form.items.reduce((acc, item) => {
      const sumWithVat = (item.sum_with_vat || 0);
      const vatSum = (item.vat_sum || 0);
      return {
        total: acc.total + sumWithVat,
        vat: acc.vat + vatSum
      };
    }, { total: 0, vat: 0 });
  };

  const totals = calculateTotals();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const invoiceData = {
        date: form.date,
        order_id: form.number,
        total: totals.total
      };
      
      if (isEditing) {
        // Здесь можно добавить API для обновления счета
        console.log('Updating invoice:', editingId, invoiceData);
      } else {
        await createInvoice(invoiceData);
      }
      
      await loadData();
      setForm({
        date: new Date().toISOString().slice(0, 10),
        time: '12:00:00',
        number: '',
        customer_id: '',
        contract: '',
        organization: 'Добро',
        warehouse: 'Головний склад',
        operation_type: 'Продаж, комісія',
        pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
        comment: '',
        responsible: 'Абдулов Юрій Володимирович',
        items: [{ 
          product_id: '', 
          quantity: 1, 
          unit: 'шт',
          coefficient: 1.000,
          price_with_vat: 0,
          vat_rate: 20,
          account: '201'
        }]
      });
      setOpen(false);
      setIsEditing(false);
      setEditingId(null);
    } catch (error) {
      console.error('Error creating invoice:', error);
    }
  };

  const handleClose = () => {
    setOpen(false);
    setIsEditing(false);
    setEditingId(null);
    setForm({
      date: new Date().toISOString().slice(0, 10),
      time: '12:00:00',
      number: '',
      customer_id: '',
      contract: '',
      organization: 'Добро',
      warehouse: 'Головний склад',
      operation_type: 'Продаж, комісія',
      pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
      comment: '',
      responsible: 'Абдулов Юрій Володимирович',
      items: [{ 
        product_id: '', 
        quantity: 1, 
        unit: 'шт',
        coefficient: 1.000,
        price_with_vat: 0,
        vat_rate: 20,
        account: '201'
      }]
    });
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>Рахунки-фактури</Typography>
      <Box sx={{ mb: 2 }}>
        <Button variant="contained" onClick={() => {
          setIsEditing(false);
          setEditingId(null);
          setOpen(true);
        }}>
          Створити рахунок-фактуру
        </Button>
      </Box>
      
      <DataGrid
        autoHeight
        rows={rows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 20, 50]}
        disableSelectionOnClick
        onRowClick={handleRowClick}
        sx={{ cursor: 'pointer' }}
      />

      <Dialog open={open} onClose={handleClose} maxWidth="xl" fullWidth>
        <DialogTitle sx={{ bgcolor: 'primary.main', color: 'white', p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">
              {isEditing ? 'Редагування' : 'Створення'} рахунку-фактури {form.number} від {form.date} {form.time} ({form.operation_type})
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <IconButton size="small" sx={{ color: 'white' }}>
                <ArrowBackIcon />
              </IconButton>
              <IconButton size="small" sx={{ color: 'white' }}>
                <ArrowForwardIcon />
              </IconButton>
              <IconButton size="small" sx={{ color: 'white' }}>
                <StarIcon />
              </IconButton>
              <IconButton size="small" sx={{ color: 'white' }}>
                <HelpIcon />
              </IconButton>
              <IconButton size="small" sx={{ color: 'white' }}>
                <LinkIcon />
              </IconButton>
              <IconButton size="small" sx={{ color: 'white' }} onClick={handleClose}>
                <CloseIcon />
              </IconButton>
            </Box>
          </Box>
        </DialogTitle>
        <DialogContent sx={{ p: 0 }}>
          <Box sx={{ p: 2, bgcolor: 'grey.100' }}>
            <Grid container spacing={2}>
              <Grid item xs={3}>
                <TextField
                  label="Номер"
                  value={form.number}
                  onChange={e => handleChange('number', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Дата"
                  type="date"
                  value={form.date}
                  onChange={e => handleChange('date', e.target.value)}
                  fullWidth
                  size="small"
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Час"
                  value={form.time}
                  onChange={e => handleChange('time', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
              <Grid item xs={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Контрагент</InputLabel>
                  <Select
                    value={form.customer_id}
                    onChange={e => handleChange('customer_id', e.target.value)}
                    label="Контрагент"
                  >
                    {customers.map(customer => (
                      <MenuItem key={customer.id} value={customer.id}>
                        {customer.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Вид операції"
                  value={form.operation_type}
                  onChange={e => handleChange('operation_type', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Договір"
                  value={form.contract}
                  onChange={e => handleChange('contract', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Організація"
                  value={form.organization}
                  onChange={e => handleChange('organization', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Склад"
                  value={form.warehouse}
                  onChange={e => handleChange('warehouse', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
            </Grid>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                {form.pricing_note}
              </Typography>
            </Box>
          </Box>

          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
              <Tab label={`Товари (${form.items.length})`} />
              <Tab label="Послуги" />
              <Tab label="Зворотна тара" />
              <Tab label="Рахунки розрахунків" />
              <Tab label="Додатково" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Box sx={{ mb: 2 }}>
              <Stack direction="row" spacing={1}>
                <Button variant="outlined" startIcon={<AddIcon />} onClick={addItem}>
                  Додати
                </Button>
                <Button variant="outlined">
                  Підбір
                </Button>
                <Button variant="outlined">
                  Змінити
                </Button>
              </Stack>
            </Box>

            <TableContainer component={Paper}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>N</TableCell>
                    <TableCell>Номенклатура</TableCell>
                    <TableCell>Кількість</TableCell>
                    <TableCell>Од.</TableCell>
                    <TableCell>К</TableCell>
                    <TableCell>Ціна з ПДВ</TableCell>
                    <TableCell>Сума з ПДВ</TableCell>
                    <TableCell>% ПДВ</TableCell>
                    <TableCell>Сума ПДВ</TableCell>
                    <TableCell>Всього</TableCell>
                    <TableCell>Рахунок</TableCell>
                    <TableCell>По</TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {form.items.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{index + 1}</TableCell>
                      <TableCell>
                        <FormControl fullWidth size="small">
                          <Select
                            value={item.product_id}
                            onChange={e => handleItemChange(index, 'product_id', e.target.value)}
                            displayEmpty
                          >
                            <MenuItem value="">
                              <em>Виберіть товар</em>
                            </MenuItem>
                            {products.map(product => (
                              <MenuItem key={product.id} value={product.id}>
                                {product.name}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </TableCell>
                      <TableCell>
                        <TextField
                          type="number"
                          value={item.quantity}
                          onChange={e => handleItemChange(index, 'quantity', e.target.value)}
                          size="small"
                          sx={{ width: 80 }}
                        />
                      </TableCell>
                      <TableCell>
                        <TextField
                          value={item.unit}
                          onChange={e => handleItemChange(index, 'unit', e.target.value)}
                          size="small"
                          sx={{ width: 60 }}
                        />
                      </TableCell>
                      <TableCell>
                        <TextField
                          type="number"
                          value={item.coefficient}
                          onChange={e => handleItemChange(index, 'coefficient', e.target.value)}
                          size="small"
                          sx={{ width: 80 }}
                        />
                      </TableCell>
                      <TableCell>
                        <TextField
                          type="number"
                          value={item.price_with_vat}
                          onChange={e => handleItemChange(index, 'price_with_vat', e.target.value)}
                          size="small"
                          sx={{ width: 100 }}
                        />
                      </TableCell>
                      <TableCell>{item.sum_with_vat?.toFixed(2) || '0.00'}</TableCell>
                      <TableCell>
                        <TextField
                          type="number"
                          value={item.vat_rate}
                          onChange={e => handleItemChange(index, 'vat_rate', e.target.value)}
                          size="small"
                          sx={{ width: 60 }}
                        />
                      </TableCell>
                      <TableCell>{item.vat_sum?.toFixed(2) || '0.00'}</TableCell>
                      <TableCell>{item.total?.toFixed(2) || '0.00'}</TableCell>
                      <TableCell>
                        <TextField
                          value={item.account}
                          onChange={e => handleItemChange(index, 'account', e.target.value)}
                          size="small"
                          sx={{ width: 60 }}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip label="On" size="small" color="success" />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" onClick={() => removeItem(index)} color="error">
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <Box sx={{ p: 2, bgcolor: 'grey.50', borderTop: 1, borderColor: 'divider' }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={3}>
                <Typography variant="h6">
                  Всього: {totals.total.toFixed(2)} грн
                </Typography>
              </Grid>
              <Grid item xs={3}>
                <Typography variant="h6">
                  ПДВ (у т.ч.): {totals.vat.toFixed(2)} грн
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Коментар"
                  value={form.comment}
                  onChange={e => handleChange('comment', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Відповідальний"
                  value={form.responsible}
                  onChange={e => handleChange('responsible', e.target.value)}
                  fullWidth
                  size="small"
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2, bgcolor: 'grey.100' }}>
          <Button 
            variant="contained" 
            startIcon={<CheckCircleIcon />}
            sx={{ bgcolor: 'warning.main', '&:hover': { bgcolor: 'warning.dark' } }}
            onClick={handleSubmit}
          >
            {isEditing ? 'Зберегти зміни' : 'Провести та закрити'}
          </Button>
          <Button variant="outlined" startIcon={<SaveIcon />}>
            Записати
          </Button>
          <Button variant="outlined">
            Провести
          </Button>
          <Button variant="outlined">
            Створити на підставі
          </Button>
          <Button variant="outlined">
            Рахунок-фактура
          </Button>
          <Button variant="outlined">
            Ще
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 