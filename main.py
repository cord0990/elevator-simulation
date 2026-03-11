# BIBLIOTECAS Usadas Para este codigo ------------------------------------------------------------------------------------
import threading
import time
import random
import pygame

#Comando fundamental para inicializar PYGAME --------------------------------------------------------------------------------
pygame.init()

# CONFIGURACION DE PANTALLA  ------------------------------------------------------------------------------------------------
ancho_ventana, alto_ventana = 1000, 750  # Nuevas dimensiones de la ventana
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
clock = pygame.time.Clock()
alto_piso = alto_ventana // 11

# FUNCIONES USADAS EN EL CODIGO------------------------------------------------------------------------------------------------

#funcion para leer el archivo .txt desde donde se sacaran los datos de entrada-------------------------------------------------
def leer_datos_archivo(nombre_archivo):
    
    """
    Descripción:
    Esta función abre el archivo de texto 'datosascensores.txt', lee su contenido, y lo procesa para extraer los valores
    que definen la cantidad de ascensores, su capacidad, las personas totales, las personas por ciclo y los tiempos por piso dichos en el documento de la tarea"
    
    Parámetros:
    nombre_archivo (str): Nombre del archivo.

    Funcionamiento:
    Abre el archivo 'datosascensores.txt', lee cada linea del archivo y guarda lo leido en valores de tipo entero en una
    lista de 'lineas'.

    Luego cada valor en 'lineas' lo guardará en variables representativas del orden dichas en el documento de la tarea.

    Finalmente retorna estas variables.
    """
    with open(nombre_archivo, 'r') as archivo:
        lineas = [int(linea.strip()) for linea in archivo.readlines()]
    cantidad_ascensores = lineas[0] # Guarda el número de ascensores
    capacidad_ascensor = lineas[1] # Guarda la capacidad MAX de cada ascensor
    personas_totales = lineas[2] # Guarda el número total de personas dentro del codigo.
    personas_por_ciclo = lineas[3] # Guarda cuántas personas se suben por ciclo.
    tiempos_por_piso = lineas[4:14] # Guarda los tiempos que tarda el ascensor en recorrer cada piso (piso 1 a piso 10), desde los índices del 4 al 13.
    return cantidad_ascensores, capacidad_ascensor, personas_totales, personas_por_ciclo, tiempos_por_piso 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Función para Simular el Funcionamiento de un Ascensor dentro del codigo-----------------------------------------------------------------------------------------------------
