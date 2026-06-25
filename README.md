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

## 📖 Guía de Uso

La plataforma fue diseñada bajo el principio *Mobile-First*, asegurando una navegación intuitiva en smartphones y computadores.

### 1. Acceso y Registro Diferenciado
El usuario elige su rol (**Candidato** o **Empleador**) al momento de registrarse, lo que configura sus permisos y lo dirige a su panel correspondiente.


### 2. Flujo del Empleador (Microempresa)
* **Publicación de Oferta:** El formulario exige definir parámetros logísticos críticos de Aysén (modalidad de turno, ubicación rural/urbana y alojamiento).
* **Gestión de Postulantes:** Desde el panel privado, el empleador visualiza una tabla con todos los candidatos, sus estados de revisión y un botón para **descargar directamente el archivo PDF o Word** del currículum.


### 3. Flujo del Candidato (Buscador de Empleo)
* **Exploración y Postulación:** Al revisar los detalles de una vacante, el usuario encuentra al final un formulario para subir su archivo CV físico y aplicar con un solo clic.
* **Retiro de Postulación (Arrepentimiento):** Si el candidato desea cancelar su aplicación, la plataforma reemplaza el formulario por un botón rojo que permite eliminar inmediatamente su registro y documento de la vista del empleador.


---

## 📊 Datos Utilizados y Procesamiento

Dado que la plataforma funciona bajo un modelo de Contenido Generado por el Usuario (UGC), el sistema se validó y estructuró con los siguientes conjuntos de datos:

* **Catálogos Geográficos y Logísticos:** Variables estáticas de dominio regional para estructurar los filtros (turnos operativos, ruralidad, opciones de campamento). Respaldadas por reportes del [Observatorio Laboral de Aysén y SENCE](https://sence.gob.cl/personas/noticias/resultados-encuesta-nacional-de-demanda-laboral-enadel-2021-aysen).
* **Datos Sintéticos de Prueba (Mock Data):** Generación de perfiles ficticios, vacantes logísticas y carga de archivos a través del Django Admin para comprobar la latencia y la integridad referencial en producción.
* **Procesamiento de Datos:** La captura de información se realiza mediante peticiones HTTP. La transformación (sanitización de inputs) se maneja con `ModelForms`, y la persistencia segura la orquesta el ORM de Django, previniendo inyecciones SQL.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.x, Django
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Producción)
* **Despliegue:** Render (PaaS)

---

## ⚙️ Instalación y Ejecución Local

Sigue estos pasos para replicar el proyecto en tu entorno de desarrollo local:

1. **Clonar el repositorio**
```bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
   cd tu-repositorio
