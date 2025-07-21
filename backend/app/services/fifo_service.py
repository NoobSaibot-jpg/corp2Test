from app.models.models import StockBatch, GoodsReceiptItem, GoodsIssueItem, GoodsReceipt, GoodsIssue
from app.db import db
from datetime import datetime

class FIFOService:
    @staticmethod
    def create_batches_from_receipt(receipt_id):
        """Создаёт партии товара из приходной накладной"""
        items = GoodsReceiptItem.query.filter_by(goods_receipt_id=receipt_id).all()
        
        for item in items:
            # Создаём партию для каждого товара
            batch = StockBatch(
                product_id=item.product_id,
                quantity=item.quantity,
                received_date=datetime.utcnow().date(),
                cost=item.price or 0
            )
            db.session.add(batch)
        
        db.session.commit()
    
    @staticmethod
    def get_available_stock(product_id):
        """Получает доступные остатки товара по FIFO"""
        batches = StockBatch.query.filter_by(product_id=product_id).filter(
            StockBatch.quantity > 0
        ).order_by(StockBatch.received_date.asc()).all()
        
        total_quantity = sum(batch.quantity for batch in batches)
        return total_quantity, batches
    
    @staticmethod
    def get_available_stock_on_date(product_id, date):
        """Получает остатки товара по FIFO на указанную дату"""
        # Суммируем все приходы до даты (включительно)
        receipts = GoodsReceiptItem.query.filter_by(product_id=product_id).filter(
            GoodsReceiptItem.goods_receipt.has(GoodsReceipt.date <= date)
        ).all()
        total_in = sum(item.quantity for item in receipts)
        # Суммируем все расходы до даты (включительно)
        issues = GoodsIssueItem.query.filter_by(product_id=product_id).filter(
            GoodsIssueItem.goods_issue.has(GoodsIssue.date <= date)
        ).all()
        total_out = sum(item.quantity for item in issues)
        available_quantity = total_in - total_out
        batches = []
        return max(available_quantity, 0), batches
    
    @staticmethod
    def consume_stock(product_id, required_quantity):
        """Списывает товар по FIFO"""
        if required_quantity <= 0:
            return True
        
        batches = StockBatch.query.filter_by(product_id=product_id).filter(
            StockBatch.quantity > 0
        ).order_by(StockBatch.received_date.asc()).all()
        
        remaining_quantity = required_quantity
        
        for batch in batches:
            if remaining_quantity <= 0:
                break
                
            if batch.quantity >= remaining_quantity:
                batch.quantity -= remaining_quantity
                remaining_quantity = 0
            else:
                remaining_quantity -= batch.quantity
                batch.quantity = 0
        
        db.session.commit()
        return remaining_quantity == 0
    
    @staticmethod
    def validate_stock_for_issue(items):
        """Проверяет достаточность остатков для расходной накладной"""
        errors = []
        
        for item in items:
            available_quantity, _ = FIFOService.get_available_stock(item['product_id'])
            if available_quantity < item['quantity']:
                errors.append({
                    'product_id': item['product_id'],
                    'required': item['quantity'],
                    'available': available_quantity,
                    'shortage': item['quantity'] - available_quantity
                })
        
        return errors 