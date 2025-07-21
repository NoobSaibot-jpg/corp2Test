import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { getGoodsReceipts, createGoodsReceipt } from '../api/goodsReceipts';
import { getCustomers } from '../api/customers';
import { getProducts } from '../api/products';
import { 
  Box, 
  Button, 
  TextField, 
  Stack, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Typography,
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
  Divider,
  Chip
} from '@mui/material';
import { 
  Add as AddIcon, 
  Delete as DeleteIcon, 
  Print as PrintIcon,
  Save as SaveIcon,
  CheckCircle as CheckCircleIcon,
  MoreVert as MoreVertIcon,
  Star as StarIcon,
  Help as HelpIcon,
  Link as LinkIcon,
  Close as CloseIcon,
  ArrowBack as ArrowBackIcon,
  ArrowForward as ArrowForwardIcon
} from '@mui/icons-material';

const columns = [
  { field: 'date', headerName: 'Дата', width: 120 },
  { field: 'number', headerName: 'Номер', width: 150 },
  { field: 'supplier_name', headerName: 'Постачальник', width: 200 },
  { field: 'total_items', headerName: 'Позицій', width: 100 },
  { field: 'total_amount', headerName: 'Сума', width: 120 }
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

export default function GoodsReceiptList() {
  const [rows, setRows] = useState([]);
  const [filter, setFilter] = useState('');
  const [open, setOpen] = useState(false);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    date: new Date().toISOString().split('T')[0],
    time: '12:00:00',
    number: '',
    supplier_id: '',
    contract: '',
    organization: 'Добро',
    warehouse: 'Головний склад',
    operation_type: 'Покупка, комісія',
    pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
    comment: '',
    responsible: 'Абдулов Юрій Володимирович',
    items: [{ 
      product_id: '', 
      quantity: '', 
      unit: 'шт',
      coefficient: 1.000,
      price_with_vat: '',
      vat_rate: 20,
      account: '201'
    }]
  });

  useEffect(() => {
    getGoodsReceipts().then(data => {
      setRows(data.map((item) => ({
        id: item.id,
        date: item.date,
        number: item.number,
        operation: 'Купівля, комісія',
        sum: item.items?.reduce((acc, i) => acc + (i.price * i.quantity), 0) || 0,
        currency: 'грн',
        contractor: item.supplier_name,
        in_date: '',
        in_number: '',
        contract: '',
        supplier_id: item.supplier_id,
        items: item.items
      })));
    });
    getCustomers().then(setCustomers);
    getProducts().then(setProducts);
  }, []);

  const filteredRows = rows.filter(row =>
    row.contractor?.toLowerCase().includes(filter.toLowerCase())
  );

  const handleRowClick = (params) => {
    const receipt = rows.find(r => r.id === params.id);
    if (receipt) {
      setIsEditing(true);
      setEditingId(receipt.id);
      setForm({
        date: receipt.date,
        time: '12:00:00',
        number: receipt.number || '',
        supplier_id: receipt.supplier_id || '',
        contract: receipt.contract || '',
        organization: 'Добро',
        warehouse: 'Головний склад',
        operation_type: 'Покупка, комісія',
        pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
        comment: '',
        responsible: 'Абдулов Юрій Володимирович',
        items: receipt.items?.map(item => ({
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
          quantity: '', 
          unit: 'шт',
          coefficient: 1.000,
          price_with_vat: '',
          vat_rate: 20,
          account: '201'
        }]
      });
      setOpen(true);
    }
  };

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...form.items];
    newItems[index] = { ...newItems[index], [field]: value };
    
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
    
    setForm(prev => ({ ...prev, items: newItems }));
  };

  const addItem = () => {
    setForm(prev => ({
      ...prev,
      items: [...prev.items, { 
        product_id: '', 
        quantity: '', 
        unit: 'шт',
        coefficient: 1.000,
        price_with_vat: '',
        vat_rate: 20,
        account: '201'
      }]
    }));
  };

  const removeItem = (index) => {
    setForm(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
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

  const handleSubmit = async () => {
    const receiptData = {
      date: form.date,
      number: form.number,
      supplier_id: form.supplier_id ? parseInt(form.supplier_id) : null,
      items: form.items.filter(item => item.product_id && item.quantity).map(item => ({
        product_id: parseInt(item.product_id),
        quantity: parseFloat(item.quantity),
        price: parseFloat(item.price_with_vat) || 0
      }))
    };

    if (isEditing) {
      // Здесь можно добавить API для обновления накладной
      console.log('Updating receipt:', editingId, receiptData);
    } else {
      const created = await createGoodsReceipt(receiptData);
      setEditingId(created.id);
      setIsEditing(true);
      setOpen(true);
      // Можно загрузить данные по новой накладной, если нужно
      return;
    }
    
    // Оновлюємо список
    const newData = await getGoodsReceipts();
    setRows(newData.map((item) => ({
      id: item.id,
      date: item.date,
      number: item.number,
      operation: 'Купівля, комісія',
      sum: item.items?.reduce((acc, i) => acc + (i.price * i.quantity), 0) || 0,
      currency: 'грн',
      contractor: item.supplier_name,
      in_date: '',
      in_number: '',
      contract: '',
      supplier_id: item.supplier_id,
      items: item.items
    })));
    
    setForm({
      date: new Date().toISOString().split('T')[0],
      time: '12:00:00',
      number: '',
      supplier_id: '',
      contract: '',
      organization: 'Добро',
      warehouse: 'Головний склад',
      operation_type: 'Покупка, комісія',
      pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
      comment: '',
      responsible: 'Абдулов Юрій Володимирович',
      items: [{ 
        product_id: '', 
        quantity: '', 
        unit: 'шт',
        coefficient: 1.000,
        price_with_vat: '',
        vat_rate: 20,
        account: '201'
      }]
    });
    setOpen(false);
    setIsEditing(false);
    setEditingId(null);
  };

  const handleClose = () => {
    setOpen(false);
    setIsEditing(false);
    setEditingId(null);
    setForm({
      date: new Date().toISOString().split('T')[0],
      time: '12:00:00',
      number: '',
      supplier_id: '',
      contract: '',
      organization: 'Добро',
      warehouse: 'Головний склад',
      operation_type: 'Покупка, комісія',
      pricing_note: 'Ціна включає ПДВ. Тип цін: Дрібногуртова',
      comment: '',
      responsible: 'Абдулов Юрій Володимирович',
      items: [{ 
        product_id: '', 
        quantity: '', 
        unit: 'шт',
        coefficient: 1.000,
        price_with_vat: '',
        vat_rate: 20,
        account: '201'
      }]
    });
  };

  return (
    <Box sx={{ height: 600, width: '100%', mt: 4 }}>
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField
          label="Контрагент"
          value={filter}
          onChange={e => setFilter(e.target.value)}
        />
        <Button variant="contained" onClick={() => {
          setIsEditing(false);
          setEditingId(null);
          setOpen(true);
        }}>
          Створити
        </Button>
      </Stack>
      <DataGrid
        rows={filteredRows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 20, 50]}
        disableSelectionOnClick
        autoHeight
        onRowClick={handleRowClick}
        sx={{ cursor: 'pointer' }}
      />
      
      <Dialog open={open} onClose={handleClose} maxWidth="xl" fullWidth>
        <DialogTitle sx={{ bgcolor: 'primary.main', color: 'white', p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">
              {isEditing ? 'Редагування' : 'Створення'} прибуткової накладної {form.number} від {form.date} {form.time} ({form.operation_type})
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
                    value={form.supplier_id}
                    onChange={e => handleChange('supplier_id', e.target.value)}
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
          <Button
            variant="outlined"
            startIcon={<PrintIcon />}
            disabled={!editingId}
            onClick={() => editingId && window.open(`http://localhost:5000/api/goods_receipts/${editingId}/print`, '_blank')}
          >
            Друк
          </Button>
          <Button variant="outlined">
            Ще
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 