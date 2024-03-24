# Agrovar Repository

![Agroestim Team Asset](/assets/agrovar-brand-product.png "Agroestim Team")

## Descripción

**Agrovar Repository** pretende ser una herramienta publica que permita a todos los productores agropecuarios, consultores y cientificos, analizar y consultar información acerca de los principales cultivos de interes y permitir comparar entre diferentes conjuntos de datos de forma sencilla y eficiente.

Este proyecto trata de una pieza fundamental de la herramienta consistiendo en una interfaz de aplicación o API; que permite conectar los servicios de control y almacenamiento con los clientes. De esta forma, los clientes podrán ingresar a una aplicación web mediante la cual podrán visualizar e interactuar con la herramienta.

- [Docs en-US version](/README_en.md "English markdown version")

- [Docs es-AR version](/README.md "Spanish markdown version")

## Tabla de contenidos

- [Status del proyecto](#status-del-proyecto)
- [Usando Agrovar](#usando-agrovar)
- [Acerca del proyecto](#acerca-del-proyecto)
  - [Construccion del proyecto](#construccion-del-proyecto)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Configuracion del proyecto](#configuracion-del-proyecto)
  - [Despliegue en local](#despliegue-en-local)

## Status del proyecto

Hasta el momento de la fecha, el proyecto se encuentra aún en desarrollo y pretende continuar con el lanzamiento periodico de nuevas versiones preliminares del software, que integren caracteristicas mejoradas y correciones pertinentes; conciderando también que tales lanzamientos pueden tener cambios drasticos, bugs y/o errores.

> [!NOTE]
> Si quieres participar en el desarrollo de nuestra herramienta puedes consultar en: ["Como colaborar 🧑‍💻"](https://github.com/Agroestim/agrovar-api-microservice "TODO")

## Usando Agrovar

Para utilizar la herramienta en entornos de desarrollo, es necesario tener acceso al contenedor de docker pertinente, actualizado a la ultima version estable disponible y desplegarlo localmente con el resto de los microservicios especificados en el fichero **docker-compose.dev.yml**. De esta forma, accediando al ["Dashboard de Django"](https://localhost/admin) — usando las credenciales correspondientes para su usuario — podrán interactuar con la herramienta de forma directa.

## Acerca del proyecto

### Construccion del proyecto

> [!IMPORTANT]
> Uno de los requisitos indispensables del proyecto es tener instalado el paquete virtualenv de Python.

El primer paso para construir el proyecto es necesario descargar el repositorio de Github usando Git e instalar las dependencias utilizando un entorno virtual como lo es virtualenv.

```powershell
  PS> git clone https://github.com/Agroestim/agrovar-api-microservice

  PS> cd agrovar-api-microservice

  PS> python -m venv venv

  PS> ./venv/bin/activate # Only in UNIX

  PS> ./venv/Scripts/Activate.ps1 # Only in Windows

  PS> python install -r requirements.txt
```

Una vez instalada las dependencias, ya puedes empezar a desarrollar tu codigo y/o desplegar snapshots locales.

### Estructura del proyecto

<!-- NOTE: Completar el titulo "Estructura del proyecto" -->

### Configuracion del proyecto

<!-- NOTE: Completar el titulo "Configurar proyecto" -->

### Despliegue en local

<!-- NOTE: Completar el titulo "Despliegue local" -->
