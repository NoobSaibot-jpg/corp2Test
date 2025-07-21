import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { getProducts, createProduct } from '../api/products';
import { 
  Box, 
  Button, 
  TextField, 
  Stack, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions,
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
  Select,
  MenuItem,
  Typography,
  Divider
} from '@mui/material';
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
  ArrowForward as ArrowForwardIcon,
  Edit as EditIcon,
  Print as PrintIcon
} from '@mui/icons-material';
import GlobalErrorSnackbar from './GlobalErrorSnackbar';

const columns = [
  { field: 'name', headerName: 'Назва', width: 200 },
  { field: 'type', headerName: 'Тип', width: 120 },
  { field: 'unit', headerName: 'Од. вим.', width: 120 },
  { field: 'price', headerName: 'Ціна', width: 120 },
  {
    field: 'actions',
    headerName: '',
    width: 120,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', gap: 1 }}>
        <IconButton size="small" color="primary">
          <EditIcon />
        </IconButton>
        <IconButton size="small" color="secondary">
          <PrintIcon />
        </IconButton>
      </Box>
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

export default function ProductList() {
  const [rows, setRows] = useState([]);
  const [filter, setFilter] = useState('');
  const [open, setOpen] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    name: '',
    type: 'product',
    unit: 'шт',
    price: '',
    description: '',
    barcode: '',
    weight: '',
    volume: '',
    manufacturer: '',
    country: 'Україна',
    group: '',
    subgroup: '',
    vat_rate: 20,
    min_stock: 0,
    max_stock: 1000,
    supplier: '',
    supplier_price: '',
    notes: ''
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    getProducts().then(data => setRows(data.map(p => ({ ...p, id: p.id })))).catch(setError);
  }, []);

  const filteredRows = rows.filter(row =>
    row.name?.toLowerCase().includes(filter.toLowerCase())
  );

  const handleRowClick = (params) => {
    const product = rows.find(r => r.id === params.id);
    if (product) {
      setIsEditing(true);
      setEditingId(product.id);
      setForm({
        name: product.name || '',
        type: product.type || 'product',
        unit: product.unit || 'шт',
        price: product.price || '',
        description: product.description || '',
        barcode: product.barcode || '',
        weight: product.weight || '',
        volume: product.volume || '',
        manufacturer: product.manufacturer || '',
        country: product.country || 'Україна',
        group: product.group || '',
        subgroup: product.subgroup || '',
        vat_rate: product.vat_rate || 20,
        min_stock: product.min_stock || 0,
        max_stock: product.max_stock || 1000,
        supplier: product.supplier || '',
        supplier_price: product.supplier_price || '',
        notes: product.notes || ''
      });
      setOpen(true);
    }
  };

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      if (isEditing) {
        // Здесь можно добавить API для обновления товара
        console.log('Updating product:', editingId, form);
      } else {
        await createProduct(form);
      }
      setRows(await getProducts().then(data => data.map(p => ({ ...p, id: p.id }))));
      setForm({
        name: '',
        type: 'product',
        unit: 'шт',
        price: '',
        description: '',
        barcode: '',
        weight: '',
        volume: '',
        manufacturer: '',
        country: 'Україна',
        group: '',
        subgroup: '',
        vat_rate: 20,
        min_stock: 0,
        max_stock: 1000,
        supplier: '',
        supplier_price: '',
        notes: ''
      });
      setOpen(false);
      setIsEditing(false);
      setEditingId(null);
      setError(null);
    } catch (err) {
      setError(err.response?.data || { message: 'Сталася помилка при створенні товару.' });
    }
  };

  const handleClose = () => {
    setOpen(false);
    setIsEditing(false);
    setEditingId(null);
    setForm({
      name: '',
      type: 'product',
      unit: 'шт',
      price: '',
      description: '',
      barcode: '',
      weight: '',
      volume: '',
      manufacturer: '',
      country: 'Україна',
      group: '',
      subgroup: '',
      vat_rate: 20,
      min_stock: 0,
      max_stock: 1000,
      supplier: '',
      supplier_price: '',
      notes: ''
    });
  };

  return (
    <Box sx={{ height: 600, width: '100%', mt: 4 }}>
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField
          label="Назва"
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
              {isEditing ? 'Редагування' : 'Створення'} товару: {form.name}
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
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
              <Tab label="Основні" />
              <Tab label="Характеристики" />
              <Tab label="Ціни" />
              <Tab label="Склад" />
              <Tab label="Додатково" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Назва товару"
                  value={form.name}
                  onChange={e => handleChange('name', e.target.value)}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={3}>
                <FormControl fullWidth>
                  <InputLabel>Тип</InputLabel>
                  <Select
                    value={form.type}
                    onChange={e => handleChange('type', e.target.value)}
                    label="Тип"
                  >
                    <MenuItem value="product">Товар</MenuItem>
                    <MenuItem value="service">Послуга</MenuItem>
                    <MenuItem value="material">Матеріал</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={3}>
                <TextField
                  label="Одиниця виміру"
                  value={form.unit}
                  onChange={e => handleChange('unit', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Опис"
                  value={form.description}
                  onChange={e => handleChange('description', e.target.value)}
                  fullWidth
                  multiline
                  rows={3}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Штрих-код"
                  value={form.barcode}
                  onChange={e => handleChange('barcode', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Виробник"
                  value={form.manufacturer}
                  onChange={e => handleChange('manufacturer', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Країна"
                  value={form.country}
                  onChange={e => handleChange('country', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Група товарів"
                  value={form.group}
                  onChange={e => handleChange('group', e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <TextField
                  label="Вага (кг)"
                  type="number"
                  value={form.weight}
                  onChange={e => handleChange('weight', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  label="Об'єм (л)"
                  type="number"
                  value={form.volume}
                  onChange={e => handleChange('volume', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  label="Підгрупа"
                  value={form.subgroup}
                  onChange={e => handleChange('subgroup', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Ставка ПДВ</InputLabel>
                  <Select
                    value={form.vat_rate}
                    onChange={e => handleChange('vat_rate', e.target.value)}
                    label="Ставка ПДВ"
                  >
                    <MenuItem value={0}>0%</MenuItem>
                    <MenuItem value={7}>7%</MenuItem>
                    <MenuItem value={20}>20%</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Примітки"
                  value={form.notes}
                  onChange={e => handleChange('notes', e.target.value)}
                  fullWidth
                  multiline
                  rows={3}
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Ціна продажу"
                  type="number"
                  value={form.price}
                  onChange={e => handleChange('price', e.target.value)}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Ціна постачальника"
                  type="number"
                  value={form.supplier_price}
                  onChange={e => handleChange('supplier_price', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Постачальник"
                  value={form.supplier}
                  onChange={e => handleChange('supplier', e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Мінімальний залишок"
                  type="number"
                  value={form.min_stock}
                  onChange={e => handleChange('min_stock', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Максимальний залишок"
                  type="number"
                  value={form.max_stock}
                  onChange={e => handleChange('max_stock', e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <Typography variant="h6" gutterBottom>
              Додаткова інформація
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  label="Повний опис"
                  value={form.description}
                  onChange={e => handleChange('description', e.target.value)}
                  fullWidth
                  multiline
                  rows={6}
                />
              </Grid>
            </Grid>
          </TabPanel>
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
            Товар
          </Button>
          <Button variant="outlined">
            Ще
          </Button>
        </DialogActions>
      </Dialog>
      <GlobalErrorSnackbar error={error} onClose={() => setError(null)} />
    </Box>
  );
}