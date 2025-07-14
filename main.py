from proyecto import leer_archivo, escribir_archivo, nombre_existe, cargar_preguntas
import datetime

# Configuración de niveles
NIVELES = {
    1: {"preguntas": 4, "puntaje_por_acierto": 10},
    2: {"preguntas": 6, "puntaje_por_acierto": 15}, 
    3: {"preguntas": 8, "puntaje_por_acierto": 20}
}

def mostrar_menu():
    print("\n--- TRIVIA AVENTURA PYTHON ---")
    print("1. Iniciar nueva partida")
    print("2. Ver historial de partidas") 
    print("3. Editar nombre de jugador")
    print("4. Eliminar registro de jugador")
    print("5. Salir")

def nueva_partida():
    while True:
        nombre = input("\nNickname: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue
            
        if nombre_existe(nombre):
            print("▲ El nombre ya está en uso. Elige otro.")
        else:
            break
    
    puntaje_total = 0
    nivel_actual = 1
    
    while nivel_actual <= 3:
        print(f"\n--- NIVEL {nivel_actual} ---")
        preguntas = cargar_preguntas(nivel_actual)
        aciertos = 0
        
        for i in range(min(NIVELES[nivel_actual]["preguntas"], len(preguntas))):
            pregunta = preguntas[i]
            print(f"\nPregunta {i+1}: {pregunta['pregunta']}")
            for j, opcion in enumerate(pregunta['opciones']):
                print(f"{j+1}. {opcion}")
                
            while True:
                try:
                    respuesta = int(input("Respuesta (1-4): "))
                    if 1 <= respuesta <= 4:
                        break
                    print("Ingresa un número entre 1 y 4.")
                except ValueError:
                    print("Entrada inválida. Ingresa un número.")
            
            if respuesta == pregunta['respuesta']:
                aciertos += 1
                puntaje_total += NIVELES[nivel_actual]["puntaje_por_acierto"]
                print("✔ Correcto!")
            else:
                print(f"✖ Incorrecto. La respuesta era: {pregunta['respuesta']}")
        
        if aciertos > NIVELES[nivel_actual]["preguntas"] / 2:
            nivel_actual += 1
            print(f"\n★ Subiste al nivel {nivel_actual}!")
        else:
            print("\n☹ No pasaste al siguiente nivel.")
            break
    
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    escribir_archivo("historial.txt", f"{nombre}|{puntaje_total}|{nivel_actual-1}|{fecha}")
    print(f"\nPartida guardada. Puntaje total: {puntaje_total}, Nivel máximo: {nivel_actual-1}")

def ver_historial():
    lineas = leer_archivo("historial.txt")
    if not lineas:
        print("\nNo hay registros en el historial.")
        return
    
    print("\n--- HISTORIAL ---")
    print("Nombre".ljust(15), "Puntaje".ljust(10), "Nivel".ljust(8), "Fecha")
    print("-"*45)
    for linea in sorted(lineas, key=lambda x: int(x.split("|")[1]), reverse=True):
        nombre, puntaje, nivel, fecha = linea.strip().split("|")
        print(nombre.ljust(15), puntaje.ljust(10), nivel.ljust(8), fecha)

def editar_jugador():
    nombre_actual = input("\nNombre actual: ").strip()
    if not nombre_existe(nombre_actual):
        print("✗ Jugador no encontrado.")
        return
        
    nuevo_nombre = input("Nuevo nombre: ").strip()
    if not nuevo_nombre:
        print("El nombre no puede estar vacío.")
        return
        
    if nombre_existe(nuevo_nombre):
        print("▲ El nuevo nombre ya está en uso.")
        return
        
    lineas = leer_archivo("historial.txt")
    with open("historial.txt", "w") as f:
        for linea in lineas:
            if linea.startswith(nombre_actual + "|"):
                partes = linea.split("|")
                partes[0] = nuevo_nombre
                f.write("|".join(partes))
            else:
                f.write(linea)
    print("✔ Nombre actualizado correctamente.")

def eliminar_jugador():
    nombre = input("\nNombre a eliminar: ").strip()
    if not nombre_existe(nombre):
        print("✗ Jugador no encontrado.")
        return
        
    confirmacion = input(f"¿Eliminar a '{nombre}'? (s/n): ").lower()
    if confirmacion == "s":
        lineas = leer_archivo("historial.txt")
        with open("historial.txt", "w") as f:
            for linea in lineas:
                if not linea.startswith(nombre + "|"):
                    f.write(linea)
        print("✔ Jugador eliminado.")

def main():
    while True:
        mostrar_menu()
        opcion = input("\nOpción: ").strip()
        
        if opcion == "1":
            nueva_partida()
        elif opcion == "2":
            ver_historial()
        elif opcion == "3":
            editar_jugador()
        elif opcion == "4":
            eliminar_jugador()
        elif opcion == "5":
            print("\n¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()