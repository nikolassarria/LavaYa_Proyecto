import os
import sys

HORARIOS_DISPONIBLES = [
    "12:00 AM", "2:00 AM", "4:00 AM", "6:00 AM",
    "8:00 AM", "10:00 AM", "12:00 PM", "2:00 PM",
    "4:00 PM", "6:00 PM", "8:00 PM", "10:00 PM"
]

class GestorLavaya:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            ruta_base = os.path.dirname(sys.executable)
        else:
            ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.archivo_datos = os.path.join(ruta_base, "datos.txt")
        self.usuarios_db = {}

    def registrar_usuario(self, nombre, usuario, correo, password, placa):
        if usuario in self.usuarios_db:
            return False, "Ese nombre de usuario ya está registrado."
        
        for datos in self.usuarios_db.values():
            if datos.get("correo") == correo:
                return False, "Ese correo @gmail.com ya está registrado."

        self.usuarios_db[usuario] = {
            "nombre": nombre,
            "correo": correo,
            "pass": password,
            "placa": placa
        }
        return True, "Registro exitoso"

    def validar_usuario(self, usuario, password):
        if usuario in self.usuarios_db and self.usuarios_db[usuario]["pass"] == password:
            return self.usuarios_db[usuario]["nombre"], self.usuarios_db[usuario]["placa"]
        return None, None

    def validar_admin(self, password):
        return password.strip() == "admin123"

    def calcular_total(self, precio_base, ajuste_vehiculo):
        return precio_base + ajuste_vehiculo

    def guardar_pedido(self, cliente, placa, vehiculo, servicio, turno, total):
        linea = f"Cliente: {cliente} | Placa: {placa} | {vehiculo} | {servicio} | Turno: {turno} | Total: ${total:,}\n"
        with open(self.archivo_datos, "a", encoding="utf-8") as archivo:
            archivo.write(linea)

    def obtener_turnos_ocupados(self):
        ocupados = []
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                for linea in f:
                    if "Turno: " in linea:
                        parte = linea.split("Turno: ")[1]
                        hora = parte.split(" | ")[0].strip()
                        ocupados.append(hora)
        return ocupados        

    def obtener_pedidos_y_total(self):
        pedidos = []
        total_dinero = 0
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                for linea in f:
                    linea_limpia = linea.strip()
                    if linea_limpia:
                        pedidos.append(linea_limpia)
                        if "Total: $" in linea_limpia:
                            try:
                                valor_str = linea_limpia.split("Total: $")[1].replace(",", "").strip()
                                total_dinero += int(valor_str)
                            except ValueError:
                                pass
        return pedidos, total_dinero

    def eliminar_pedido(self, indice):
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                registros = [l for l in f if l.strip()]
            if 0 <= indice < len(registros):
                registros.pop(indice)
                with open(self.archivo_datos, "w", encoding="utf-8") as f:
                    f.writelines(registros)
                return True
        return False