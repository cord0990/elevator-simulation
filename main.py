# ---------------------------------------------------------------------------------
# LIBRARIES
# ---------------------------------------------------------------------------------
import threading
import time
import random
import pygame

# Initialize PYGAME
pygame.init()

# ---------------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------------
CONFIG_FILE = 'datosascensores.txt'  # Input configuration file
COOLDOWN_FACTOR = 30                 # Multiplier applied to floor wait time for visual cooldown
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 750
FLOORS = 11

# ---------------------------------------------------------------------------------
# SCREEN SETUP
# ---------------------------------------------------------------------------------
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
floor_height = WINDOW_HEIGHT // FLOORS

# ---------------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------------

def read_config_file(filename):
    """
    Descripción:
    Abre el archivo de texto de configuración, lee su contenido y extrae los valores
    que definen la cantidad de ascensores, su capacidad, las personas totales,
    las personas por ciclo y los tiempos por piso.

    Parámetros:
    filename (str): Nombre del archivo de configuración.

    Retorna:
    num_elevators (int), elevator_capacity (int), total_people (int),
    people_per_cycle (int), floor_times (list)
    """
    with open(filename, 'r') as file:
        lines = [int(line.strip()) for line in file.readlines()]

    num_elevators    = lines[0]      # Number of elevators
    elevator_capacity = lines[1]     # Max capacity of each elevator
    total_people     = lines[2]      # Total number of people in the simulation
    people_per_cycle = lines[3]      # People added per cycle
    floor_times      = lines[4:14]   # Time spent on each floor (floors 1–10)

    return num_elevators, elevator_capacity, total_people, people_per_cycle, floor_times


def elevator_function(elevator_id):
    """
    Descripción:
    Simula el funcionamiento de un ascensor que recoge y deja pasajeros
    en diferentes pisos, teniendo siempre como base el piso 0.

    Parámetros:
    elevator_id (int): ID único del hilo del ascensor.

    Funcionamiento:
    - Si hay personas esperando, el ascensor las recoge y las lleva a sus destinos.
    - Si no hay pasajeros, el ascensor regresa al piso 0 a esperar.
    """
    global people_waiting  # Global list storing people waiting on each floor

    elevator = elevators[elevator_id]  # Select the elevator by its ID

    # Wait 2 seconds before elevators start moving
    time.sleep(2)

    # Main loop: runs while there are people waiting on any floor
    while any(people_waiting):
        elevator[2].acquire()  # Acquire semaphore to prevent race conditions

        passengers = elevator[1]  # List of people currently inside the elevator

        # Pick up people waiting on each floor
        for floor in range(FLOORS):
            still_waiting = []  # People who remain waiting after this pass
            for person_id in people_waiting[floor]:
                person = people[person_id]
                if len(passengers) < elev_capacity:  # Check elevator is not full
                    if person['status'] == 'going_up':
                        passengers.append(person_id)
                        person['graphic_state'] = 'elevator_up'
                    elif person['status'] == 'going_down' and person['graphic_state'] == 'ready_to_descend':
                        passengers.append(person_id)
                        person['graphic_state'] = 'elevator_down'
                    else:
                        still_waiting.append(person_id)
                else:
                    still_waiting.append(person_id)  # Elevator full, person keeps waiting
            people_waiting[floor] = still_waiting

        # Determine destinations of current passengers
        destinations = []
        for p in passengers:
            person = people[p]
            if person['status'] == 'going_up':
                destinations.append(person['destination'])
            elif person['status'] == 'going_down' and person['graphic_state'] == 'elevator_down':
                destinations.append(0)  # People going down always return to floor 0
        destinations = sorted(set(destinations))  # Remove duplicates and sort

        # If no destinations, look for people waiting to go down
        if not destinations:
            target_floor = None
            for floor in range(1, FLOORS):
                for person_id in people_waiting[floor]:
                    person = people[person_id]
                    if person['status'] == 'going_down' and person['graphic_state'] == 'ready_to_descend':
                        target_floor = floor
                        break
                if target_floor is not None:
                    break

            # If found someone waiting to go down, move toward them
            if target_floor is not None:
                while elevator[0] < target_floor:
                    elevator[0] += 1
                    pick_up_on_floor(elevator, passengers)
                    time.sleep(1)
                while elevator[0] > target_floor:
                    elevator[0] -= 1
                    pick_up_on_floor(elevator, passengers)
                    time.sleep(1)
            else:
                # No one to pick up, release semaphore and wait
                elevator[2].release()
                time.sleep(1)
                continue

        # Move toward each destination and drop off passengers
        for destination in destinations:
            while elevator[0] < destination:
                elevator[0] += 1
                pick_up_on_floor(elevator, passengers)
                time.sleep(1)
            while elevator[0] > destination:
                elevator[0] -= 1
                pick_up_on_floor(elevator, passengers)
                time.sleep(1)

            # Drop off passengers who have reached their destination
            remaining_passengers = []
            for passenger in passengers:
                person = people[passenger]
                dest = person['destination'] if person['status'] == 'going_up' else 0
                if dest == elevator[0]:
                    if person['status'] == 'going_up':
                        # Passenger arrived at destination — start cooldown wait
                        cooldown = floor_times[dest - 1]
                        person['cooldown'] = cooldown * COOLDOWN_FACTOR
                        person['status'] = 'going_down'
                        person['graphic_state'] = 'waiting'
                        threading.Thread(
                            target=wait_and_return,
                            args=(passenger, dest, cooldown)
                        ).start()
                    elif person['status'] == 'going_down' and person['graphic_state'] == 'elevator_down' and elevator[0] == 0:
                        # Passenger reached ground floor — simulation complete for this person
                        person['status'] = 'finished'
                        person['graphic_state'] = 'finished'
                else:
                    remaining_passengers.append(passenger)
            passengers = remaining_passengers
            elevator[1] = passengers

        # Return to ground floor if elevator ended up on an upper floor
        while elevator[0] > 0:
            elevator[0] -= 1
            pick_up_on_floor(elevator, passengers)
            time.sleep(1)

        # Drop off any remaining passengers who need to exit at floor 0
        remaining_passengers = []
        for p in elevator[1]:
            person = people[p]
            if person['status'] == 'going_down' and person['graphic_state'] == 'elevator_down' and elevator[0] == 0:
                person['status'] = 'finished'
                person['graphic_state'] = 'finished'
            else:
                remaining_passengers.append(p)
        elevator[1] = remaining_passengers

        # Release semaphore for next elevator
        elevator[2].release()
        time.sleep(1)


