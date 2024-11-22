from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = "your_secret_key"
# Database configuration
db_config = {
    'dbname': 'thongtin_new',  # Đổi tên database
    'user': 'postgres',
    'password': '130404',
    'host': 'localhost',
    'port': '5432',
    'table_name': 'hanghoa',
    'user_table': 'users'  # Thêm bảng users cho chức năng đăng nhập, đăng ký
}

def get_connection():
    """Establish a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
app.permanent_session_lifetime = timedelta(minutes=5)
# Kiểm tra người dùng đã đăng nhập chưa
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
@login_required
def index():
    """Home page displaying all items."""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(db_config['table_name']))
            cur.execute(query)
            hang_hoa = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('index.html', hang_hoa=hang_hoa)
        except Exception as e:
            flash(f"Error loading data: {e}", "error")
    return render_template('index.html', hang_hoa=[])

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Edit an existing item."""
    conn = get_connection()
    if conn:
        try:
            if request.method == 'POST':
                # Lấy thông tin từ form
                ten = request.form.get('ten')
                gia = request.form.get('gia')
                soluong = request.form.get('soluong')
                if ten and gia and soluong:
                    cur = conn.cursor()
                    query = sql.SQL("UPDATE {} SET ten = %s, gia = %s, soluong = %s WHERE id = %s").format(sql.Identifier(db_config['table_name']))
                    cur.execute(query, (ten, gia, soluong, item_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    flash("Cập nhật hàng hóa thành công!", "success")
                    return redirect(url_for('index'))
                else:
                    flash("Vui lòng nhập đầy đủ thông tin!", "warning")
            else:
                # Lấy thông tin hàng hóa từ database
                cur = conn.cursor()
                query = sql.SQL("SELECT * FROM {} WHERE id = %s").format(sql.Identifier(db_config['table_name']))
                cur.execute(query, (item_id,))
                item = cur.fetchone()
                cur.close()
                conn.close()

                if item:
                    return render_template('edit_item.html', item=item)
                else:
                    flash("Hàng hóa không tồn tại!", "error")
        except Exception as e:
            flash(f"Error editing item: {e}", "error")
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
@login_required
def add_item():
    """Add a new item."""
    ten = request.form.get('ten')
    gia = request.form.get('gia')
    soluong = request.form.get('soluong')
    if ten and gia and soluong:
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                query = sql.SQL("INSERT INTO {} (ten, gia, soluong) VALUES (%s, %s, %s)").format(sql.Identifier(db_config['table_name']))
                cur.execute(query, (ten, gia, soluong))
                conn.commit()
                cur.close()
                conn.close()
                flash("Thêm hàng hóa thành công!", "success")
            except Exception as e:
                flash(f"Error adding item: {e}", "error")
    else:
        flash("Vui lòng nhập đầy đủ thông tin!", "warning")
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_item():
    """Tìm kiếm hàng hóa."""
    query = request.form.get('query')
    results = []
    if query:
        conn = get_connection()
        if conn:
            try:
                cur = conn.cursor()
                # Ví dụ truy vấn tìm kiếm trong bảng hàng hóa
                query_sql = sql.SQL("SELECT * FROM {} WHERE ten ILIKE %s").format(sql.Identifier(db_config['table_name']))
                cur.execute(query_sql, ('%' + query + '%',))
                results = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                flash(f"Error searching items: {e}", "error")
    return render_template('search_results.html', results=results)

@app.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    """Delete an item."""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(db_config['table_name']))
            cur.execute(query, (item_id,))
            conn.commit()
            cur.close()
            conn.close()
            flash("Xóa hàng hóa thành công!", "success")
        except Exception as e:
            flash(f"Error deleting item: {e}", "error")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if username and password:
            password_hash = generate_password_hash(password)
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    query = sql.SQL("INSERT INTO {} (username, password, email) VALUES (%s, %s, %s)").format(sql.Identifier(db_config['user_table']))
                    cur.execute(query, (username, password_hash, email))
                    conn.commit()
                    cur.close()
                    conn.close()
                    flash("Đăng ký thành công!", "success")
                    return redirect(url_for('login'))
                except Exception as e:
                    flash(f"Error registering user: {e}", "error")
        else:
            flash("Vui lòng nhập đầy đủ thông tin!", "warning")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    query = sql.SQL("SELECT * FROM {} WHERE username = %s").format(sql.Identifier(db_config['user_table']))
                    cur.execute(query, (username,))
                    user = cur.fetchone()
                    cur.close()
                    conn.close()

                    if user and check_password_hash(user[2], password):  # Kiểm tra mật khẩu
                        session['user_id'] = user[0]  # Lưu ID người dùng vào session
                        flash("Đăng nhập thành công!", "success")
                        return redirect(url_for('index'))
                    else:
                        flash("Sai tên đăng nhập hoặc mật khẩu!", "error")
                except Exception as e:
                    flash(f"Error logging in: {e}", "error")
        else:
            flash("Vui lòng nhập đầy đủ thông tin!", "warning")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.pop('user_id', None)
    flash("Đăng xuất thành công!", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