def funcion_ascensor(id):
    """
    Descripcion:
    Esta funcion Simula el funcionamiento de un ascensor que recoge y deja pasajeros en diferentes pisos 
    todo esto con origen y destino final el piso 0.
    
    Parámetros:
    id (int): ID del ascensor que se está ejecutando (por ejemplo: el primer ascensor, segundo, etc.)

    Funcionamiento:
    El ascensor verifica si hay personas esperando en los pisos y ocurren 2 casos: 
        1.-Si las hay, las recoge y las lleva a sus destinos.
        2.-Si no hay pasajeros, el ascensor regresa al piso 0 a la espera de más personas.
    """
    global personas_en_espera, objetivo # Variables globales que almacenan las personas esperando y el destino del ascensor
    ascensor = ascensores[id]  # Se selecciona el ascensor específico de la lista 'ascensores' usando su índice único Que seria su ID.

    # Pausamos 2 segundos antes de que los ascensores empiezen a subir.
    time.sleep(2)  # Espera de 2 segundo

    # Loop caso 1:personas esperando un ascensor.
    while any(personas_en_espera):
        ascensor[2].acquire()  # Bloquea el semáforo para evitar errores en el acceso al ascensor
        pasajeros = ascensor[1] # Lista de personas que se encuentran dentro de un ascensor.

        #Ascensor Recoge personas que esperan el ascensor
        for piso in range(11):
            nuevos_esperando = [] # Lista para actualizar personas que siguen esperando un ascensor.
            for persona_id in personas_en_espera[piso]:
                persona = personas[persona_id] # Obtiene la persona por su ID
                if len(pasajeros) < cap_ascensor: # verifica que el ascensor no está lleno
                    if persona['situacion'] == 'p_subiendo':
                        pasajeros.append(persona_id)
                        persona['Estado grafico'] = 'ascensor_subiendo'  # Agrega persona al ascensor
                    elif persona['situacion'] == 'p_bajando' and persona['Estado grafico'] == 'lista_p_bajando':
                        pasajeros.append(persona_id)  # Agrega persona que desea bajar
                        persona['Estado grafico'] = 'ascensor_bajando'
                    else:
                        nuevos_esperando.append(persona_id) # Mantiene a las personas que aún deben esperar
                else:
                    nuevos_esperando.append(persona_id) # Si el ascensor está lleno, mantiene a las personas en espera
            personas_en_espera[piso] = nuevos_esperando # Actualiza la lista de personas que siguen esperando

        # Define los destinos de los pasajeros actuales
        destinos = []
        for p in pasajeros:
            persona = personas[p]
            if persona['situacion'] == 'p_subiendo':
                destinos.append(persona['destino']) # Si la persona está subiendo, se añade su destino.
            elif persona['situacion'] == 'p_bajando' and persona['Estado grafico'] == 'ascensor_bajando':
                destinos.append(0) # Si está bajando, su destino FINAL es el piso 0.
        destinos = sorted(set(destinos))  # Elimina destinos repetidos y los ordena.

        # Si no hay destinos, el ascensor irá en bajada para quedar en el piso 0 a la espera de más pasajeros.
        if not destinos:
            encontrado = False
            for piso in range(1, 11):
                for persona_id in personas_en_espera[piso]:
                    persona = personas[persona_id]
                    if persona['situacion'] == 'p_bajando' and persona['Estado grafico'] == 'lista_p_bajando':
                        objetivo = piso
                        encontrado = True
                        break
                if encontrado:
                    break
                
            # Si encontró personas que quieran bajar, las llevará a la calle primero (piso 0).
            if encontrado:
                while ascensor[0] < objetivo:
                    ascensor[0] += 1
                    recoger_personas_piso(ascensor, pasajeros)  # Recoge a las personas esperando en ese piso.
                    time.sleep(1)  # Pausa de 1 segundo entre movimientos
                while ascensor[0] > objetivo:
                    ascensor[0] -= 1
                    recoger_personas_piso(ascensor, pasajeros)
                    time.sleep(1)  # Pausa de 1 segundo entre movimientos
                    
            # Si no encontró personas que quieran bajar, libera el semáforo y espera.        
            else:
                ascensor[2].release() # Libera el semáforo para que el próximo ascensor pueda funcionar.
                time.sleep(1)
                continue

        # Si hay destinos, recorrerá los pisos para llevar a las personas a sus destinos
        for destino in destinos:
            while ascensor[0] < destino:
                ascensor[0] += 1
                recoger_personas_piso(ascensor, pasajeros) # Recoge personas en ese piso.
                time.sleep(1)  # Pausa de 1 segundo entre movimientos
            while ascensor[0] > destino:
                ascensor[0] -= 1
                recoger_personas_piso(ascensor, pasajeros)  #Recoge personas en ese piso.
                time.sleep(1)  # Pausa de 1 segundo entre movimientos

            # Baja a las personas en su destino
            nuevos_pasajeros = []
            for pasajero in pasajeros:
                persona = personas[pasajero]
                dest = persona['destino'] if persona['situacion'] == 'p_subiendo' else 0
                if dest == ascensor[0]:
                    # La persona que venía en el ascensor subiendo y llegó a su destino se baja y comienza a quedarse el tiempo correpondiente en ese piso
                    if persona['situacion'] == 'p_subiendo':
                        cooldown = tiempos_pisos[dest - 1]
                        persona['cooldown'] = cooldown * 30 # Multiplica el cooldown (tiempo de espera de la persona hasta que este disponible) por un factor.
                        persona['situacion'] = 'p_bajando'
                        persona['Estado grafico'] = 'espera'
                        threading.Thread(target=pers_esperar_y_regresar, args=(pasajero, dest, cooldown)).start()
                        
                    # La persona que venía bajando y se encuentra en el piso de la calle (piso 0) , se baja la persona y se finaliza el estado de esa misma.    
                    elif persona['situacion'] == 'p_bajando' and persona['Estado grafico'] == 'ascensor_bajando' and ascensor[0] == 0:
                        persona['situacion'] = 'finalizado'
                        persona['Estado grafico'] = 'finalizado'
                else:
                    nuevos_pasajeros.append(pasajero)
            pasajeros = nuevos_pasajeros
            ascensor[1] = pasajeros

        # Vuelve a planta baja si quedó en un piso superior.
        while ascensor[0] > 0:
            ascensor[0] -= 1
            recoger_personas_piso(ascensor, pasajeros)
            time.sleep(1)  # Pausa de 1 segundo entre movimientos

        # Verifica que hayan pasajeros dentro de un ascensor que necesiten bajar.
        nuevos_pasajeros = []
        for p in ascensor[1]:
            persona = personas[p]
            if persona['situacion'] == 'p_bajando' and persona['Estado grafico'] == 'ascensor_bajando' and ascensor[0] == 0:
                persona['situacion'] = 'finalizado'
                persona['Estado grafico'] = 'finalizado'
            else: 
                nuevos_pasajeros.append(p)
        ascensor[1] = nuevos_pasajeros

        # Fin de funcionamiento de este ascensor
        ascensor[2].release() # Libera el semáforo.
        time.sleep(1)
