import os
#variables para los archivos.txt
ALUMNOS_FILE = "alumnos.txt"
LIBROS_FILE = "libros.txt"
PRESTAMOS_FILE = "prestamos.txt"
SANCIONES_FILE = "sanciones.txt"

#funcion para limpiar la pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def bisiesto(year):
    return year % 4 == 0 and (year % 400 == 0)

def dias_en_mes(mes, year):
    if mes == 2:
        return 29 if bisiesto(year) else 28
    elif mes in [4, 6, 9, 11]:
        return 30
    
    else:
        return 31
def sumar_dias_a_fecha(fecha, dias_sumar):
    year, mes, dia = map(int, fecha.split('-'))
    
    for _ in range(dias_sumar):
        dia += 1
        if dia > dias_en_mes(mes, year):
            dia = 1
            mes += 1
            if mes > 12:
                mes = 1
                anio += 1
 #funcion para asegurarse que el año tenga 4 digitos y el mes y el dia 2 digitos               
    return f"{year: 04d} {mes:02d} {dia:02d}"
#fecha actual para que el programa le tenga como refencia (sujeta a cambios)
def obtener_fecha_actual():
    return "2025-03-30"
def comparar_fechas(fecha1, fecha2):
    return fecha1 == fecha2

def fecha_es_menor_o_igual(fecha1, fecha2):
    year1, mes1, dia1 = map(int, fecha1.split('-'))
    year2, mes2, dia2 = map(int, fecha2.split('-'))
    
    if year1 < year2:
        return True
    elif year1 == year2:
        if mes1 < mes2:
            return True
        elif mes1 == mes2:
            return dia1 <= dia2
    return False

def validar_fecha(fecha):
    try:
        year, mes, dia = map(int, fecha.split('-'))
        if mes < 1 or mes > 12:
            return False
        if dia < 1 or dia > dias_en_mes(mes, year):
            return False
        return True
    except:
        return False
#prints para el menu
def mostrar_menu_principal():
    print("\n SISTEMA DE GESTIÓN DE BIBLIOTECA UNIMAR ")
    print("1. Registrar nuevo alumno")
    print("2. Registrar préstamo")
    print("3. Ver préstamos activos")
    print("4. Ver libros disponibles")
    print("5. Ver alumnos sancionados")
    print("6. Renovar préstamo")
    print("7. Devolver libro")
    print("8. Ingresar nuevo libro")
    print("9. Modificar registros")
    print("10. Eliminar registros")
    print("11. Buscar registros")
    print("0. Salir")
    
#funcion para asegurarse que la cedula tenga al menos 1 digito
def validar_cedula(cedula):
    return cedula.isdigit() and len(cedula) >= 1

def leer_archivo(nombre_archivo):
    datos = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as file:
            for linea in file:
                datos.append(linea.strip().split(';'))
    return datos

def escribir_archivo(nombre_archivo, datos):
    with open(nombre_archivo, 'w') as file:
        for registro in datos:
            file.write(';'.join(registro) + '\n')

def buscar_registro(nombre_archivo, criterio, posicion):
    datos = leer_archivo(nombre_archivo)
    for registro in datos:
        if registro[posicion] == criterio:
            return registro
    return None

def modificar_registro(nombre_archivo, criterio, posicion, nuevo_registro):
    datos = leer_archivo(nombre_archivo)
    for i, registro in enumerate(datos):
        if registro[posicion] == criterio:
            datos[i] = nuevo_registro
            escribir_archivo(nombre_archivo, datos)
            return True
    return False

def eliminar_registro(nombre_archivo, criterio, posicion):
    datos = leer_archivo(nombre_archivo)
    nuevos_datos = [registro for registro in datos if registro[posicion] != criterio]
    if len(nuevos_datos) < len(datos):
        escribir_archivo(nombre_archivo, nuevos_datos)
        return True
    return False

def sancionado(cedula):
    sanciones = leer_archivo(SANCIONES_FILE)
    hoy = obtener_fecha_actual()
    for sancion in sanciones:
        if sancion[0] == cedula:
            if fecha_es_menor_o_igual(sancion[2], hoy):
                return True
    return False

