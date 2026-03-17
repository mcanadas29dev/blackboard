from flask import render_template, jsonify, abort
from flask_login import login_required

from app.database import get_pizarra_db, get_pizarra_db_write
from . import main_bp


@main_bp.route("/")
@login_required
def index():
    db = get_pizarra_db()

    # Lista de compra activa con info del producto y categoría
    items = db.execute(
        """
        SELECT
            lc.id,
            lc.comprado,
            p.id_producto,
            p.nombre,
            p.url_imagen,
            c.nombre AS categoria
        FROM lista_compra lc
        JOIN productos_mercadona p ON lc.id_producto = p.id_producto
        JOIN categorias c ON p.id_categoria_padre = c.id_categoria
        ORDER BY c.nombre, p.nombre
        """
    ).fetchall()

    # Agrupar por categoría
    categorias = {}
    for item in items:
        cat = item["categoria"]
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(dict(item))

    total = len(items)
    comprados = sum(1 for i in items if i["comprado"])

    return render_template(
        "main/index.html",
        categorias=categorias,
        total=total,
        comprados=comprados,
    )


@main_bp.route("/toggle/<int:item_id>", methods=["POST"])
@login_required
def toggle_comprado(item_id):
    """Marca/desmarca un item de la lista como comprado (AJAX)"""
    db_w = get_pizarra_db_write()

    item = db_w.execute(
        "SELECT id, comprado FROM lista_compra WHERE id = ?", (item_id,)
    ).fetchone()

    if not item:
        abort(404)

    nuevo_estado = 0 if item["comprado"] else 1
    db_w.execute(
        "UPDATE lista_compra SET comprado = ? WHERE id = ?",
        (nuevo_estado, item_id),
    )
    db_w.commit()

    return jsonify({"id": item_id, "comprado": bool(nuevo_estado)})


@main_bp.route("/catalogo")
@login_required
def catalogo():
    """Vista del catálogo completo con búsqueda"""
    db = get_pizarra_db()

    categorias = db.execute(
        "SELECT id_categoria, nombre FROM categorias ORDER BY nombre"
    ).fetchall()

    return render_template("main/catalogo.html", categorias=categorias)


@main_bp.route("/api/productos")
@login_required
def api_productos():
    """Endpoint JSON para búsqueda dinámica de productos"""
    from flask import request

    q = request.args.get("q", "").strip()
    cat_id = request.args.get("categoria", "").strip()
    db = get_pizarra_db()

    query = """
        SELECT p.id_producto, p.nombre, p.url_imagen, c.nombre AS categoria
        FROM productos_mercadona p
        JOIN categorias c ON p.id_categoria_padre = c.id_categoria
        WHERE 1=1
    """
    params = []

    if q:
        query += " AND p.nombre LIKE ?"
        params.append(f"%{q}%")
    if cat_id:
        query += " AND p.id_categoria_padre = ?"
        params.append(cat_id)

    query += " ORDER BY p.nombre LIMIT 50"

    rows = db.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])
