# Practica 2 - Parte MaaS


## Introduccion




## Red

A continuación se añade la configuración de los distintos equipos involucrados en la práctica

### Equipos Workers sobre equipos ZX:
Se configuran sin sistema operativo, esperando el arranque desde la red

Equipo Z34 --> Nombre MV: Worker_2_Z34 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec 
--> Solo arranque red y sin SSOO. ----> NOK (El PC no tiene un interfaz de red) --> Pasar a ordenador de Backup --> mac: 0800 275 123 B8 --> 169.254.156.155
ip 169.254.255.102 mask 255.255.0.0 gw: 169.254.255.100


Equipo Z42 --> Nombre MV: Worker_3_Z42 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK
--> mac: 0800 27A 8CD71 IP --> 169.254.155.130
ip 169.254.255.104 mask 255.255.0.0 gw: 169.254.255.100


Equipo Z40 --> Nombre MV: Worker_4_Z40 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK
--> mac: 0800 279 49200 ip--> 169.254.220.75
ip 169.254.255.103 mask 255.255.0.0 gw: 169.254.255.100


Equipo Z19 --> Nombre MV: Worker_5_Z19 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK
mac: 0800 270 6C00B ip: 169.254.201.218
ip 169.254.255.108 mask 255.255.0.0 gw: 169.254.255.100


Equipo Z20 --> Nombre MV: Worker_6_Z20 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK
mac: 0800 273 FE839 ip: 169.254.244.84
ip 169.254.255.107 mask 255.255.0.0 gw: 169.254.255.100


Equipo Z21 --> Nombre MV: Worker_7_Z21 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK
mac: 0800 270 6DAC2 ip:169.254.126.221
ip 169.254.255.106 mask 255.255.0.0 gw: 169.254.255.100


Equipo Z22 --> Nombre MV: Worker_8_Z22 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK
mac: 0800 27B 137D5 ip: 169.254.96.231
ip 169.254.255.105 mask 255.255.0.0 gw: 169.254.255.100


z10 ip 169.254.255.101 mask 255.255.0.0 gw: 169.254.255.100

### Equipos K8s controladores todos sobre el equipo Z10:

Nombre MV: K8s_Etcd --> RAM: 8192 MB, Procesadores x2, Memoria Video 16 MB (por defecto), Disco duro: 25 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Nombre MV: K8s_Easyrsa --> RAM: 4096 MB, Procesadores x1, Memoria Video 16 MB (por defecto), Disco duro: 25 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Nombre MV: K8s_Apisaver --> RAM: 8192 MB, Procesadores x2, Memoria Video 16 MB (por defecto), Disco duro: 25 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK


dar una etiqueta con el destino (k8master, juju controller,...), para que no elija aleatorismente el equipo, 


### Equipo con Maas Controller sobre Z9 (sobre una máquina virtual de Kubuntu):

A continuación, se añaden los pasos llevados a cabo para instalar y configurar el controlador MaaS:
Para la instalación, hemos seguido el tutorial incluido en los apuntes de la práctica

#### 1. Descarga de la versión 3.4 de MaaS

En nuestro caso, descargaremos la version 3.4de MaaS. Para ello:

```bash
sudo apt-add-repository ppa:maas/3.4
sudo apt update 
sudo apt upgrade
sudo apt-get -y install maas
```

#### 2. Desabilitar systemd-timesyncd

```bash
sudo systemctl disable --now systemd-timesyncd
```

#### 3. Configuración previa de variables de entorno:
Configuramos algunas variables de entorno que se usarán durante la instalación de PostgreSQL:

```bash
export DBUSER="user"
export DBPASS="1234"
export DBNAME="userDB"
```

#### 4. Instalación de PostgreSQL:

```bash
sudo apt install -y postgresql
```

#### 5. Configuración de postgreSQL (base de datos y usuario)
Creamos un rol y una base de datos.

```bash
sudo -i -u postgres psql -c "CREATE USER \"$DBUSER\" WITH ENCRYPTED PASSWORD '$DBPASS'"
sudo -i -u postgres createdb -O "$DBUSER" "$DBNAME"
```

#### 6. Modificación del fichero pg_hba.conf en /etc/postgresql/14/main/:
Al final del fichero, se añade lo siguiente:

```bash
host    userDB    user    0/0     md5
```

#### 7. Configurar usuario en MaaS e inicializar
Usamos sudo maas init (distinto al comando indicado en el tutorial, pues hemos descargado otra
versión de MaaS)

```bash
sudo maas init
```

Durante la creación de un nuevo usuario, indicamos lo siguiente:
- URL de Canonical RBAC: no se indica nada pues no se usa.
- Ruta de autencicación Candid: : no se indica nada pues no se usa.
- Username: usuario
- Password: 1234
- Email: fsanz003@ikasle.ehu.eus (podría ser otro, pero es importante no dejar vacio este campo).
- SSH keys: lo dejamos en blanco.

#### 8. Interfaz gráfica de MaaS:
Para acceder a la interfaz gráfica de MaaS y asi poder configurar el controladors, desde el navegador:

http://0.0.0.0:5240/MAAS


#### 9. Algunas otras instalaciones:
Se incluyen algunas herramientas que pueden ser de utilidad después-

Para poder ver la configuración de interfaces de red:
```bash
sudo apt install net-tools
```
Para utilizar Wireshark:
```bash
sudo apt install wireshark
```

#### 9. Configuración del controlador MaaS desde el GUI
Una vez accedemos desde el navegador al GUI de MaaS

##### 1. Iniciar sesión
Iniciamos sesión con las credenciales indicadas en el paso 7 del anterior apartado.

##### 2. Configuración de los DNS
Utilizaremos los servidores DNS de la universidad. Para saber cuales son, ejecutamos en el host
"ipconfig -all" y consultamos el apartado "Servidores DNS".

En este caso, indicaremos los de la universidad: 10.10.13.107 10.10.13.108

##### 3. Obtención de la clave ssh:
Obtenemos la pareja de claves pública-privada e importamos la clave pública a MaaS. Para ello, primero la generamos:
```bash
ssh-keygen -t rsa -b 4096 -C "fsanz003@ikasle.ehu.eus"
![Ejemplo generación de clave](Imagenes/Clave_ejemp.pngimagen.png)
```
La clave, salvo que se haya indicado otro directorio, se habrá creado en ~/.ssh/

##### 4. Imagen a cargar:
Indicamos la imagen que deseamos cargar: Ubuntu 22.04 lTS y arquitectura AMD64

##### 5. 


