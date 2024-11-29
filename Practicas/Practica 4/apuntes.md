# SERVICIOS EN KUBERNETES
## 2.1.PRINCIPIOS (Con los que trabajamos)
Inmutibilidad -> Trabajar con imágenes
Configuración declarativa -> Estado definido en fichero *.yanl
Self-healing (Auto-recuperación) -> Monitoreo constante del estado
Desacoplamiento -> Pods aislados
## 2.2.CLIENTE KUBECTL
Comando kubectl -> Se configura en ~/.kube/config (Determinar con que cluster Kubernetes se habla)
kubectl options -> Todas las opciones de comandos
## 2.3.ESPACIOS DE NOMBRES
El namespace agrupa todos los objetos del cluster.
```bash
kubect create namespace nombreNamespace
```
Indicar el namespace de trabajo:
```bash
kubect -n nombreNamespace
```
En el YAML para referenciar el namesapce a desplegar:
```bash
metadata:
  namespace: nombre
```
## 2.4.VERBOS
Acciones via API REST.
## 2.5.OPERACIONES
Consulta (get todo cholon|describe más legible):
```bash
kubectl get|describe <resource-name> <obj-name>
```
get -o wide -> Más info
describe -o yaml/json -> Pasar a un formato

Modificación
Modificar configuración del cluster:
```bash
kubectl apply -f myobj.yaml
```
## 2.6.ETIQUETAS
Formato clave/valor
```bash
kubectl label pods bar color=red` #Añadir etiqueta
kubectl label pods bar color- #Eliminar etiquetas
kubectl run ... --labels="ver=1,app=alpaca,env=prod"
```
De forma declarativa con YAML:
```bash
metadata:
  labels:
    app: kuard
    version: "2"
```
Replicaset con selectores para saber que gestionar:
```bash
# Forma tradicional
selector:
  app: alpaca
  ver: 1
```
O de forma más completa:
```bash
# Forma nueva (permite expresiones más complejas)
selector:
  matchLabels:
    app: alpaca
    matchExpressions:
      - {key: ver, operator: In, values: [1, 2]}
```
## 2.7.WORKLOADS
Aplicaciones que se ejecutan en Kubernetes: 
    Pods, ReplicaSet, Deployment, StatefulSet, DaemonSet, Job, CronJob
# 3.PODS
## 3.1.INTRODUCCIÓN
Grupo de contenedores:
 - Comparte:  IP, puertos, nombre del host, IPCs, etc.
 - Independiente: CPU, memoria, etc.
Máquinas == Nodos
Un pod solo puede estar en un nodo
Contenedores que tienen que ir en la misma máquina -> Mismo pod
## 3.2.PATRONES DE DISEÑO
Patrón sidecar: 
 - Añador HTTPS a un servicio legacy HTTP
 - Añadir configuración de sincronización
## 3.3.DESPLIEGUE
API Server (Coamndo) -> Fichero etcd -> Scheduler
YAML básico para desplegar un pod:
```bash
apiVersion: v1                # Versión de la API para el recurso Pod
kind: Pod                     # Tipo de recurso: Pod
metadata:                     # Metadatos del Pod
  name: kuard                 # Nombre del Pod
spec:                         # Especificación del Pod
  containers:                 # Lista de contenedores dentro del Pod
    - image: gcr.io/kuar-demo/kuard-amd64:blue # Imagen del contenedor
      name: kuard             # Nombre del contenedor
      ports:                  # Lista de puertos expuestos por el contenedor
        - containerPort: 8080 # Puerto expuesto por el contenedor dentro del Pod
          protocol: TCP       # Protocolo del puerto, en este caso TCP
```
Y para desplgar en el cluster:
```bash
kubectl apply -f kuard-pod.yaml
```
Eliminar pod del YAML:
```bash
kubectl delete pods/kuard
kubectl delete -f kuard-pod.yaml
```
Conectar al pod:
```bash
kubectl port-forward kuard 8080:8080 
kubectl exec -it kuard -- /bin/sh #Entrar al pod ssh
```
# 4.REPLICASET
Pods con varias réplicas -> Mantener un número de réplicas (pods) activos
## 4.1.CARACTEÍSTICAS
Un replicaset arranca 3 pods, y si se modifica la etiqueta de un pod -> Se pasan a 2 pods en el resplicaset y busca uno nuevo
Microservicios esclables y sin estado
## 4.2.YAML
```bash
apiVersion: apps/v1   # Versión de la API para el recurso ReplicaSet
kind: ReplicaSet      # Tipo de recurso: ReplicaSet
metadata:             # Metadatos del ReplicaSet
  name: kuard         # Nombre del ReplicaSet
spec:                 # Especificación del ReplicaSet
  replicas: 3         # Número deseado de réplicas (pods)
  selector:           # Selector para gestionar los pods de este ReplicaSet
    matchLabels:      # Define etiquetas que los pods deben tener para ser gestionados por este ReplicaSet
      app: kuard      # Etiqueta que deben tener los pods para ser gestionados por este ReplicaSet
  template:           # Template del pod, describe cómo serán los pods del ReplicaSet
    metadata:         # Metadatos del pod template
      labels:         # Etiquetas aplicadas a los pods creados por el ReplicaSet
        app: kuard    # Etiqueta utilizada para identificar los pods
    spec:             # Especificación del pod
      containers:     # Lista de contenedores dentro del pod
        - image: gcr.io/kuar-demo/kuard-amd64:blue # Imagen del contenedor
          name: kuard # Nombre del contenedor
          ports:      # Lista de puertos expuestos por el contenedor
            - containerPort: 8080 # Puerto expuesto por el contenedor dentro del pod
              protocol: TCP       # Protocolo del puerto, en este caso TCP
