import sqlite3
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Función para conectar a la base de datos
def conectar():
    return sqlite3.connect('AmericanGym.db')

# Función para crear la tabla Socios
def crear_tabla_socios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''               
            CREATE TABLE IF NOT EXISTS Socios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                telefono TEXT,
                frecuencia_semanal INTEGER,
                estado TEXT CHECK(estado IN ('activo', 'inactivo')) DEFAULT 'activo',
                fecha_primer_pago DATE 
            )                  
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al crear la tabla Socios: {e}")
    finally:
        conn.close()

# Función para crear la tabla Pagos
def crear_tabla_pagos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                socio_id INTEGER NOT NULL,
                fecha_pago DATE NOT NULL,
                monto REAL NOT NULL,
                metodo_pago TEXT,
                notas TEXT,
                FOREIGN KEY (socio_id) REFERENCES Socios (id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al crear la tabla Pagos: {e}")
    finally:
        conn.close()

# Crear las tablas al iniciar el script
crear_tabla_socios()
crear_tabla_pagos()

# Función para insertar un nuevo socio
def insertar_socio(nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Socios (nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago))
        conn.commit()
        print(f"{Fore.GREEN}Socio insertado exitosamente.")
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al insertar socio: {e}")
    finally:
        conn.close()

# Función para insertar un nuevo pago
def insertar_pago(socio_id, fecha_pago, monto, metodo_pago, notas):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Pagos (socio_id, fecha_pago, monto, metodo_pago, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', (socio_id, fecha_pago, monto, metodo_pago, notas))
        conn.commit()
        print(f"{Fore.GREEN}Pago insertado exitosamente.")
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al insertar pago: {e}")
    finally:
        conn.close()

# Función para obtener todos los socios
def obtener_socios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Socios
        ''')
        socios = cursor.fetchall()
        return socios
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al obtener socios: {e}")
    finally:
        conn.close()

# Función para obtener un socio por su ID
def obtener_socio(socio_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Socios WHERE id = ?
        ''', (socio_id,))
        socio = cursor.fetchone()
        return socio
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al obtener socio: {e}")
    finally:
        conn.close()

# Función para obtener los pagos de un socio por su ID
def obtener_pagos_socio(socio_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Pagos WHERE socio_id = ?
        ''', (socio_id,))
        pagos = cursor.fetchall()
        return pagos
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al obtener pagos de un socio: {e}")
    finally:
        conn.close()

# Función para eliminar un pago por su ID
def eliminar_pago(pago_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Pagos WHERE id = ?
        ''', (pago_id,))
        conn.commit()
        print(f"{Fore.GREEN}Pago eliminado exitosamente.")
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al eliminar pago: {e}")
    finally:
        conn.close()

# Función para actualizar los datos de un socio
def actualizar_socio(socio_id, nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Socios SET nombre = ?, apellido = ?, dni = ?, telefono = ?, frecuencia_semanal = ?, fecha_primer_pago = ?
            WHERE id = ?
        ''', (nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago, socio_id))
        conn.commit()
        print(f"{Fore.GREEN}Socio actualizado exitosamente.")
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al actualizar socio: {e}")
    finally:
        conn.close()

# Función para mostrar el menú y manejar la interacción con el usuario
def menu():
    while True:
        print(f"{Fore.CYAN}1. Insertar socio")
        print(f"{Fore.CYAN}2. Insertar pago")
        print(f"{Fore.CYAN}3. Obtener socios")
        print(f"{Fore.CYAN}4. Obtener socio por ID")
        print(f"{Fore.CYAN}5. Obtener pagos de un socio")
        print(f"{Fore.CYAN}6. Eliminar pago")
        print(f"{Fore.CYAN}7. Actualizar socio")
        print(f"{Fore.CYAN}8. Salir")
        opcion = input(f"{Fore.YELLOW}Seleccione una opción: ")
        if opcion == '1':
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            telefono = input("Teléfono: ")
            frecuencia_semanal = int(input("Frecuencia semanal: "))
            fecha_primer_pago = input("Fecha primer pago (YYYY-MM-DD): ")
            insertar_socio(nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago)
        elif opcion == '2':
            socio_id = int(input("ID del socio: "))
            fecha_pago = input("Fecha de pago (YYYY-MM-DD): ")
            monto = float(input("Monto: "))
            metodo_pago = input("Método de pago: ")
            notas = input("Notas: ")
            insertar_pago(socio_id, fecha_pago, monto, metodo_pago, notas)
        elif opcion == '3':
            socios = obtener_socios()
            for socio in socios:
                print(socio)
        elif opcion == '4':
            socio_id = int(input("ID del socio: "))
            socio = obtener_socio(socio_id)
            print(socio)
        elif opcion == '5':
            socio_id = int(input("ID del socio: "))
            pagos = obtener_pagos_socio(socio_id)
            for pago in pagos:
                print(pago)
        elif opcion == '6':
            pago_id = int(input("ID del pago: "))
            eliminar_pago(pago_id)
        elif opcion == '7':
            socio_id = int(input("ID del socio: "))
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            telefono = input("Teléfono: ")
            frecuencia_semanal = int(input("Frecuencia semanal: "))
            fecha_primer_pago = input("Fecha primer pago (YYYY-MM-DD): ")
            actualizar_socio(socio_id, nombre, apellido, dni, telefono, frecuencia_semanal, fecha_primer_pago)
        elif opcion == '8':
            break
        else:
            print(f"{Fore.RED}Opción inválida")

# Ejecutar el menú si el script se ejecuta directamente
if __name__ == "__main__":
    menu()
