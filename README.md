# CosmoAgency

A test project built with **Django 5.2 + Python 3.12 + MySQL**,  
demonstrating the implementation of a Figma-based layout  
using **Bootstrap 5** and **Slick Slider** (Slider Syncing mode)  
with backend configuration via the Django admin panel.

The project delivers a webpage featuring a photo slider where:

- **Bootstrap 5** is used for layout and UI components.
- **Slick Slider** is implemented with synchronized main and navigation sliders.
- Images are managed through the **Django Admin** interface.
- Image storage is handled by **django-filer**.
- Slider item ordering is implemented via **drag & drop** using **django-admin-sortable2**.


## 🛠 Tech Stack

### Backend
- Python 3.12
- Django 5.2
- MySQL 9

### Frontend
- Bootstrap 5


## Prerequisites

Before getting started, make sure the following components are installed:

- Docker version 4.22 or later  
- Docker Compose version 2.20 or later


## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vladkachal/cosmo-agency.git
cd cosmo-agency
```

### 2. Configure environment variables

Copy `.env.template` to `.env`.

Edit the `.env` file and provide the required values for the following variables:

```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_PASSWORD=
DATABASE_ROOT_PASSWORD=
```

### 3. Build and run the application

Use Docker Compose to build and start the application:

```
export COMPOSE_FILE=./docker/compose.development.yaml
docker compose up --build
```

### 4. Create a superuser

To access the Django admin panel, create a superuser:

```
docker compose exec django python src/manage.py createsuperuser
```

### 5. Application access

Website: http://localhost:8000/
Django Admin: http://localhost:8000/admin/
