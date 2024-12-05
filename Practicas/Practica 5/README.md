Practica 5 - Escalabilidad y Disponibilidad en Kubernetes

# Introduccion

Implementación de LoadBalancer para clusters Kubernetes bare metal. 
Instalación:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install -n metallb metallb bitnami/metallb --create-namespace # Para crear en una namespace
```
Común para todos el namespace. Aviso: Reservar/excluir rango de IPs del servidor DHCP del MaaS.
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
 - 192.168.13.120-192.168.13.150  # Cambia este rango según tu red
```