```
## 4.3.CLI
```bash
# Creación y consulta
kubectl apply -f kuard-rs.yaml
kubectl get all # Todas las características

# Escalado manual
kubectl scale replicasets kuard --replicas=4

# Eliminación
kubectl delete rs kuard # Elimina en cascada replicaset y pods
kubectl delete rs kuard --cascade=false # No elimina los pods
```
# 5.DEPLOYMENT
## 5.1.Características
Pods y ReplicaSets trbaja sobre imagen del contenedor que no cambia -> Con Deplyments se van deteniendo un porcentaje de pods y se van actualizando gradualmente para actualizar la aplicación (proprocionando siempre el servicio)
Deployments -> gestiona -> ReplicaSets -> gestiona -> Pods
## 5.2.YAML
```bash
apiVersion: apps/v1   # Versión de la API para el recurso Deployment
kind: Deployment      # Tipo de recurso: Deployment
metadata:             # Metadatos del Deployment
  name: kuard         # Nombre del Deployment
spec:                 # Especificación del Deployment
  replicas: 3         # Número deseado de réplicas (pods)
  selector:           # Selector para gestionar los pods de este Deployment
    matchLabels:      # Define etiquetas que los pods deben tener para ser gestionados por este Deployment
      app: kuard      # Etiqueta que deben tener los pods para ser gestionados por este Deployment
  template:           # Template del pod, describe cómo serán los pods del Deployment
    metadata:         # Metadatos del pod template
      labels:         # Etiquetas aplicadas a los pods creados por el Deployment
        app: kuard    # Etiqueta utilizada para identificar los pods
    spec:             # Especificación del pod
      containers:     # Lista de contenedores dentro del pod
        - image: gcr.io/kuar-demo/kuard-amd64:blue # Imagen del contenedor
          name: kuard # Nombre del contenedor
          ports:      # Lista de puertos expuestos por el contenedor
            - containerPort: 8080 # Puerto expuesto por el contenedor dentro del pod
              protocol: TCP       # Protocolo del puerto, en este caso TCP 
```
## 5.3.Rollout
RollingUpdate:
```bash
# Dentro de spec: strategy:
type: RollingUpdate
rollingUpdate:
  maxUnavailable: 1 # Pods (tb %) no disponibles durante rollout
  maxSurge: 1       # Pods (tb %) extra durante rollout 
```
Anotación de la actualización del Deplyment:
```bash
# Dentro de spec: template: metadata: annotations:
kubernetes.io/change-cause: "Update to green kuard"
```
Historial de versiones:
```bash
spec:
  revisionHistoryLimit: 10 # Podemos limitar el historial
```
## 5.4.CLI
```bash
# Creación y consulta
kubectl apply -f kuard-deployment.yaml
kubectl get deployments
kubectl get all
kubectl describe deployments kuard

# Escalado manual
kubectl scale replicasets kuard-d94fcfd7 --replicas=2 # ¿Qué ocurre?
kubectl scale deployments kuard --replicas=2 # ¿Qué ocurre?

# Rollout
kubectl rollout status deployments kuard
kubectl rollout pause deployments kuard
kubectl rollout resume deployments kuard
kubectl rollout history deployment kuard
kubectl rollout history deployment kuard --revision=2
kubectl rollout undo deployments kuard
kubectl rollout undo deployments kuard --to-revision=3

# Eliminación
kubectl delete deployments kuard
kubectl delete deployments kuard --cascade=false
```
# 6.Servicios
## 6.1.CARACTERÍSTICAS
Service -> Selector para identificar pods (IP fija -ClusterIP- y nombre DNS)
DNS ->kuard.dyd.svc.cluster.local:
    - kuard: nombre del servicio
    - dyd: espacio de nombres
    - svc: servicio (podría exponer otro tipo de objetos)
    - cluster.local: configurar si conectar varios cluste
## 6.2.YAML
```bash
apiVersion: v1       # Versión de la API
kind: Service        # Tipo de objeto
metadata:            # Metadatos del objeto
  name: kuard        # Nombre del servicio
spec:                # Especificaciones del servicio
  ports:             # Puertos del servicio
  - port: 8080       # Puerto expuesto
    targetPort: 8080 # Puerto al que se redirige
    protocol: TCP    # Protocolo utilizado
  selector:          # Selección de pods
    app: kuard       # Etiqueta para seleccionar los pods
  type: ClusterIP    # Tipo de servicio
```
## 6.3.CLI
```bash
# Creación
kubectl apply -f kuard-service.yaml   # Declarativa
kubectl expose deployment kuard       # Imperativa

# Consulta
kubectl get all
kubectl get deployments
kubectl describe deployment kuard
kubectl get endpoints kuard # Muestra los pos con IPs se balancea el servicio
kubectl describe endpoints kuard
kubectl get endpoints kuard --watch   # Ver cambios en tiempo real

# Acceso
kubectl port-forward pod/kuard-598d54d9c6-jsxtd 1234:8080 # Sin balanceo (conectar a un pod concreto)
ssh -N -L 1234:10.152.183.102:8080 ubuntu@192.168.13.30   # Balanceo por ClusterIP (cambia la ip del pod que responde) 10.152.183.102 -> IP del cluster

# Eliminación
kubectl delete service kuard
kubectl delete services,deployments -l app
```
## 6.4.NODEPORT
```bash
# Cambiar de ClusterIP a NodePort en spec: type:
kubectl edit service kuard

# Consultamos puerto asignado
kubectl describe service kuard

# Acceso a través del nuevo puerto en un nodo cualquiera
# http://192.168.13.26:32060
```
