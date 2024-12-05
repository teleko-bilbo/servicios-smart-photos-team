# Practica 5 - Escalabilidad y Disponibilidad en Kubernetes
# 1. LoadBlancer
Implementación de LoadBalancer para clusters Kubernetes bare metal. 
Instalación:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install -n metallb metallb bitnami/metallb --create-namespace # Para crear en una namespace
```
Configurar MetalLB -> Se necesita una configuración para definir el rango de IPs que se asigna (Reservar/excluir rango de IPs del servidor DHCP del MaaS). Crear el archivo de configuración metallb.yaml:
YAML (Común para todos el namespace):
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
 - 192.168.1.195-192.168.1.205  # Cambia este rango según tu red
```
Aplicar la configuración:
```bash
kubectl apply -f metallb.yaml
```
Edita el servicio kuard de la práctica anterior para que sea de tipo LoadBalancer:
```bash
kubectl edit service kuard
```
Cambia el tipo a LoadBalancer:
```bash
spec:
  type: LoadBalancer
```
Aplica el manifiesto:
```bash
kubectl apply -f service.yaml
```
Verifica que el servicio tiene una IP externa asignada:
```bash
kubectl get svc kuard
```
La salida debería incluir algo como esto:
```bash
NAME    TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
kuard   LoadBalancer   10.152.183.104   192.168.1.195    80:30706/TCP   5m
```
La columna EXTERNAL-IP mostrará la IP asignada por MetalLB.
Accede al servicio usando la IP externa en un navegador o con curl:
```bash
curl http://<EXTERNAL-IP>:8080
```
Para verificar el balanceo de carga:
- Escala el despliegue de kuard a múltiples réplicas:
```bash
kubectl scale deployment kuard --replicas=3
```
- Realiza múltiples solicitudes al servicio y observa cómo las solicitudes se distribuyen entre las réplicas. Esto puede hacerse con un script o herramientas como curl.
```bash
while true; do curl http://<EXTERNAL-IP>; sleep 1; done
```
Cada respuesta debería provenir de diferentes pods, indicando que el balanceo está funcionando.