def verificar_sanciones():
    sanciones = leer_archivo(SANCIONES_FILE)
    hoy = obtener_fecha_actual()
    nuevas_sanciones = []
    actualizado = False
    
    for sancion in sanciones:
        if not fecha_es_menor_o_igual(sancion[2], hoy):
            nuevas_sanciones.append(sancion)
        else:
            actualizado = True
    
    if actualizado:
        escribir_archivo(SANCIONES_FILE, nuevas_sanciones)
    
    return actualizado

#funion y datos que vamos a utilizar para resgistrar un nuevo alumno
def registrar_alumno():
    clear_screen()
    print("\n REGISTRAR NUEVO ALUMNO ")
    
    cedula = input("Ingrese la cédula del alumno: ")
    if not validar_cedula(cedula):
        print("Cédula no válida. Debe contener solo números y al menos 6 dígitos.")
        return
    
    if buscar_registro(ALUMNOS_FILE, cedula, 0):
        print("Ya existe un alumno registrado con esta cédula.")
        return
    
    nombre = input("Ingrese el nombre completo del alumno: ")
    carrera = input("Ingrese la carrera del alumno: ")
    telefono = input("Ingrese el teléfono del alumno: ")
    
    nuevo_alumno = [cedula, nombre, carrera, telefono]
    alumnos = leer_archivo(ALUMNOS_FILE)
    alumnos.append(nuevo_alumno)
    escribir_archivo(ALUMNOS_FILE, alumnos)
    
    print("\nAlumno registrado exitosamente!")

def mostrar_alumnos():
    alumnos = leer_archivo(ALUMNOS_FILE)
    if not alumnos:
        print("No hay alumnos registrados.")
        return
    
    print("\n LISTA DE ALUMNOS ")
    for alumno in alumnos:
        print(f"Cédula: {alumno[0]}, Nombre: {alumno[1]}, Carrera: {alumno[2]}, Teléfono: {alumno[3]}")
       
# Funcion que vamos a utilizar para registrar y administrar los libros
def ingresar_libro():
    clear_screen()
    print("\n INGRESAR NUEVO LIBRO\n ")
    
    codigo = input("Ingrese el código del libro: ")
    if buscar_registro(LIBROS_FILE, codigo, 0):
        print("Ya existe un libro con este código.")
        return
    
    titulo = input("Ingrese el título del libro: ")
    autor = input("Ingrese el autor del libro: ")
    categoria = input("Ingrese la categoría del libro: ")
    cantidad = input("Ingrese la cantidad disponible: ")
    
    if not cantidad.isdigit() or int(cantidad) <= 0:
        print("La cantidad debe ser un número positivo.")
        return
    
    nuevo_libro = [codigo, titulo, autor, categoria, cantidad]
    libros = leer_archivo(LIBROS_FILE)
    libros.append(nuevo_libro)
    escribir_archivo(LIBROS_FILE, libros)
    
    print("\nLibro registrado exitosamente!")

def mostrar_libros():
    libros = leer_archivo(LIBROS_FILE)
    if not libros:
        print("No hay libros registrados.")
        return
    
    print(" INVENTARIO DE LIBROS \n")
    for libro in libros:
        print(f"Código: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}, Categoría: {libro[3]}, Cantidad: {libro[4]}")

# Funciones para préstamos
def registrar_prestamo():
    clear_screen()
    print(" REGISTRAR PRÉSTAMO\n ")
    
    cedula = input("Ingrese la cédula del alumno: ")
    alumno = buscar_registro(ALUMNOS_FILE, cedula, 0)
    if not alumno:
        print("No existe un alumno registrado con esta cédula.")
        return
    
    if sancionado(cedula):
        print("Este alumno está actualmente sancionado y no puede realizar préstamos.")
        return
    
    codigo_libro = input("Ingrese el código del libro: ")
    libro = buscar_registro(LIBROS_FILE, codigo_libro, 0)
    if not libro:
        print("No existe un libro con este código.")
        return
    
    if int(libro[4]) <= 0:
        print("No hay ejemplares disponibles de este libro.")
        return
    
