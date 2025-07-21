import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ProductList from './components/ProductList';
import CustomerList from './components/CustomerList';
import GoodsReceiptList from './components/GoodsReceiptList';
import GoodsIssueList from './components/GoodsIssueList';
import InvoiceList from './components/InvoiceList';
import StockList from './components/StockList';
import StockReport from './components/StockReport';
import { AppBar, Toolbar, Button, Container } from '@mui/material';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Товари та послуги</Button>
          <Button color="inherit" component={Link} to="/customers">Клієнти</Button>
          <Button color="inherit" component={Link} to="/goods-receipts">Надходження</Button>
          <Button color="inherit" component={Link} to="/goods-issues">Продажі</Button>
          <Button color="inherit" component={Link} to="/invoices">Рахунки-фактури</Button>
          <Button color="inherit" component={Link} to="/stock">Залишки</Button>
          <Button color="inherit" component={Link} to="/stock-report">Звіт по залишках</Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/customers" element={<CustomerList />} />
          <Route path="/goods-receipts" element={<GoodsReceiptList />} />
          <Route path="/goods-issues" element={<GoodsIssueList />} />
          <Route path="/invoices" element={<InvoiceList />} />
          <Route path="/stock" element={<StockList />} />
          <Route path="/stock-report" element={<StockReport />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;