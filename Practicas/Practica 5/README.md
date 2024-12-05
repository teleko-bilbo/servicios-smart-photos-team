Practica 5 - Escalabilidad y Disponibilidad en Kubernetes

# Introduccion

Implementación de LoadBalancer para clusters Kubernetes bare metal. 
Instalación:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install -n metallb metallb bitnami/metallb --create-namespace # Para crear en una namespace
```
Configurar MetalLB MetalLB necesita una configuración para definir el rango de IPs que se asigna (Reservar/excluir rango de IPs del servidor DHCP del MaaS). Crear el archivo de configuración metallb-config.yaml:
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
 - 192.168.13.120-192.168.13.150  # Cambia este rango según tu red
```

Aplicar la configuración:
```bash
kubectl apply -f metallb-config.yaml
```

Edita el servicio kuard de la práctica anterior para que sea de tipo LoadBalancer:
```bash
kubectl edit service kuard
```
