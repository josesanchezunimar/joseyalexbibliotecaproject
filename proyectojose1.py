#variables para los archivos.txt
ALUMNOS_FILE = "alumnos.txt"
LIBROS_FILE = "libros.txt"
PRESTAMOS_FILE = "prestamos.txt"
SANCIONES_FILE = "sanciones.txt"
#trtando de simular la fecha actual para que el programa sepa cuando un año es bisiesto o no
#No estoy segro de si es necesario, pero teniendo en cuenta lo de los dias habiles lo dejo
#aun falta codigo para esta funcion
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
    return "2025-03-30"
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
mostrar_menu_principal()