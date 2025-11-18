# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from db import db
from models import Cliente
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

# 📌 Endpoint de salud
@app.route("/health")
def health():
    return jsonify({"ok": True})

# 📌 Listar clientes con búsqueda y paginación
@app.route("/clientes", methods=["GET"])
def listar_clientes():
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = Cliente.query

    # Filtrar por razón social o CUIT si se pasa "search"
    if search:
        query = query.filter(
            db.or_(
                Cliente.razon_social.ilike(f"%{search}%"),
                Cliente.cuit.ilike(f"%{search}%")
            )
        )

    # Paginación
    paginated = query.order_by(Cliente.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    data = [
        {
            "id": c.id,
            "razon_social": c.razon_social,
            "cuit": c.cuit,
            "email": c.email,
            "telefono": c.telefono,
            "direccion": c.direccion,
            "activo": c.activo
        }
        for c in paginated.items
    ]

    return jsonify({
        "clientes": data,
        "total": paginated.total,
        "pages": paginated.pages,
        "page": paginated.page
    })

# 📌 Obtener cliente por ID
@app.route("/clientes/<int:id>", methods=["GET"])
def obtener_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify({
        "id": cliente.id,
        "razon_social": cliente.razon_social,
        "cuit": cliente.cuit,
        "email": cliente.email,
        "telefono": cliente.telefono,
        "direccion": cliente.direccion,
        "activo": cliente.activo
    })

# 📌 Alta de cliente
@app.route("/clientes", methods=["POST"])
def crear_cliente():
    data = request.get_json()
    nuevo = Cliente(
        razon_social=data.get("razon_social"),
        cuit=data.get("cuit"),
        email=data.get("email"),
        telefono=data.get("telefono"),
        direccion=data.get("direccion"),
        activo=data.get("activo", True)
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"message": "Cliente creado", "id": nuevo.id}), 201

# 📌 Modificación de cliente
@app.route("/clientes/<int:id>", methods=["PUT"])
def actualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    cliente.razon_social = data.get("razon_social", cliente.razon_social)
    cliente.cuit = data.get("cuit", cliente.cuit)
    cliente.email = data.get("email", cliente.email)
    cliente.telefono = data.get("telefono", cliente.telefono)
    cliente.direccion = data.get("direccion", cliente.direccion)
    cliente.activo = data.get("activo", cliente.activo)
    cliente.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Cliente actualizado"})

# 📌 Baja de cliente
@app.route("/clientes/<int:id>", methods=["DELETE"])
def borrar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado"})

# --- Bloque para arrancar el servidor ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # crea las tablas si no existen
    app.run(debug=True, port=4000)
