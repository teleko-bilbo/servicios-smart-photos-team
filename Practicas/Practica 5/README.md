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
Editar el servicio kuard de la práctica anterior para que sea de tipo LoadBalancer:
```bash
kubectl edit service kuard
```
Cambiar el tipo a LoadBalancer:
```bash
spec:
  type: LoadBalancer
```
Aplicar el manifiesto:
```bash
kubectl apply -f service.yaml
```
Verificar que el servicio tiene una IP externa asignada:
```bash
kubectl get svc kuard
```
La salida debería incluir algo como esto:
```bash
NAME    TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGE
kuard   LoadBalancer   10.152.183.104   192.168.1.195    8080:30706/TCP   5m
```
La columna EXTERNAL-IP muestra la IP asignada por MetalLB.
Acceder al servicio usando la IP externa en un navegador o con curl:
```bash
curl http://<EXTERNAL-IP>:8080
```
Con el buscador:
(Imágenes del resultado del buscador)
# 2.Ingress
--- (Completar)
Con el el controlador ingress-nginx desplegado, verificar que el controlador está corriendo y las etiquetas:
```bash
kubectl get pods -n ingress-nginx --show labels
```
--- (Completar)

Verificar la IP externa para compruebar que se asigna una IP al servicio ingress-nginx (Tomar nota de la IP externa para usarla más adelante):
```bash
kubectl get svc -n ingress-nginx # 192.168.1.196
```
Crear dos despliegues y servicios. Uno puede ser similar al de la práctica anterior.
Deployment y servicio del primer servicio (kuard)
Deployment y servicio del primer servicio (kuardgreen)

Editar el archivo /etc/hosts del cliente para asociar la IP externa del servicio ingress-nginx a dos nombres diferentes. Por ejemplo:
```bash
sudo nano /etc/hosts
```
Agregar estas líneas (external-ip-of-ingress-nginx = 192.168.1.196): 
```bash
<external-ip-of-ingress-nginx> kuard
<external-ip-of-ingress-nginx> kuardgreen
```
Crear un archivo ingress.yaml con la configuración para dirigir las solicitudes según el host:
```bash
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virtualhost
spec:
  rules:
  - host: "kuard"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kuard
            port:
              number: 8080
  - host: "kuardgreen"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kuardgreen
            port:
              number: 8080
```
Aplicar el manifiesto:
```bash
kubectl apply -f ingress.yaml
```
Desde el navegador web:
- Acceder a http://kuard para verificar que responde el servicio kuard.
- Acceder a http://kuardgreen para verificar que responde el servicio kuardgreen.
Refrescar la página varias veces y observar cómo las respuestas provienen de diferentes pods, lo que indica que el balanceo de carga funciona.
(Fotos del balanceo) 
