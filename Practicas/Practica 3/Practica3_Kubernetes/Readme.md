# Practica 3 - Container as a Service (CaaS) - Kubernetes


## Introduccion
A lo largo de esta practica, desplegaremos mediante Juju un cluster de Kubernetes sobre la arquitectura de red que hemos preparado durante las clases anteriores.
Habilitar un cluster de Kubernetes sobre nuestra arquitectura fisica nos permitira desplegar servicios y aplicaciones de forma sencilla y de forma simultanea y eficiente en distintas maquinas. 

Una vez desplegado el Cluster de Kubernetes, podremos gestionarlo mediante Juju. En particular, Juju nos permititrañ:
 - Desplegar nuevos servicios y sus aplicaciones.
 - Escalar: añadir y/o eliminar nuevas maquinas y unidades de forma sencilla.

Una vez desplegadas las maquinas y unidades, nistalaremos Helm y mediate su CLI, Longhorn. Longhorn nos permitirá añadir a nuestra nube de Kubernetes soporte de almacenamiento persistente. De esta forma, evitaremos que, aquella informacion que se deba guardar, se pierda al apagar el cluster.


## Instalación de un Cluster de Kubernetes de producción:
Para la instalacion del cluster de Kubernetes, primero crearemos un nuevo modelo, y luego ejecutaremos el siguiente comando:

```bash
juju add-model k8s maas-cloud
juju deploy charmed-kubernetes --overlay k8s-overlay.yaml
```

![cluster](imgs/1_1.png)


## Ajuste del Cluster mediante "k8s_overlay.yaml":
Como puede apreciarse en el comando anterior, se hace referenecia a un fichero "k8s_overlay.yaml". Este fichero nos permitirá ajustar el despliegue del cluster de Kubernetes, de la siguiente forma:
 - Crear solo 3 unidades Worker y elegir solo maquinas que tengan el tag "Worker" en MaaS.
 - No crear el balanceador de carga "Kubeapi-load-balancer".
 - Crear solo 1 unidad de cada "easyrsa", "etcd" y "kubernetes-control-plane", usando para  cada uno el tag correspondiente de la maquina. 

![cluster](imgs/1_2.png)


## Escalado horizontal del cluster:
Una vez que se ha desplegado el Cluster, se puede escalar este horizontalmente, añadiendo o quitando unidades e incluso desplegando nuevas maquinas con sus propias unidades. Esto, podremos hacerlo de varias maneras:

### Escalado horizontal añadiendo una maquina y luego sus unidades:
Podemos escalar el cluster ejecutando los siguientes comandos. En este caso, primero añadimos una maquina (seleccionando un equipo que tenga el tag "Worker") y luego añadimos a esta la unidad "Kubernetes-worker". En <machine-id> indicaremos el ID dado a la maquina

```bash
juju add-machine --constraints "tags=Worker"
juju status 
juju add-unit kubernetes-worker --to <machine-id>

```


### Escalado horizontal añadiendo unidades directamente a una maquina nueva:
Si la maquina no esta creada, podemos desplegar una nueva maquina y tambien añadir una unidad a esta (todo en un unico paso), mediante el siguiente comando.

```bash
juju add-unit kubernetes-worker
```


### Escalado horizontal añadiendo unidades directamente a una maquina ya desplegada:
Si la maquina ya esta creada, podemos añadir nuevas unidades a esta mediante el comando a continuacion

```bash
juju add-unit kubernetes-worker --to <machine-id>
```

### Eliminado de maquinas y unidades:
Finalmente, podremos eliminar aquelas maquinas / unidades que no necesitemos en nuestro cluster de Kubernetes. Para ello, usaremos los siguientes comandos:

Eliminar una unidad de una maquina: indicamos que servicio en <service-name> y el ID de la unidad en <unit-id>

```bash
juju remove-unit <service-name>/<unit-id>
#juju remove-unit kubernetes-worker/0
```

Eliminar una maquina: eliminamos una maquina completa, indicando el id de la maquina en <machine-id>

```bash
juju remove-machine <machine-id>
#juju remove-machine 1
```


## Instalacion del CLI y GUI de Kubectl:
Para poder instalar el CLI de Kubectl, debemos primero esperar a que se desplieguen completamente algunas unidades, como por ejemplo, "Kubernetes-control-plane". 

De esta maquina, obtendremos y copiaremos el fichero "config" de la siguiente manera:

```bash
sudo snap install kubectl --classic
kubectl version
mkdir ~/.kube
juju ssh kubernetes-control-plane/1 -- cat config > ~/.kube/config
```

El GUI se "instalara" haciendo un reenvio de puertos entre la maquina local y el servicio Kubernetes Dashboard, permitiendo asi el acceso desde fuera del cluster a un servicio que solo está en dicho cluster.

```bash
kubectl port-forward service/kubernetes-dashboard -n kubernetes-dashboard 8443:443
```


## Instalación de Helm:





## Instalación de Longhorn mediante Helm:






@izaballa010

![imagen](https://github.com/user-attachments/assets/81f843cb-fe3c-4ad4-a523-60babe733882)
![imagen](https://github.com/user-attachments/assets/cd04e414-6d7c-4724-8a73-3193ba8616df)
![imagen](https://github.com/user-attachments/assets/594f6029-48a2-492b-864e-5604504676c8)
![imagen](https://github.com/user-attachments/assets/0c39c8fa-f984-4adf-a2a9-6adc6fa88d75)
![imagen](https://github.com/user-attachments/assets/bf839db0-da72-487b-b34b-c0a45802c145)
![imagen](https://github.com/user-attachments/assets/ac2b3182-6325-4ad9-9d64-0098d973c15b)

```bash
juju staus
```
![imagen](https://github.com/user-attachments/assets/4721325e-9735-4227-b40d-d737f0a0672e)


```bash
juju add-unit kubernetes-worker
```
![imagen](https://github.com/user-attachments/assets/a9305db5-b99c-49a4-8834-e46819e204a2)


kubectl get all -A
