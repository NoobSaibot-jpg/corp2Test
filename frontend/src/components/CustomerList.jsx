import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { getCustomers, createCustomer, updateCustomer } from '../api/customers';
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
  Print as PrintIcon,
  Business as BusinessIcon,
  Person as PersonIcon
} from '@mui/icons-material';
import GlobalErrorSnackbar from './GlobalErrorSnackbar';

const columns = [
  { field: 'name', headerName: 'Ім\'я', width: 200 },
  { field: 'address', headerName: 'Адреса', width: 250 },
  { field: 'phone', headerName: 'Телефон', width: 180 },
  { field: 'edrpou', headerName: 'ЕДРПО', width: 150 },
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

export default function CustomerList() {
  const [rows, setRows] = useState([]);
  const [filter, setFilter] = useState('');
  const [open, setOpen] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    name: '',
    type: 'company',
    address: '',
    phone: '',
    email: '',
    edrpou: '',
    ipn: '',
    bank_name: '',
    bank_account: '',
    mfo: '',
    vat_certificate: '',
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    discount: 0,
    credit_limit: 0,
    payment_terms: '',
    notes: '',
    country: 'Україна',
    city: '',
    postal_code: '',
    website: '',
    tax_system: 'general',
    vat_payer: true
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    getCustomers().then(data => setRows(data.map(c => ({ ...c, id: c.id })))).catch(setError);
  }, []);

  const filteredRows = rows.filter(row =>
    row.name?.toLowerCase().includes(filter.toLowerCase())
  );

  const handleRowClick = (params) => {
    const customer = rows.find(r => r.id === params.id);
    if (customer) {
      setIsEditing(true);
      setEditingId(customer.id);
      setForm({
        name: customer.name || '',
        type: customer.type || 'company',
        address: customer.address || '',
        phone: customer.phone || '',
        email: customer.email || '',
        edrpou: customer.edrpou || '',
        ipn: customer.ipn || '',
        bank_name: customer.bank_name || '',
        bank_account: customer.bank_account || '',
        mfo: customer.mfo || '',
        vat_certificate: customer.vat_certificate || '',
        contact_person: customer.contact_person || '',
        contact_phone: customer.contact_phone || '',
        contact_email: customer.contact_email || '',
        discount: customer.discount || 0,
        credit_limit: customer.credit_limit || 0,
        payment_terms: customer.payment_terms || '',
        notes: customer.notes || '',
        country: customer.country || 'Україна',
        city: customer.city || '',
        postal_code: customer.postal_code || '',
        website: customer.website || '',
        tax_system: customer.tax_system || 'general',
        vat_payer: customer.vat_payer !== false
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
        await updateCustomer(editingId, form);
      } else {
        await createCustomer(form);
      }
      setRows(await getCustomers().then(data => data.map(c => ({ ...c, id: c.id }))));
      setForm({
        name: '',
        type: 'company',
        address: '',
        phone: '',
        email: '',
        edrpou: '',
        ipn: '',
        bank_name: '',
        bank_account: '',
        mfo: '',
        vat_certificate: '',
        contact_person: '',
        contact_phone: '',
        contact_email: '',
        discount: 0,
        credit_limit: 0,
        payment_terms: '',
        notes: '',
        country: 'Україна',
        city: '',
        postal_code: '',
        website: '',
        tax_system: 'general',
        vat_payer: true
      });
      setOpen(false);
      setIsEditing(false);
      setEditingId(null);
      setError(null);
    } catch (err) {
      setError(err.response?.data || { message: 'Сталася помилка при створенні клієнта.' });
    }
  };

  const handleClose = () => {
    setOpen(false);
    setIsEditing(false);
    setEditingId(null);
    setForm({
      name: '',
      type: 'company',
      address: '',
      phone: '',
      email: '',
      edrpou: '',
      ipn: '',
      bank_name: '',
      bank_account: '',
      mfo: '',
      vat_certificate: '',
      contact_person: '',
      contact_phone: '',
      contact_email: '',
      discount: 0,
      credit_limit: 0,
      payment_terms: '',
      notes: '',
      country: 'Україна',
      city: '',
      postal_code: '',
      website: '',
      tax_system: 'general',
      vat_payer: true
    });
  };

  return (
    <Box sx={{ height: 600, width: '100%', mt: 4 }}>
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField
          label="Ім'я"
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
              {isEditing ? 'Редагування' : 'Створення'} контрагента: {form.name}
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
              <Tab label="Контакти" />
              <Tab label="Банк" />
              <Tab label="Умови" />
              <Tab label="Додатково" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Назва контрагента"
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
                    <MenuItem value="company">
                      <BusinessIcon sx={{ mr: 1 }} />
                      Підприємство
                    </MenuItem>
                    <MenuItem value="individual">
                      <PersonIcon sx={{ mr: 1 }} />
                      Фізична особа
                    </MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={3}>
                <FormControl fullWidth>
                  <InputLabel>Система оподаткування</InputLabel>
                  <Select
                    value={form.tax_system}
                    onChange={e => handleChange('tax_system', e.target.value)}
                    label="Система оподаткування"
                  >
                    <MenuItem value="general">Загальна</MenuItem>
                    <MenuItem value="simplified">Спрощена</MenuItem>
                    <MenuItem value="single">Єдиний податок</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="ЄДРПОУ"
                  value={form.edrpou}
                  onChange={e => handleChange('edrpou', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="ІПН"
                  value={form.ipn}
                  onChange={e => handleChange('ipn', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Адреса"
                  value={form.address}
                  onChange={e => handleChange('address', e.target.value)}
                  fullWidth
                  multiline
                  rows={2}
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  label="Країна"
                  value={form.country}
                  onChange={e => handleChange('country', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  label="Місто"
                  value={form.city}
                  onChange={e => handleChange('city', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  label="Поштовий індекс"
                  value={form.postal_code}
                  onChange={e => handleChange('postal_code', e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Телефон"
                  value={form.phone}
                  onChange={e => handleChange('phone', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Email"
                  type="email"
                  value={form.email}
                  onChange={e => handleChange('email', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Веб-сайт"
                  value={form.website}
                  onChange={e => handleChange('website', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Контактна особа"
                  value={form.contact_person}
                  onChange={e => handleChange('contact_person', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Контактний телефон"
                  value={form.contact_phone}
                  onChange={e => handleChange('contact_phone', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Контактний email"
                  type="email"
                  value={form.contact_email}
                  onChange={e => handleChange('contact_email', e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Назва банку"
                  value={form.bank_name}
                  onChange={e => handleChange('bank_name', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="МФО"
                  value={form.mfo}
                  onChange={e => handleChange('mfo', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Рахунок"
                  value={form.bank_account}
                  onChange={e => handleChange('bank_account', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Свідоцтво ПДВ"
                  value={form.vat_certificate}
                  onChange={e => handleChange('vat_certificate', e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Знижка (%)"
                  type="number"
                  value={form.discount}
                  onChange={e => handleChange('discount', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Кредитний ліміт"
                  type="number"
                  value={form.credit_limit}
                  onChange={e => handleChange('credit_limit', e.target.value)}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Умови оплати"
                  value={form.payment_terms}
                  onChange={e => handleChange('payment_terms', e.target.value)}
                  fullWidth
                  multiline
                  rows={2}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Платник ПДВ</InputLabel>
                  <Select
                    value={form.vat_payer}
                    onChange={e => handleChange('vat_payer', e.target.value)}
                    label="Платник ПДВ"
                  >
                    <MenuItem value={true}>Так</MenuItem>
                    <MenuItem value={false}>Ні</MenuItem>
                  </Select>
                </FormControl>
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
                  label="Примітки"
                  value={form.notes}
                  onChange={e => handleChange('notes', e.target.value)}
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
            Контрагент
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