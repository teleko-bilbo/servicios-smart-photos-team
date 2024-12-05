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
NAME    TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
kuard   LoadBalancer   10.152.183.104   192.168.1.195    80:30706/TCP   5m
```
La columna EXTERNAL-IP mostrará la IP asignada por MetalLB.
Accede al servicio usando la IP externa en un navegador o con curl:
```bash
curl http://<EXTERNAL-IP>:8080
```
O con el buscador:
(Imágenes del resultado del buscador)
# 2.Ingress
---
Verificar la IP externa para compruebar que se asigna una IP al servicio ingress-nginx (Toma nota de la IP externa para usarla más adelante):
```bash
kubectl get svc -n ingress-nginx
```
Editar el archivo /etc/hosts del cliente para asociar la IP externa del servicio ingress-nginx a dos nombres diferentes. Por ejemplo:
```bash
sudo nano /etc/hosts
```
Agregar estas líneas:
```bash
<external-ip-of-ingress-nginx> app1.local
<external-ip-of-ingress-nginx> app2.local
```
Crea un archivo ingress.yaml con la configuración para dirigir las solicitudes según el host:
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

