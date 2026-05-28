from modulos import menu_pert


while True:

    print("\n===== SISTEMA PRINCIPAL =====")
    print("1. Módulo PERT")
    print("2. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":

        menu_pert()

    elif opcion == "2":

        print("Saliendo del sistema...")
        break

    else:

        print("Opción inválida")