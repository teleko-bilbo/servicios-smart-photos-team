# Practica 2 - Parte MaaS


## Introduccion
MaaS, o Metal as a Service, es un modelo que permite a los usuarios administradores implementar y gestionar recursos de hardware físico de manera 
similar a cómo se gestionan los recursos en la nube. A través de interfaces de programación de aplicaciones (API) y herramientas de automatización, 
MaaS permite a los administradores de sistemas implementar y escalar servidores, redes y almacenamiento de forma rápida y eficiente. 

Esto simplifica la administración de centros de datos y facilita la asignación dinámica de recursos, reduciendo los costos asociados a la gestión del hardware. MaaS 
es especialmente útil en entornos de desarrollo, pruebas y producción que requieren escalabilidad en el uso de recursos físicos.

Durante esta práctica, se utilizará MaaS para cargar la configuración y recursos a los equipos Worker y controladores K8s.

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

Se edita el ficehro de configuración de PostgreSQL:

```bash
sudo nano pg_hba.conf
```

Al final del fichero, se añade lo siguiente:

```bash
host    userDB    user    0/0     md5
```

#### 7. Configurar usuario en MaaS e inicializar
Usamos `sudo maas init` (distinto al comando indicado en el tutorial, pues hemos descargado otra versión de MaaS).

```bash
sudo maas init
```

##### 7.1 Acceso de un usuario estándar

Durante la creación de un nuevo usuario, indicamos lo siguiente:
- **URL de Canonical RBAC:** no se indica nada pues no se usa.
- **Ruta de autenticación Candid:** no se indica nada pues no se usa.
- **Username:** usuario
- **Password:** 1234
- **Email:** fsanz003@ikasle.ehu.eus (podría ser otro, pero es importante no dejar vacío este campo).
- **SSH keys:** lo dejamos en blanco.

##### 7.2 Acceso como administrador

Para crear un usuario con privilegios de administrador, se indica lo siguiente:
- **URL de Canonical RBAC:** no se indica nada pues no se usa.
- **Ruta de autenticación Candid:** no se indica nada pues no se usa.
- **Username:** admin
- **Password:** admin
- **Email:** admin@maas.com (o el correo que prefieras, pero no dejes el campo vacío).
- **SSH keys:** lo dejamos en blanco, posteriormente se añade la clave SSH del administrador.

#### 8. Interfaz gráfica de MaaS:
Para acceder a la interfaz gráfica de MaaS y asi poder configurar el controladors, desde el navegador:

http://0.0.0.0:5240/MAAS


#### 9. Algunas otras instalaciones:
Se incluyen algunas herramientas que pueden ser de utilidad después.

Para poder ver la configuración de interfaces de red:
```bash
sudo apt install net-tools
```
Para utilizar Wireshark:
```bash
sudo apt install wireshark
```

#### 10. Configuración del controlador MaaS desde el GUI
Una vez accedemos desde el navegador al GUI de MaaS

##### 10.1 Iniciar sesión
Iniciamos sesión con las credenciales indicadas en el paso 7 del anterior apartado.

##### 10.2 Configuración de los DNS
Utilizaremos los servidores DNS de la universidad: 10.10.13.107 10.10.13.108

   ![DNS Configuration](Imagenes/MAASConfiguration_DNS.jpg)

##### 10.3 Imagen a cargar:
Indicamos la imagen que deseamos cargar: Ubuntu 22.04 LTS y arquitectura AMD64.

    ![Image Configuration](Imagenes\ConfigurationImages.jpg)

##### 10.4 Añadir la clave SSH al usuario MaaS:
Obtenemos la pareja de claves pública-privada e importamos la clave pública a MaaS. Para ello, primero la generamos:

```bash
ssh-keygen -t rsa -b 4096 -C "admin@maas.com"
```
Una vez se ejecuta el comando, se piden cumplimentar los siguientes campos:
- **file:** se indica el que proporciona por defecto `cat ~/.ssh/id_rsa`.

   ![Ejemplo generación de clave](Imagenes/Clave_ejemp.png)

A continuación, se copia la clabe pública generada:

```bash
cat ~/.ssh/id_rsa.pub
```

Y se añade al Maas User:
1. Inicia sesión en la interfaz web de MAAS.
2. Ve a **Username** (esquina superior derecha) > **Preferences**.
3. En la sección **SSH keys**, haz clic en **Add key**.
4. Pega tu clave pública SSH en el campo y guárdala.

##### 10.5 Configuración DHCP, VLAN y Subred

1. En **Networking** > **Subnets**:
   - Habilita el DHCP.
   - Crea la subred `192.168.1.0/24` con el gateway del equipo MAAS `192.168.1.1`.
   - Asigna a esta subred la VID (VLAN ID) `100` con el nombre `smartphotos`.

   A continuación, se muestran las imágenes con la configuración final:

   ![Networking Subnets](Imagenes/MAASConfiguration_NetworkingSubnets.jpg)

   ![Networking Summary](Imagenes/MAASConfiguration_SmartPhotosNetworkSummary.jpg)

##### 11 Configuración de Nodos PXE

1. Habilita el arranque/apagado remoto de máquinas VirtualBox mediante el script `vboxpower.py` del proyecto **vboxpower** (asegúrate de haber completado los pasos previos necesarios).
2. Arranca las máquinas para que las comisione MAAS.
3. Configura los webhooks correspondientes para que MAAS realice arranque/apagado automático.
4. Accede por SSH a los nodos y verifica:
   - Espacio en disco
   - Uso de CPU
   - Uso de RAM

   ![Arranque por red VM](Imagenes/MAAS_HardwareMachines.jpg)




