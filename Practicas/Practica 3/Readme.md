# Practica 3 - Container as a Service (CaaS)


## Introduccion


## Instalación del cliente Juju
El cliente Juju se instalará en 3 equipos, unos por componente de este grupo. Para ello, se ejecutarán los siguientes comandos:

### 1º Instalacion de juju mediante Snap:
Instalamos Juju mediante el siguiente comando:

```bash
sudo snap install juju --classic
```

### 2º Registamos la nube:
Para registrar una nueva nube. debemos primero editar el fichero "maas-cloud.yml". En este fichero, en la linea de "endpoint", indicaremos la URL en la que escucha el controlador de MaaS: http://192.168.1.1:5240/MAAS
UNa vez realizada esta configuracion, ejecutamos el siguiente comando:

```bash
juju add-cloud maas-cloud maas-cloud.yaml
```

### 3º Generamos unas nuevas credenciales para la nube creada:
Debemos crear las credenciales para la nube recien creada. Despues de ejecutar ese comando, indicaremos "user", 



## Instalacion del Dashboard Juju