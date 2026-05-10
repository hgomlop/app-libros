# 📚 App Reporte de Libros

Aplicación web para registrar y gestionar tus lecturas anuales.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python + FastAPI |
| Base de datos | PostgreSQL 16 |
| Infraestructura | Docker + Docker Compose |

## Estructura del proyecto

```
proyecto/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   └── package.json
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── .env.example
    ├── db/
    │   └── init.sql
    └── routers/
        ├── auth.py
        └── books.py
```

## Arrancar el proyecto

```bash
# 1. Clona el repo y entra en él
git clone <tu-repo>
cd proyecto

# 2. Copia el fichero de variables de entorno del backend
cp backend/.env.example backend/.env
# Edita backend/.env y cambia SECRET_KEY por algo seguro

# 3. Levanta todos los contenedores
docker-compose up --build

# 4. Abre el navegador
# Frontend → http://localhost:5173
# API Docs → http://localhost:8000/docs
```

## Comandos útiles

```bash
# Ver logs de un servicio concreto
docker-compose logs -f backend

# Reiniciar solo el backend
docker-compose restart backend

# Parar todo
docker-compose down

# Parar todo y borrar la base de datos
docker-compose down -v

# Acceder a la shell de PostgreSQL
docker exec -it libros_postgres psql -U libros_user -d libros_db
```

## API Endpoints

La documentación interactiva (Swagger) está disponible en:
**http://localhost:8000/docs**

### Auth
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/register` | Crear cuenta |
| POST | `/api/auth/login` | Iniciar sesión |
| GET | `/api/auth/me` | Perfil del usuario actual |

### Libros
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/books/` | Todos los libros (filtros: status, year) |
| GET | `/api/books/current` | Lectura actual |
| GET | `/api/books/recent` | Últimas 5 lecturas finalizadas |
| GET | `/api/books/recommended` | Libros recomendados |
| POST | `/api/books/` | Añadir libro |
| PUT | `/api/books/{id}` | Editar libro |
| DELETE | `/api/books/{id}` | Eliminar libro |

## Estados de un libro

- `reading` → lectura actual
- `finished` → leído y con nota
- `wishlist` → lista de deseos / próximas lecturas
