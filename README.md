# Task Manager with Priorities

A command-line task management system that allows users to add tasks, mark them as completed, and filter them by priority or status. Tasks are persisted to a flat file for data retention between sessions.

## Features

- **Add tasks** with description, priority (high/medium/low), due date, and estimated hours
- **Mark tasks as completed** using task ID
- **View all tasks** sorted by priority
- **Filter tasks** by priority level or completion status
- **Persistent storage** using plain text file format
- **Input validation** with regular expressions for dates, hours, and priorities
- **Task summary** showing counts of pending and completed tasks

## Project Structure

```
gestor-tareas/
├── main.py              # Entry point: menu and user interaction
├── README.md            # This file
├── tareas/              # Package containing core logic
│   ├── __init__.py
│   ├── modelo.py        # Task data structure and constants
│   ├── validaciones.py  # Input validation with regex
│   ├── almacenamiento.py# File persistence (load/save)
│   └── operaciones.py   # Core operations: add, complete, filter
└── datos/
    └── tareas.txt       # Data repository (flat file)
```

## How to Run

Make sure you have Python 3 installed, then run:

```bash
python main.py
```

The program will display an interactive menu where you can manage your tasks.

### Sample Session

```
Se cargaron 2 tarea(s) desde el archivo.

========================================
     GESTOR DE TAREAS CON PRIORIDADES
========================================
  1) Agregar tarea
  2) Ver todas las tareas
  3) Completar una tarea
  4) Filtrar tareas
  5) Guardar y salir
Elegi una opcion (1-5): 2

=== Todas las tareas ===
  [X] #1  (alta )  vence 20/12/2026  8.5h  -> Estudiar para el examen final
  [ ] #2  (media)  vence 25/11/2026  4.0h  -> Preparar presentacion del proyecto

Resumen: 2 tarea(s) en total | 1 pendiente(s) | 1 completada(s).
```

## Technology Stack

- **Python 3** (standard library only)
- No external dependencies required

## Technical Highlights

This project demonstrates:

- **Modular design** with clear separation of concerns (data model, validation, storage, operations, UI)
- **Input validation** using Python regular expressions
- **File-based persistence** with pipe-delimited format
- **Error handling** for file I/O and user input
- **Functional programming** concepts (filtering, sorting with lambda functions)
- **Data structures** (dictionaries for tasks, lists for collections)

## Data Format

Each line in `datos/tareas.txt` represents a task with pipe-separated fields:

```
id|description|priority|due_date|estimated_hours|completed
```

Example:
```
1|Estudiar para el examen final|alta|20/12/2026|8.5|1
```

The `completed` field is `1` (True) or `0` (False).

## Academic Context

**University Project**  
Course: Programación II  
Institution: UAI (Universidad Abierta Interamericana)  
Faculty: Facultad de Tecnología Informática - Analista Programador  
Student: Candela Dolores Dengra

This project was developed as an integrative practical assignment (Trabajo Práctico Integrador) to demonstrate proficiency in Python programming, modular design, data validation, and file-based persistence.

---

## Versión en español

Sistema de línea de comandos para administrar una lista de tareas con prioridades. Permite agregar tareas, marcarlas como completadas y filtrarlas por prioridad o estado. Las tareas se guardan en un archivo plano para persistencia entre ejecuciones.

**Contexto académico:** Trabajo práctico integrador del curso de Programación II en la Universidad Abierta Interamericana (UAI), Facultad de Tecnología Informática.

**Cómo ejecutar:**
```bash
python main.py
```

**Tecnología:** Python 3 (solo biblioteca estándar, sin dependencias externas).