#Fin de la funcion-------------------------------------------------------------------------------------------------------------------------------------------

#funcion para gestionar_pasajeros_en_piso-----------------------------------------------------------------------------------------------------------------
def recoger_personas_piso(ascensor, pasajeros):
    """
    Descripción:
    Esta función se encarga de verificar si un ascensor en el piso actual hay personas que quieran bajar 
    y gestionar si pueden ingresar al ascensor o deben esperar.
    
    Parámetros:
    1.-ascensor (list): Lista que contiene los datos del ascensor (piso actual, pasajeros, semáforo).
    2.-pasajeros (list): Lista de las personas a bordo del ascensor, representadas por sus identificadores.

    Funcionamiento:
    Verifica si hay personas que desean bajar y ocurren 2 casos:
        1.-Si hay, la función comprueba si el ascensor tiene espacio suficiente para agregar más personas. 
            -Si el ascensor tiene espacio, las agrega a la lista de pasajeros.
            -Si el ascensor está lleno, las personas deben seguir esperando en el piso hasta que vea otro disponible.
        
        2.-Si no hay personas que deseen bajar, simplemente se vacía la lista de personas en espera en ese piso.

    """
    piso_actual = ascensor[0] # Obtiene el piso actual del ascensor.
    nuevos_esperando = [] # Lista para almacenar a las personas que seguirán esperando.
    
    # iteracion que Recorre todas las personas que están esperando en el piso actual.
    for persona_id in personas_en_espera[piso_actual]:
        persona = personas[persona_id] # Obtiene la persona por su ID.

        # Verifica si la persona quiere bajar y si está lista para hacerlo.
        if persona['situacion'] == 'p_bajando' and persona['Estado grafico'] == 'lista_p_bajando':
            if len(pasajeros) < cap_ascensor: # Si el ascensor no está lleno.
                pasajeros.append(persona_id) # Agrega la persona al ascensor.
                persona['Estado grafico'] = 'ascensor_bajando'
            else: # Si el ascensor está lleno, la persona sigue esperando.
                nuevos_esperando.append(persona_id)
                
         # Si no quiere bajar, sigue esperando.        
        else:
            nuevos_esperando.append(persona_id)
            
    # Finalmente aqui Actualiza la lista de personas que siguen esperando en ese piso.
    personas_en_espera[piso_actual] = nuevos_esperando
#Fin de la funcion-------------------------------------------------------------------------------------------------------------------------------------------