def pick_up_on_floor(elevator, passengers):
    """
    Descripción:
    Verifica si hay personas en el piso actual que quieran bajar
    y las sube al ascensor si hay espacio disponible.

    Parámetros:
    elevator (list): Datos del ascensor [piso_actual, lista_pasajeros, semáforo].
    passengers (list): Lista de IDs de pasajeros dentro del ascensor.

    Funcionamiento:
    - Si una persona está lista para bajar y hay espacio, sube al ascensor.
    - Si el ascensor está lleno, la persona continúa esperando en el piso.
    """
    current_floor = elevator[0]
    still_waiting = []

    for person_id in people_waiting[current_floor]:
        person = people[person_id]

        if person['status'] == 'going_down' and person['graphic_state'] == 'ready_to_descend':
            if len(passengers) < elev_capacity:
                passengers.append(person_id)
                person['graphic_state'] = 'elevator_down'
            else:
                still_waiting.append(person_id)  # Elevator full
        else:
            still_waiting.append(person_id)  # Not ready to descend yet

    people_waiting[current_floor] = still_waiting


def wait_and_return(person_id, current_floor, wait_time):
    """
    Descripción:
    Simula la espera de una persona en su piso de destino antes de volver
    a la lista de espera para tomar el ascensor de bajada.

    Parámetros:
    person_id (int): ID único de la persona.
    current_floor (int): Piso donde la persona está esperando.
    wait_time (int): Tiempo en segundos antes de que la persona esté lista para bajar.

    Funcionamiento:
    1. Duerme el tiempo de espera indicado.
    2. Reinicia el cooldown a 0 y actualiza el estado gráfico a ready_to_descend.
    3. Agrega a la persona a la lista de espera del piso si aún no está en ella.
    """
    time.sleep(wait_time)

    people[person_id]['cooldown'] = 0
    people[person_id]['graphic_state'] = 'ready_to_descend'

    if person_id not in people_waiting[current_floor]:
        people_waiting[current_floor].append(person_id)