#funcion para Verificar si el alumno ya tiene este libro prestado
    prestamos = leer_archivo(PRESTAMOS_FILE)
    for prestamo in prestamos:
        if prestamo[0] == cedula and prestamo[1] == codigo_libro and prestamo[4] == "activo":
            print("Este alumno ya tiene prestado este libro.")
            return
    
    fecha_prestamo = obtener_fecha_actual()
    fecha_devolucion = sumar_dias_a_fecha(fecha_prestamo, 3)
    
    nuevo_prestamo = [cedula, codigo_libro, fecha_prestamo, fecha_devolucion, 'activo']
    prestamos.append(nuevo_prestamo)
    escribir_archivo(PRESTAMOS_FILE, prestamos)
# Actualizar cantidad de libros disponibles
    libro[4] = str(int(libro[4]) - 1)
    modificar_registro(LIBROS_FILE, codigo_libro, 0, libro)
    
    print("Préstamo registrado exitosamente!\n")
    print(f"Fecha de devolución: {fecha_devolucion}")
#identacion corregida
def mostrar_prestamos_activos():
    clear_screen()
    print(" PRESTAMOS ACTIVOS\n ")
    
    prestamos = leer_archivo(PRESTAMOS_FILE)
    if not prestamos:
        print("No hay prestamos activos.")
        return
    
    hoy = obtener_fecha_actual()
    hay_sanciones = False
    
    for prestamo in prestamos:
        if prestamo[4] == 'activo':
            alumno = buscar_registro(ALUMNOS_FILE, prestamo[0], 0)
            libro = buscar_registro(LIBROS_FILE, prestamo[1], 0)
            
            if alumno and libro:
                estado = "En plazo"
                if not fecha_es_menor_o_igual(prestamo[3], hoy):
                    estado = "Vencido"
                    # Aplicar sanción si no está ya sancionado
                    if not sancionado(prestamo[0]):
                        fecha_fin_sancion = sumar_dias_a_fecha(hoy, 7)
                        nueva_sancion = [prestamo[0], hoy, fecha_fin_sancion]
                        sanciones = leer_archivo(SANCIONES_FILE)
                        sanciones.append(nueva_sancion)
                        escribir_archivo(SANCIONES_FILE, sanciones)
                        hay_sanciones = True
                
                print(f"Alumno: {alumno[1]} (Cédula: {alumno[0]})")
                print(f"Libro: {libro[1]} (Código: {libro[0]})")
                print(f"Fecha préstamo: {prestamo[2]}, Fecha devolución: {prestamo[3]}")
                print(f"Estado: {estado}")
                
    if hay_sanciones:
        print("Se han aplicado sanciones por préstamos vencidos \n")

def renovar_prestamo():
    clear_screen()
    print(" RENOVAR PRESTAMO\n")
    
    cedula = input("Ingrese la cedula del alumno: ")
    codigo_libro = input("Ingrese el código del libro: ")
    
    prestamo = None
    prestamos = leer_archivo(PRESTAMOS_FILE)
    for p in prestamos:
        if p[0] == cedula and p[1] == codigo_libro and p[4] == 'activo':
            prestamo = p
            break
    if not prestamo:
        print("No se encontro un préstamo activo con estos datos.")
        return
    if sancionado(cedula):
        print("Este alumno esta sancionado y no puede renovar préstamos.")
        return
    
# funcionalidad para verificar si el préstamo está vencido
    hoy = obtener_fecha_actual()
    if not fecha_es_menor_o_igual(prestamo[3], hoy):
        print("No se puede renovar un préstamo vencido.")
        return  
    
    nueva_fecha_devolucion = sumar_dias_a_fecha(hoy, 3)
    prestamo[3] = nueva_fecha_devolucion
    prestamo[2] = hoy  # asi actualiza la fecha de los préstamos
    
    modificar_registro(PRESTAMOS_FILE, cedula, 0, prestamo)
    
    print("\nPrestamo renovado exitosamente!")
    print(f"Nueva fecha de devolucion: {nueva_fecha_devolucion}")