#Funcion para la espera y el regreso de las personas ----------------------------------------------------------------------------------------------------------
def pers_esperar_y_regresar(persona_id, piso_actual, tiempo):
    """
    Descripcion:
    Función que simula la espera de una persona en un piso y su posterior regreso a la lista de personas Disponibles para bajar.
    
    Parámetros:
    persona_id (int): ID único de la persona.
    piso_actual (int): Piso donde la persona está esperando.
    tiempo (int): Tiempo que la persona debe esperar antes de ser considerada lista para bajar.
    
    Funcionamiento:
    Funciona de la siguiente manera:
    1.-Primero duerme a la persona el tiempo estimado.
    2-Luego que despierta, reinicia su 'cooldown' a 0 y actualiza su 'Estado grafico' como listo para bajar.
    3-Posteriormente preguntará si el ID de esta persona no se encuentra en la lista de personas en espera de dicho piso, en el 
    caso que la persona NO se encuentra se añadirá a la lista.
    """
    time.sleep(tiempo) # La persona espera el tiempo estimado (duerme).
    
     # Restablece el "cooldown" de la persona a 0, indicando que ya está lista para tomar el ascensor.
    personas[persona_id]['cooldown'] = 0
    personas[persona_id]['Estado grafico'] = 'lista_p_bajando'
    
    # Verifica si la persona no está en la lista de personas esperando en el piso actual.
    if persona_id not in personas_en_espera[piso_actual]:
        # Si no está en la lista, la agrega a la lista de espera para ese piso.
        personas_en_espera[piso_actual].append(persona_id)
#Fin de la funcion-------------------------------------------------------------------------------------------------------------------------------------------

# Función para actualizar el tiempo de espera (cooldown) de las personas en fase de bajada.
def actualizar_cooldown():
    """
    Descripcion:
    Actualiza el cooldown de las personas que vayan bajando y que su cooldown sea mayor a 0.
    """
    # Una iteracion que Recorre todas las personas para actualizar su cooldown
    for p in personas:
        # Verifica si la persona está en fase de 'p_bajando' y tiene un cooldown mayor a 0
        if p['situacion'] == 'p_bajando' and p['cooldown'] > 0:
            p['cooldown'] -= 1 # Reduce el cooldown en 1 para la persona, indicando que ha pasado un ciclo de espera
#Fin de la funcion-------------------------------------------------------------------------------------------------------------------------------------------


