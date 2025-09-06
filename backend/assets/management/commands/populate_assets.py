"""
Management command to populate sample asset management data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from assets.models import (
    Category, Vendor, Warehouse, Asset, InventoryItem, 
    StockLevel, PurchaseOrder, PurchaseOrderItem, 
    GoodsReceiptNote, MaintenanceSchedule, StockMovement
)
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for asset management system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample asset management data...'))
        
        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@company.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: admin/admin123')

        # Create categories
        categories_data = [
            ('IT Equipment', 'Computer hardware and software'),
            ('Office Furniture', 'Desks, chairs, cabinets'),
            ('Vehicles', 'Company cars and delivery vehicles'),
            ('Electronics', 'Phones, tablets, audio equipment'),
            ('Raw Materials', 'Manufacturing inputs and supplies'),
            ('Finished Products', 'Ready-to-sell products'),
            ('Safety Equipment', 'PPE and safety gear'),
            ('Tools & Machinery', 'Production tools and machines')
        ]
        
        categories = {}
        for name, desc in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories[name] = category
            if created:
                self.stdout.write(f'Created category: {name}')

        # Create vendors
        vendors_data = [
            ('TechSupply Corp', 'TECH001', 'John Smith', 'john@techsupply.com', '+1-555-0101'),
            ('Office Solutions Ltd', 'OFF001', 'Sarah Johnson', 'sarah@officesolutions.com', '+1-555-0102'),
            ('AutoFleet Services', 'AUTO001', 'Mike Davis', 'mike@autofleet.com', '+1-555-0103'),
            ('ElectroMax Inc', 'ELEC001', 'Lisa Wilson', 'lisa@electromax.com', '+1-555-0104'),
            ('MaterialSource Pro', 'MAT001', 'David Brown', 'david@materialsource.com', '+1-555-0105'),
            ('SafetyFirst Equipment', 'SAFE001', 'Emma Martinez', 'emma@safetyfirst.com', '+1-555-0106')
        ]
        
        vendors = {}
        for name, code, contact, email, phone in vendors_data:
            vendor, created = Vendor.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'contact_person': contact,
                    'email': email,
                    'phone': phone,
                    'address': f'123 {name} Street, Business City, BC 12345',
                    'city': 'Business City',
                    'state': 'BC',
                    'country': 'Canada',
                    'postal_code': '12345',
                    'payment_terms': 30  # 30 days
                }
            )
            vendors[name] = vendor
            if created:
                self.stdout.write(f'Created vendor: {name}')

        # Create warehouses
        warehouses_data = [
            ('Main Warehouse', 'WH001', '1000 Industrial Blvd, City, State 12345', 10000),
            ('IT Storage', 'WH002', '200 Tech Park Dr, City, State 12345', 2000),
            ('Office Supplies', 'WH003', '300 Business Ave, City, State 12345', 1500),
            ('Vehicle Depot', 'WH004', '400 Fleet St, City, State 12345', 5000)
        ]
        
        warehouses = {}
        for name, code, address, capacity in warehouses_data:
            warehouse, created = Warehouse.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'address': address,
                    'capacity': capacity,
                    'manager': admin_user
                }
            )
            warehouses[name] = warehouse
            if created:
                self.stdout.write(f'Created warehouse: {name}')

        # Create assets
        assets_data = [
            ('Dell Laptop 5520', 'LAP001', categories['IT Equipment'], vendors['TechSupply Corp'], 1200, 'ACTIVE', warehouses['IT Storage']),
            ('MacBook Pro 14"', 'LAP002', categories['IT Equipment'], vendors['TechSupply Corp'], 2500, 'ACTIVE', warehouses['IT Storage']),
            ('Office Desk - Executive', 'DESK001', categories['Office Furniture'], vendors['Office Solutions Ltd'], 800, 'ACTIVE', warehouses['Office Supplies']),
            ('Ergonomic Chair', 'CHAIR001', categories['Office Furniture'], vendors['Office Solutions Ltd'], 400, 'ACTIVE', warehouses['Office Supplies']),
            ('Company Vehicle - Sedan', 'VEH001', categories['Vehicles'], vendors['AutoFleet Services'], 25000, 'ACTIVE', warehouses['Vehicle Depot']),
            ('iPhone 15 Pro', 'PHN001', categories['Electronics'], vendors['ElectroMax Inc'], 1000, 'ACTIVE', warehouses['IT Storage']),
            ('Industrial Printer', 'PRT001', categories['IT Equipment'], vendors['TechSupply Corp'], 3500, 'MAINTENANCE', warehouses['Main Warehouse'])
        ]
        
        assets = {}
        for name, code, category, vendor, price, status, location in assets_data:
            asset, created = Asset.objects.get_or_create(
                asset_tag=code,
                defaults={
                    'name': name,
                    'category': category,
                    'vendor': vendor,
                    'purchase_cost': price,
                    'current_value': price * Decimal('0.8'),  # 20% depreciation
                    'status': status,
                    'location': location,
                    'assigned_to': admin_user if random.choice([True, False]) else None,
                    'purchase_date': date.today() - timedelta(days=random.randint(30, 365))
                }
            )
            assets[name] = asset
            if created:
                self.stdout.write(f'Created asset: {name}')

        # Create inventory items
        inventory_data = [
            ('Laptop Batteries', 'BATT001', categories['Electronics'], 50, 25, 100, 'SPARE_PARTS'),
            ('Office Paper A4', 'PAPER001', categories['Office Furniture'], 5, 10, 500, 'CONSUMABLES'),
            ('USB Cables', 'USB001', categories['Electronics'], 15, 5, 200, 'SPARE_PARTS'),
            ('Printer Ink Cartridges', 'INK001', categories['Electronics'], 30, 10, 100, 'CONSUMABLES'),
            ('Safety Helmets', 'HELM001', categories['Safety Equipment'], 25, 20, 150, 'FINISHED_GOODS'),
            ('Steel Rods 10mm', 'STEEL001', categories['Raw Materials'], 500, 50, 1000, 'RAW_MATERIAL')
        ]
        
        inventory_items = {}
        for name, sku, category, unit_cost, reorder_level, max_stock, item_type in inventory_data:
            item, created = InventoryItem.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'category': category,
                    'unit_cost': unit_cost,
                    'reorder_level': reorder_level,
                    'max_stock_level': max_stock,
                    'item_type': item_type,
                    'preferred_vendor': vendors[list(vendors.keys())[random.randint(0, len(vendors)-1)]]
                }
            )
            inventory_items[name] = item
            if created:
                self.stdout.write(f'Created inventory item: {name}')

        # Create stock levels for different warehouses
        for item_name, item in inventory_items.items():
            for warehouse_name, warehouse in warehouses.items():
                if random.choice([True, False]):  # Random assignment
                    stock_level, created = StockLevel.objects.get_or_create(
                        item=item,
                        warehouse=warehouse,
                        defaults={
                            'quantity': random.randint(10, 200),
                            'reserved_quantity': random.randint(0, 10)
                        }
                    )
                    if created:
                        self.stdout.write(f'Created stock level: {item_name} at {warehouse_name}')

        # Create purchase orders
        po_data = [
            ('TechSupply Corp', 'Main Warehouse', [('Laptop Batteries', 50), ('USB Cables', 100)]),
            ('Office Solutions Ltd', 'Office Supplies', [('Office Paper A4', 200)]),
            ('ElectroMax Inc', 'IT Storage', [('Printer Ink Cartridges', 25)]),
            ('SafetyFirst Equipment', 'Main Warehouse', [('Safety Helmets', 50)])
        ]
        
        for vendor_name, warehouse_name, items in po_data:
            po_number = f"PO{random.randint(1000, 9999)}"
            total_amount = sum([inventory_items[item_name].unit_cost * qty for item_name, qty in items])
            
            po, created = PurchaseOrder.objects.get_or_create(
                po_number=po_number,
                defaults={
                    'vendor': vendors[vendor_name],
                    'warehouse': warehouses[warehouse_name],
                    'order_date': date.today() - timedelta(days=random.randint(1, 30)),
                    'expected_delivery_date': date.today() + timedelta(days=random.randint(5, 15)),
                    'status': random.choice(['DRAFT', 'CONFIRMED', 'COMPLETED']),
                    'subtotal': total_amount,
                    'tax_amount': total_amount * Decimal('0.1'),
                    'total_amount': total_amount * Decimal('1.1'),
                    'created_by': admin_user,
                    'approved_by': admin_user if random.choice([True, False]) else None
                }
            )
            
            if created:
                self.stdout.write(f'Created purchase order: {po_number}')
                
                # Create PO items
                for item_name, qty in items:
                    PurchaseOrderItem.objects.get_or_create(
                        purchase_order=po,
                        item=inventory_items[item_name],
                        defaults={
                            'quantity': qty,
                            'unit_price': inventory_items[item_name].unit_cost,
                            'total_price': inventory_items[item_name].unit_cost * qty
                        }
                    )

        # Create maintenance schedules
        maintenance_data = [
            ('Industrial Printer', 'PREVENTIVE', 'Quarterly maintenance check', 150),
            ('Company Vehicle - Sedan', 'REPAIR', 'Oil change and tire rotation', 200),
            ('Dell Laptop 5520', 'INSPECTION', 'Hardware diagnostic test', 50)
        ]
        
        for asset_name, mtype, description, cost in maintenance_data:
            if asset_name in assets:
                maintenance, created = MaintenanceSchedule.objects.get_or_create(
                    asset=assets[asset_name],
                    scheduled_date=date.today() + timedelta(days=random.randint(1, 30)),
                    defaults={
                        'maintenance_type': mtype,
                        'description': description,
                        'cost': cost,
                        'performed_by': admin_user if random.choice([True, False]) else None,
                        'is_completed': random.choice([True, False])
                    }
                )
                if created:
                    self.stdout.write(f'Created maintenance schedule for: {asset_name}')

        # Create some stock movements
        movement_types = ['IN', 'OUT', 'TRANSFER', 'ADJUSTMENT']
        for i in range(10):
            item = random.choice(list(inventory_items.values()))
            warehouse = random.choice(list(warehouses.values()))
            
            movement, created = StockMovement.objects.get_or_create(
                item=item,
                warehouse=warehouse,
                movement_type=random.choice(movement_types),
                quantity=random.randint(1, 50),
                defaults={
                    'reference_number': f"MOV{random.randint(1000, 9999)}",
                    'notes': f"Stock movement for {item.name}",
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Created stock movement: {movement.reference_number}')

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created sample asset management data!\n'
                'You can now test the system with realistic data.'
            )
        )