def update_cooldowns():
    """
    Descripción:
    Decrementa el contador de cooldown de todas las personas en estado going_down
    que tengan un cooldown mayor a 0. Se llama una vez por frame.
    """
    for p in people:
        if p['status'] == 'going_down' and p['cooldown'] > 0:
            p['cooldown'] -= 1


def draw():
    """
    Descripción:
    Renderiza el estado actual de la simulación en la ventana de Pygame.

    Dibuja:
    1. Líneas y etiquetas de los pisos.
    2. Ascensores con pasajeros dentro identificados por color.
    3. Personas esperando en los pisos (verde) y en cooldown (rojo).

    Referencia de colores:
    - Verde   : Pasajero esperando o subiendo
    - Amarillo: Pasajero bajando
    - Rojo    : Pasajero en cooldown (esperando en el piso)
    - Morado  : Estado de error (no debería aparecer)
    """
    window.fill((250, 250, 255))  # Background color

    # Draw floor lines and labels
    for i in range(FLOORS):
        y = WINDOW_HEIGHT - (i + 1) * floor_height
        pygame.draw.line(window, (220, 220, 220), (0, y), (WINDOW_WIDTH, y))
        font = pygame.font.SysFont(None, 20)
        label = font.render(f'Floor {i}', True, (0, 0, 0))
        window.blit(label, (5, y + 5))

    # Draw elevators and passengers inside them
    for idx, (floor, passengers, _) in enumerate(elevators):
        x = 70 + idx * 100
        y = WINDOW_HEIGHT - (floor + 1) * floor_height
        pygame.draw.rect(window, (169, 169, 169), (x, y, 55, floor_height))  # Gray elevator box

        for j, pid in enumerate(passengers):
            person = people[pid]
            if person['graphic_state'] == 'elevator_up':
                color = (0, 255, 0)      # Green: riding up
            elif person['graphic_state'] == 'elevator_down':
                color = (255, 255, 0)    # Yellow: riding down
            else:
                color = (128, 0, 128)    # Purple: error state

            pygame.draw.circle(window, color, (x + 4 + j * 12, y + 25), 5)

    # Draw people waiting on floors and people on cooldown
    floor_positions = {f: {"waiting": 0, "inactive": 0} for f in range(FLOORS)}
    for p in people:
        floor = 0 if p['status'] == 'going_up' else p['destination']
        y_base = WINDOW_HEIGHT - (floor + 1) * floor_height + floor_height // 2

        if p['graphic_state'] == 'going_up' or p['graphic_state'] == 'ready_to_descend':
            x = 600 + floor_positions[floor]["waiting"] * 10
            pygame.draw.circle(window, (0, 255, 0), (x, y_base), 6)   # Green: waiting
            floor_positions[floor]["waiting"] += 1
        elif p['graphic_state'] == 'waiting':
            x = 600 + floor_positions[floor]["inactive"] * 10
            pygame.draw.circle(window, (255, 0, 0), (x, y_base + 10), 6)  # Red: on cooldown
            floor_positions[floor]["inactive"] += 1

    pygame.display.flip()


# ---------------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------------

# Load configuration from file
num_elevators, elev_capacity, total_people, cycle_people, floor_times = read_config_file(CONFIG_FILE)

# Initialize waiting list for each floor
people_waiting = [[] for _ in range(FLOORS)]

# Create elevators: [current_floor, passengers_list, semaphore]
elevators = [[0, [], threading.Semaphore(1)] for _ in range(num_elevators)]

# Create people with random destinations
people = []
for i in range(total_people):
    destination = random.randint(1, 10)
    people.append({
        "id": i,
        "status": "going_up",
        "destination": destination,
        "cooldown": 0,
        "graphic_state": "going_up"
    })
    people_waiting[0].append(i)

# Start one thread per elevator
threads = []
for i in range(num_elevators):
    t = threading.Thread(target=elevator_function, args=(i,))
    threads.append(t)
    t.start()

# Main Pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update_cooldowns()  # Update cooldown counters each frame
    draw()              # Render simulation state
    clock.tick(30)      # Cap at 30 FPS

pygame.quit()
# ---------------------------------------------------------------------------------
# END OF PROGRAM
# ---------------------------------------------------------------------------------