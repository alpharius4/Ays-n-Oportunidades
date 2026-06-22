# 🏔️ Aysén Oportunidades

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap_5-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

Plataforma web de intermediación laboral diseñada específicamente para resolver el "caos de datos" y la fragmentación del mercado laboral en la Región de Aysén. El sistema estandariza la oferta de las microempresas e incorpora variables de logística extrema (sistemas de turnos, aislamiento rural y movilización) para facilitar la conexión entre empleadores y trabajadores locales.

---

## 🚀 Características Principales

El sistema está construido bajo una arquitectura monolítica MVT (Modelo-Vista-Template) e incluye funcionalidades divididas por roles:

### Para el Empleador (Empresas)
* **Gestión de Ofertas (CRUD):** Publicación parametrizada exigiendo campos críticos regionales (sistemas de turno, ruralidad, alojamiento).
* **Dashboard Privado:** Panel de control para visualizar y administrar el estado de las vacantes activas o cerradas.
* **Revisión de Candidatos:** Recepción centralizada de postulaciones y botón de descarga directa de archivos Currículum Vitae (PDF/Word).

### Para el Candidato (Buscadores de empleo)
* **Motor de Búsqueda Local:** Exploración del mercado laboral utilizando filtros geográficos y logísticos.
* **Postulación Ágil:** Carga directa de documentos (CV) a través de formularios con codificación `multipart/form-data`.
* **Retiro de Postulación:** Opción de arrepentimiento para desvincular el perfil y eliminar el archivo enviado a una vacante.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.x, Django
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Diseño Mobile-First)
* **Base de Datos:** SQLite (Entorno de Desarrollo) / PostgreSQL (Entorno de Producción)
* **Despliegue:** Render (PaaS)

---

## ⚙️ Instalación y Ejecución Local

Sigue estos pasos para replicar el proyecto en tu entorno de desarrollo local:

1. **Clonar el repositorio**
```bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
   cd tu-repositorio