# Funcion Importante la cual se muestra el estado de los ascensores y personas graficamente------------------------------------------------------------------
def dibujar():
    """
    Descripción:
    Esta función se encarga de dibujar el estado Grafico actual de los ascensores y las personas en la ventana de Pygame,
    mostrando tanto los ascensores en movimiento como las personas esperando o viajando entre los pisos mencionados.

    Funcionamiento:
    1.-Dibuja los pisos de la simulación en la pantalla.
    2.-Dibuja los ascensores y sus pasajeros dentro de ellos, representados por círculos de diferentes colores que representan su estado.
    3.-Actualiza la visualización de las personas esperando el ascensor y las que ya están dentro de los ascensores.
    4.-Los colores de las pelotitas indican el estado de las personas (subiendo, bajando, en espera).
    """
    # Dibuja el fondo
    ventana.fill((250, 250, 255))

    # Dibuja los pisos y su texto
    for i in range(11):
        y = alto_ventana - (i + 1) * alto_piso
        pygame.draw.line(ventana, (220, 220, 220), (0, y), (ancho_ventana, y))# Dibuja las líneas de los pisos
        font = pygame.font.SysFont(None, 20)
        texto = font.render(f'Piso {i}', True, (0, 0, 0))
        ventana.blit(texto, (5, y + 5))# Coloca el texto con el número de cada piso

    #Estructura ascensor 
        #1.-Dibuja el ascensor y sus pasajeros
        #2.-Los pasajeros que están subiendo se muestran en verde
        #3.- Los pasajeros que están bajando se muestran en amarillo
    
    for idx, (piso, pasajeros, _) in enumerate(ascensores):
        x = 70 + idx * 100  # posicion horizontal de los ascensore.
        y = alto_ventana - (piso + 1) * alto_piso  # Calcula la posición vertical del ascensor
        pygame.draw.rect(ventana, (169, 169, 169), (x, y, 55, alto_piso))  # Color del ascensor (en este caso gris)

        # Ajustes posicion y color personas dentro del ascensor
        for j, pid in enumerate(pasajeros):
            persona = personas[pid]
            if persona['Estado grafico'] == 'ascensor_subiendo':
                color = (0, 255, 0)  #color personas subiendo en el ascensor(Verde fosforescente)
            elif persona['Estado grafico'] == 'ascensor_bajando':
                color = (255, 255, 0)  #color personas bajando en el ascensor (Amarillo)
            else:
                color = (128, 0, 128) #En el caso que haya un error , la persona tomara el color morado

            # Calcula la posición de las pelotitas horizontalmente
            pygame.draw.circle(ventana, color, (x + 4 + j * 12, y + 25), 5)  


    # Dibuja las personas esperando el ascensor y las personas que todavía no lo esperan (caso cooldown)
    piso_posiciones = {p: {"esperando": 0, "inactivos": 0} for p in range(11)} 
    for p in personas:
        piso = 0 if p['situacion'] == 'p_subiendo' else p['destino'] # Calcula el piso según la situación de la persona
        y_base = alto_ventana - (piso + 1) * alto_piso + alto_piso // 2
        if p['Estado grafico'] == 'p_subiendo' or p['Estado grafico'] == 'lista_p_bajando':
            x = 600 + piso_posiciones[piso]["esperando"] * 10  # Posición horizontal para personas esperando 
            pygame.draw.circle(ventana, (0, 255, 0), (x, y_base), 6)  #Color Verde (esperando)
            piso_posiciones[piso]["esperando"] += 1
        elif p['Estado grafico'] == 'espera':
            x = 600 + piso_posiciones[piso]["inactivos"] * 10 # Posición horizontal para personas en espera
            pygame.draw.circle(ventana, (255, 0, 0), (x, y_base + 10), 6)  # Color Rojo (personas en espera "cooldown")
            piso_posiciones[piso]["inactivos"] += 1

    # Aqui se Actualiza la pantalla con los cambios realizado
    pygame.display.flip()
#Fin de la funcion-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------MAIN---------------------------------------------------------------------

# Lectura de datos desde El archivo (En el cual estaran los datos de entradas)
cant_ascensores, cap_ascensor, total_personas, ciclo_personas, tiempos_pisos = leer_datos_archivo('datosascensores.txt')

# Aqui se Inicializa la lista de personas esperando en cada piso (11 pisos)
personas_en_espera = [[] for _ in range(11)]

# Se crea una lista con sublistas que representan los datos de cada ascensor de la siguiente forma:
# ascensor = [piso actual, lista de pasajeros, semáforo]
ascensores = [[0, [], threading.Semaphore(1)] for _ in range(cant_ascensores)]

# Inicia un hilo para cada ascensor
personas = []
for i in range(total_personas):
    destino = random.randint(1, 10)
    personas.append({
        "id": i,
        "situacion": "p_subiendo",
        "destino": destino,
        "cooldown": 0,
        "Estado grafico": "p_subiendo"
    })
    personas_en_espera[0].append(i)

# Hebras para cada ascensor
hebras = []
for i in range(cant_ascensores):
    h = threading.Thread(target= funcion_ascensor, args=(i,))
    hebras.append(h)
    h.start()

# Bucle principal para ejecutar pygame
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    actualizar_cooldown() # Actualiza el cooldown de las personas que están bajando
    dibujar() # Dibuja la interfaz de Pygame
    clock.tick(30) # Limita la velocidad de actualización a 30 FPS
    
pygame.quit() # Cierra Pygame cuando termina la simulación
#Fin del programa-------------------------------------------------------------------------------------------------------------------------------------------