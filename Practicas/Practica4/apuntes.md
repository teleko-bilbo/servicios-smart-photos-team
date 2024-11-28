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
