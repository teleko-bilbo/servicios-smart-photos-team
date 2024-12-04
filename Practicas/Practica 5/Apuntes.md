# 2.Balanceo de Servicios
# 2.1.Fundamentos
Balanceador L4 -> Ejemplo NAT
# 2.2.LoadBalancer
Servicio ClusterIP -> Desde dentro del cluster Kubernetes
Servicio NodePort -> A través de un equipo (si falla bye bye)
Servicio LoadBalancer -> Balanceador de carga externo 
# 2.3.MetalLB
Implementación de LoadBalancer para clusters Kubernetes bare metal
Instalación:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install -n metallb metallb bitnami/metallb --create-namespace # Para crear en una namespace
```

Común para todos el namespace.
Aviso: Reservar/excluir rango de IPs del servidor DHCP del MaaS.

 YAML:
 ```bash
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb
spec:
  ipAddressPools:
  - metallbpool
--- # Dos YAML concatenados
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: metallbpool
  namespace: metallb
spec:
  addresses:
  - 192.168.13.120-192.168.13.150
```

# 2.4.Ingress
Charmed Kubernetes instala ingress-nginx-kubernetes-worker (necesario exponerlo) -> DemonSet (1 pod por nodo) -> Ya instalado

Usar /etc/hosts, para asignar la IP del LoadBalancer con varios nombres.

Ejemplo Ingress para dos virtual hosts:
```bash
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virtualhost
spec:
  rules:
  - host: "alpaca.dyd.eus"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: alpaca
            port:
              number: 80
  - host: "bandicoot.dyd.eus"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: bandicoot
            port:
              number: 80
```
# 3.Escalado de Servicios
# 3.1.Fundamentos
Kubernetes -> Escalado horizontal
Shared Service -> Dividir la base de datos en trozitos
# 3.2.Horizontal Pod Autoscaling (HPA)
Horizontal -> Añadir más pods
Pod -> Escalado de los pods (Escalado de nodos del cluster lo hace Juju)
Autoscaling -> Escalado automático según CPU, memoria o métrica propia

metrics-server (incluido con charmed kubernetes) y especificación de recursos del contenedor:
```bash
resources:
  requests:
    cpu: "100m"       # 100 millicores (0.1 CPU)
    memory: "128Mi"   # 128 MiB de memoria
  limits: # Contenedor no crece más de estos límite
    cpu: "500m"       # 500 millicores (0.5 CPU) # Si se pasa, pausa el contenedor y carga más tarde
    memory: "512Mi"   # 512 MiB de memoria # Si se pasa, se lo carga y vuelve a crear
```

1 ubidad CPU = 1 core / 1 vCPU / 1 hyper-thread
0.5 = 500m = media unidad de CPU (m="milicpu")

CLI:
```bash
# Autoescalar entre 2 y 10 réplicas con un umbral de CPU del 80%
kubectl autoscale deployment alpaca --min=2 --max=10 --cpu-percent=80 # 

# Consultar uso de recursos de los pods
kubectl top pod -l app=alpaca

# Consultar estado del HPA
kubectl get hpa alpaca

# Conectarme a un pod y cargar su CPU
kubectl exec -it pod/alpaca-56bfbd8956-v89ww -- /bin/sh
# Cargar CPU con herramienta stress, bucle espera activa, etc.
```
# 4.Bases de datos
# 4.1.Fundamentos escalado
Vertical Shards -> Separar por columnas
Horizontal Shards -> Separar por filas

![imagen](https://github.com/user-attachments/assets/3c39ef6a-0218-48b4-816d-d4292f932f82)
# 4.2.Opciones
Para escabilidad y sharding -> Para el caso de MySQL puede emplearse Vitess

![imagen](https://github.com/user-attachments/assets/86dfc2dc-d06f-431c-a4cc-35bfce203c80)

Bases de datos NoSQL -> MongoDB o Apache Cassandra

![imagen](https://github.com/user-attachments/assets/8969d0d2-37a7-481d-860e-7454f931c268)
![imagen](https://github.com/user-attachments/assets/d1899608-30b4-4576-bdff-bc36b4237115)

# 4.3.Volúmenes de almacenamiento
Tipos de volúmenes:
- emptyDir: permite compartir entre contenedores de un pod, pero no sobrevive al pod
- hostPath: monta un directorio del nodo en el pod, para casos muy concretos (evitar)
- configMap: el objeto ConfigMap permite guardar pares clave-valor de forma persistente
    - Posibilidad de montarlo como volumen: ficheros=claves, contenidos=valores
- persistentVolumeClaim: se puede pedir tamaño y modo de acceso
    - Usando Storage Classes se pueden aprovisionar PersistentVolumes (PV) automáticamente

YAML:
```bash
# Primero crear el PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: example-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

```bash
# CLI
kubectl get pv
kubectl get pvc
```

```bash
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: storage
  volumes:
    - name: storage
      persistentVolumeClaim:
        claimName: example-pvc
```



