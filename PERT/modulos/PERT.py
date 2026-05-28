actividades = []


def definir_actividades():

    cantidad = int(
        input("¿Cuántas actividades desea registrar?: ")
    )

    for i in range(cantidad):

        print(f"\nActividad {i+1}")

        nombre = input(
            "Nombre de la actividad: "
        )

        dependencia = input(
            "Dependencia (vacío si no tiene): "
        )

        duracion = int(
            input("Duración en días: ")
        )

        actividad = {

            "nombre": nombre,
            "dependencia": dependencia,
            "duracion": duracion
        }

        actividades.append(actividad)

    print("\nActividades registradas correctamente")


def calcular_ruta_critica():

    print("\n===== RUTA CRÍTICA =====")

    tiempo_total = 0

    for actividad in actividades:

        tiempo_total += actividad["duracion"]

        print(
            f"{actividad['nombre']} "
            f"-> {actividad['duracion']} días"
        )

    print(
        f"\nTiempo total del proyecto: "
        f"{tiempo_total} días"
    )


def mostrar_diagrama_pert():

    print("\n===== DIAGRAMA PERT =====")

    for actividad in actividades:

        if actividad["dependencia"] != "":

            print(
                f"{actividad['dependencia']} "
                f"----> "
                f"{actividad['nombre']}"
            )

        else:

            print(
                f"Inicio ----> "
                f"{actividad['nombre']}"
            )


def menu_pert():

    while True:

        print("\n===== MENÚ PERT =====")
        print("1. Definir actividades y dependencias")
        print("2. Calcular tiempos y ruta crítica")
        print("3. Mostrar diagrama PERT")
        print("4. Regresar al menú principal")

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            definir_actividades()

        elif opcion == "2":

            calcular_ruta_critica()

        elif opcion == "3":

            mostrar_diagrama_pert()

        elif opcion == "4":

            print(
                "Regresando al menú principal..."
            )

            break

        else:

            print("Opción inválida")