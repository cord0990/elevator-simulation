<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,1a1a2e,2e4a7a&height=200&section=header&text=Elevator%20Simulation&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Sistema%20de%20ascensores%20concurrente%20con%20visualizaci%C3%B3n%20en%20tiempo%20real%20con%20Pygame&descAlignY=58&descSize=16" />

<br/>

![Python](https://img.shields.io/badge/Python-3.11-1a1a2e?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/GUI-Pygame-2e4a7a?style=for-the-badge&logo=python&logoColor=white)
![Threading](https://img.shields.io/badge/Concurrencia-Threading-6b7280?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Completado-2e4a7a?style=flat-square&labelColor=1a1a1a&color=2e4a7a)
![Universidad](https://img.shields.io/badge/PUCV-Hardware%20%26%20SO-3d3d3d?style=flat-square)

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎DESCRIPCIÓN

**Elevator Simulation** es una simulación concurrente de un sistema de ascensores para un edificio de 10 pisos. Desarrollado en **Python 3** con visualización gráfica en tiempo real usando **Pygame**, aplicando conceptos de **Sistemas Operativos** como hebras y semáforos para gestionar la sincronización de los ascensores y el flujo de pasajeros.

Cada ascensor se ejecuta en su propia hebra y coordina el acceso a los recursos compartidos mediante semáforos, evitando condiciones de carrera mientras transporta pasajeros a sus destinos.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎FUNCIONALIDADES

- **Gestión de múltiples ascensores** — cantidad configurable de ascensores ejecutándose de forma concurrente en hebras independientes.
- **Sincronización con semáforos** — evita condiciones de carrera cuando múltiples ascensores acceden a los datos compartidos de los pasajeros.
- **Generación aleatoria de pasajeros** — los pasajeros reciben pisos de destino aleatorios en tiempo de ejecución.
- **Sistema de cooldown** — los pasajeros esperan en su piso antes de regresar a la planta baja.
- **Visualización en tiempo real** — ventana Pygame en vivo que muestra ascensores, pasajeros y el estado de los pisos con colores identificadores.
- **Configuración por archivo** — todos los parámetros de la simulación se cargan desde un archivo `.txt` externo.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎TECNOLOGÍAS

| Tecnología | Uso |
|---|---|
| ![](https://img.shields.io/badge/Python%203-1a1a2e?style=flat-square&logo=python&logoColor=white) | Lenguaje principal |
| ![](https://img.shields.io/badge/Pygame-2e4a7a?style=flat-square&logo=python&logoColor=white) | Visualización gráfica en tiempo real |
| ![](https://img.shields.io/badge/Threading-6b7280?style=flat-square) | Ejecución concurrente de ascensores |
| ![](https://img.shields.io/badge/Semáforos-1a1a2e?style=flat-square) | Sincronización de recursos compartidos |
| ![](https://img.shields.io/badge/Archivo%20E%2FS-2e4a7a?style=flat-square) | Carga de parámetros desde .txt |

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎VISTA PREVIA

| Estado inicial | Ascensores subiendo |
|---|---|
| ![Inicial](screenshots/01_initial_state.png) | ![Subiendo](screenshots/02_elevators_ascending.png) |

| Pasajeros bajando | Simulación en curso |
|---|---|
| ![Bajando](screenshots/03_passengers_descending.png) | ![EnCurso](screenshots/04_mid_simulation.png) |

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎LEYENDA DE COLORES

| Color | Significado |
|---|---|
| 🟢 Verde | Pasajero esperando el ascensor / subiendo |
| 🟡 Amarillo | Pasajero bajando |
| 🔴 Rojo | Pasajero en cooldown (esperando en el piso) |

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎ESTRUCTURA DEL PROYECTO

```
elevator-simulation/
├── main.py                  # Lógica principal de la simulación
├── datosascensores.txt      # Archivo de configuración de entrada
├── .gitignore
├── LICENSE
└── README.md
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎ARCHIVO DE CONFIGURACIÓN

Edita `datosascensores.txt` con los parámetros de tu simulación:

```
2       ← Cantidad de ascensores
5       ← Capacidad del ascensor (máximo de pasajeros)
20      ← Total de personas
5       ← Personas generadas por ciclo
1       ← Tiempo en piso 1
2       ← Tiempo en piso 2
3       ← Tiempo en piso 3
4       ← Tiempo en piso 4
5       ← Tiempo en piso 5
6       ← Tiempo en piso 6
7       ← Tiempo en piso 7
8       ← Tiempo en piso 8
9       ← Tiempo en piso 9
10      ← Tiempo en piso 10
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎REQUISITOS

- **Python 3.11** — [Descargar](https://www.python.org/downloads/release/python-3119/) ⚠️ Python 3.12+ aún no es compatible con Pygame
- Librería **Pygame**

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎CÓMO EJECUTAR

**1. Instalar dependencias**
```bash
pip install pygame
```

**2. Ejecutar la simulación**

Linux / macOS:
```bash
python main.py
```
Windows:
```bash
py -3.11 main.py
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎CONTEXTO ACADÉMICO

Proyecto desarrollado para el curso **Hardware y Sistemas Operativos** -INF2322- en la [Pontificia Universidad Católica de Valparaíso (PUCV)](https://www.pucv.cl), 1er semestre de Ingeniería en Informática durante el 2024.

Conceptos aplicados: programación concurrente, manejo de hebras, sincronización con semáforos, simulación gráfica en tiempo real.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎AUTOR

<div align="center">

[![cord0990](https://img.shields.io/badge/@cord0990-1a1a2e?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cord0990)

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,1a1a2e,2e4a7a&height=100&section=footer" />
