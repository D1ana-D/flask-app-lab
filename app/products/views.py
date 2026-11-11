import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename
from . import products_bp
from .forms import ProductForm

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
db_path = os.path.join(DATA_DIR, 'products.json')
db = TinyDB(db_path)
products_table = db.table('products')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_image(file):
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        return f"uploads/{unique_filename}"
    return None

def get_next_id():
    all_items = products_table.all()
    if not all_items:
        return 1
    return max(item['id'] for item in all_items) + 1

@products_bp.route('/')
@products_bp.route('/product')
def list_products():
    products = products_table.all()
    return render_template('products/products.html', products=products)

@products_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = save_image(form.image.data)
        
        new_product = {
            'id': get_next_id(),
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        products_table.insert(new_product)
        flash("Товар успішно додано!", "success")
        return redirect(url_for('products.list_products'))
        
    return render_template('products/add_product.html', form=form, title="Додати товар")

@products_bp.route('/product/<int:product_id>')
def detail_product(product_id):
    Product = Query()
    product = products_table.get(Product.id == product_id)
    if not product:
        abort(404)
    return render_template('products/detail_product.html', product=product)

@products_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    Product = Query()
    product = products_table.get(Product.id == product_id)
    if not product:
        abort(404)

    form = ProductForm(data=product)
    if form.validate_on_submit():
        new_image = save_image(form.image.data)
        image_path = new_image if new_image else product.get('image')
        
        updated_data = {
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path
        }
        products_table.update(updated_data, Product.id == product_id)
        flash("Товар успішно оновлено!", "success")
        return redirect(url_for('products.detail_product', product_id=product_id))

    return render_template('products/edit_product.html', form=form, product=product, title="Редагувати товар")

@products_bp.route('/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    Product = Query()
    product = products_table.get(Product.id == product_id)
    if not product:
        abort(404)
        
    products_table.remove(Product.id == product_id)
    flash("Товар успішно видалено!", "info")
    return redirect(url_for('products.list_products'))