from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

dispositivos = []
solicitudes = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        rol = request.form.get("rol")
        codigo = request.form.get("codigo")
        
        if rol == "Administrador" and codigo != "7755":
            return "Codigo administrador incorrecto"
        
        session["correo"] = correo
        session["rol"] = rol
        return redirect("/panel")
    return render_template("login.html")

@app.route("/panel")
def panel():
    if "correo" not in session:
        return redirect("/")
    disponibles = len([d for d in dispositivos if d["estado"] == "Disponible"])
    pendientes = len([s for s in solicitudes if s["estado"] == "Pendiente"])
    ocupados = len([d for d in dispositivos if d["estado"] == "Ocupado"])
    return render_template("panel.html", correo=session["correo"], rol=session["rol"], dispositivos=dispositivos, solicitudes=solicitudes, disponibles=disponibles, pendientes=pendientes, ocupados=ocupados)

@app.route("/agregar_dispositivo", methods=["POST"])
def agregar_dispositivo():
    dispositivos.append({
        "id": len(dispositivos) + 1,
        "nombre": request.form.get("nombre"),
        "tipo": request.form.get("tipo"),
        "serie": request.form.get("serie"),
        "estado": "Disponible"
    })
    return redirect("/panel")

@app.route("/borrar_dispositivo/<int:id>")
def borrar_dispositivo(id):
    global dispositivos
    dispositivos = [d for d in dispositivos if d.get("id") != id]
    return redirect("/panel")

@app.route("/solicitar", methods=["POST"])
def solicitar():
    solicitudes.append({
        "nombre": request.form.get("nombre_solicitante"),
        "universidad": request.form.get("universidad"),
        "correo": request.form.get("correo_solicitante"),
        "dispositivo": request.form.get("dispositivo"),
        "motivo": request.form.get("motivo"),
        "estado": "Pendiente"
    })
    return redirect("/panel")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)