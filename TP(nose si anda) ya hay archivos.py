import os
import csv
import random

empresas = {
    "Apple": 150.00,
    "Google": 2800.00,
    "Amazon": 3400.50,
    "Microsoft": 299.00,
    "Disney": 123.10
}

log_file = "log.txt"
portafolio_file = "portafolio.csv"

def log(message):
    with open(log_file, "a") as file:
        file.write(message + "\n")

def cargar_portafolio():
    portafolio = []
    if os.path.exists(portafolio_file):
        with open(portafolio_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                empresa, cantidad, precio = row
                portafolio.append([empresa, int(cantidad), float(precio)])
    return portafolio

def guardar_portafolio(portafolio):
    with open(portafolio_file, "w", newline='') as file:
        writer = csv.writer(file)
        for accion in portafolio:
            writer.writerow(accion)

def mostrar_empresas(empresas):
    for empresa, precio in empresas.items():
        print(f"{empresa}: ${precio:.2f}")

def agregar_empresa(empresas):
    nombre = input("\nIngrese el nombre de la nueva empresa: ").capitalize()
    precio_inicial = float(input("Ingrese el precio inicial de la acción: "))
    empresas[nombre] = precio_inicial
    print(f"Empresa '{nombre}' agregada con un precio inicial de ${precio_inicial:.2f}")
    log(f"Empresa '{nombre}' agregada con un precio inicial de ${precio_inicial:.2f}")

def menu_gestion_empresas():
    opcion = ""
    while opcion != "3":
        print("\n--- Menú de Gestión de Empresas ---")
        print("1. Mostrar empresas en el mercado")
        print("2. Agregar nueva empresa")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_empresas(empresas)
        elif opcion == "2":
            agregar_empresa(empresas)
        elif opcion == "3":
            print("Volviendo al menú principal...")
        else:
            print("Opción no válida. Intente de nuevo.")

def comprar_accion(empresas, saldo_usuario, portafolio):
    global saldo_usuario
    mostrar_empresas(empresas)
    nombre_empresa = input("Seleccione la empresa para comprar acciones (nombre): ").capitalize()
    
    if nombre_empresa in empresas:
        cantidad = int(input(f"Ingrese la cantidad de acciones de {nombre_empresa} a comprar: "))
        precio = empresas[nombre_empresa]
        costo_total = cantidad * precio
        
        if saldo_usuario >= costo_total:
            portafolio.append([nombre_empresa, cantidad, precio])
            saldo_usuario -= costo_total
            guardar_portafolio(portafolio)
            print(f"Has comprado {cantidad} acciones de {nombre_empresa} a ${precio:.2f} cada una.")
            log(f"Compra: {cantidad} acciones de {nombre_empresa} a ${precio:.2f} cada una.")
        else:
            print("Saldo insuficiente para realizar la compra.")
    else:
        print("La empresa seleccionada no existe en el mercado.")
def vender_accion(empresas, saldo_usuario, portafolio):
    global saldo_usuario
    if not portafolio:
        print("No tienes acciones en tu portafolio para vender.")
        log("Intento de venta fallido. Portafolio vacío.")
        return saldo_usuario, portafolio

    print("\nPortafolio actual:")
    for i, accion in enumerate(portafolio):
        print(f"{i + 1}. Empresa: {accion[0]}, Cantidad: {accion[1]}, Precio de compra: ${accion[2]:.2f}")

    try:
        seleccion = int(input("Seleccione la acción que desea vender (número): ")) - 1
    except ValueError:
        print("Selección inválida. Por favor, ingrese un número.")
        log("Intento de venta fallido. Selección inválida.")
        return saldo_usuario, portafolio

    if 0 <= seleccion < len(portafolio):
        empresa, cantidad, precio_compra = portafolio.pop(seleccion)
        precio_actual = empresas[empresa]
        ganancia_perdida = (precio_actual - precio_compra) * cantidad
        saldo_usuario += precio_actual * cantidad
        print(f"Has vendido {cantidad} acciones de {empresa} a ${precio_actual:.2f} cada una.")
        print(f"Ganancia/Pérdida de la transacción: ${ganancia_perdida:.2f}")
        print(f"Saldo actual: ${saldo_usuario:.2f}")
        log(f"Vendido {cantidad} acciones de {empresa} a ${precio_actual:.2f} cada una. Ganancia/Pérdida: ${ganancia_perdida:.2f}. Saldo actual: ${saldo_usuario:.2f}")
    else:
        print("Selección inválida.")
        log("Intento de venta fallido. Selección inválida.")
    
    return saldo_usuario, portafolio

def menu_gestion_compra():
    global saldo_usuario, portafolio
    while True:
        print("\n--- Menú de Compra y Venta de Acciones ---")
        print("1. Comprar acciones")
        print("2. Vender acciones")
        print("3. Volver al menú principal")
        op = input("Seleccione una opción: ")
        if op == "1":
            saldo_usuario, portafolio = comprar_accion(empresas, saldo_usuario, portafolio)
            guardar_portafolio(portafolio)
        elif op == "2":
            saldo_usuario, portafolio = vender_accion(empresas, saldo_usuario, portafolio)
            guardar_portafolio(portafolio)
        elif op == "3":
            print("Volviendo al menú principal...")
            return
        else:
            print("Error: Opción no válida. Intente de nuevo.")

def simular_dia(empresas):
    confirmacion1 = input("¿Desea avanzar un día en el mercado? (s/n): ").lower()
    if confirmacion1 != 's':
        print("Operación cancelada. Volviendo al menú principal...")
        return
    
    print("\nSimulando un día de mercado...")
    log("Simulando un día de mercado...")
    
    for nombre in empresas:
        cambio = random.uniform(-0.05, 0.05)
        empresas[nombre] *= (1 + cambio)
        log(f"Empresa {nombre} nuevo precio: ${empresas[nombre]:.2f}")

def mostrar_portafolio(portafolio, empresas):
    if not portafolio:
        print("No tienes acciones en tu portafolio.")
        return

    print("\n--- Portafolio de Inversiones ---")

    for accion in portafolio:
        empresa = accion[0]
        cantidad = accion[1]
        precio_compra = accion[2]
        precio_actual = empresas[empresa]

        print(f"Empresa: {empresa}")
        print(f"Cantidad de acciones: {cantidad}")
        print(f"Precio de compra: ${precio_compra:.2f}")
        print(f"Precio actual: ${precio_actual:.2f}\n")

def simular_10_dias(empresas):
    matriz_resumen = [[0.0 for _ in range(2)] for _ in range(len(empresas))]
    precios = list(empresas.values())
    
    for i in range(len(precios)):
        matriz_resumen[i][0] = precios[i]

    for dia in range(10):
        print(f"\n--- Día {dia + 1} de simulación ---")
        simular_dia(empresas)

    precios = list(empresas.values())
    for i in range(len(precios)):
        matriz_resumen[i][1] = precios[i]

    print("\n--- Resumen de precios después de 10 días ---")
    print("Empresa         Precio Inicial   Precio Final")
    for i, empresa in enumerate(empresas):
        print(f"{empresa:<15} ${matriz_resumen[i][0]:<14.2f} ${matriz_resumen[i][1]:.2f}")
        log(f"Empresa: {empresa}, Precio Inicial: ${matriz_resumen[i][0]:.2f}, Precio Final: ${matriz_resumen[i][1]:.2f}")

continuar = True
saldo_usuario = 1000.00
portafolio = cargar_portafolio()

def main():
    global continuar, saldo_usuario, portafolio
    while continuar:
        print()
        print("---------------------------")
        print("MENÚ DEL SISTEMA           ")
        print("---------------------------")
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción inválida. Por favor, ingrese un número.")
            continue
        print("[2] Opción 2 (Comprar/vender acciones)")
        print("[3] Opción 3 (Simular un día de mercado)")
        print("[4] Opción 4 (Mostrar portafolio)")
        print("[5] Opción 5 (Simular 10 días y generar matriz de resumen)")
        print("[0] Salir del programa")
        print()
        opcion = int(input("Seleccione una opción: "))
        if opcion in range(0, 6):
            if opcion == 0:
                continuar = False
            elif opcion == 1:
                menu_gestion_empresas()
            elif opcion == 2:
                menu_gestion_compra()
            elif opcion == 3:
                simular_dia(empresas)
            elif opcion == 4:
                mostrar_portafolio(portafolio, empresas)
            elif opcion == 5:
                simular_10_dias(empresas)
        else:
            input("Opción inválida. Presione ENTER para volver a seleccionar.")

        if continuar:
            print()
            input("Presione ENTER para volver al menú.")

if __name__ == "__main__":
    main()











