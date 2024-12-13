# Practica 5 - Escalabilidad y Disponibilidad en Kubernetes

# 1. LoadBlancer
Debemos implementar un balanceador de carga bare metal para nuestro clusters de Kubernetes. 

La instalacion la hacemos mediante la ejecucion de los siguientes comandos. Primero añadimos un nuevo repositorio de helm y luego instalamos metallb creando un namespace propio: 

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami # añade un nuevo repositoio de helm
helm repo update
helm install -n metallb metallb bitnami/metallb --create-namespace # Para crear en una namespace 
```

Una vez instalado metallb, se necesita configurarlo para definir el rango de IPs que entregará a los servicios. Se usara un rango que excluya los rangos de direcciones IP que ya han sido usadas. Para eso creamos un ficheo "metallb.yaml", con el siguiente contenido:

```bash
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb
spec:
  ipAddressPools:
  - metallbpool
---
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: metallbpool
  namespace: metallb
spec:
  addresses:
  - 192.168.1.195-192.168.1.205
```

Aplicamos la configuración:
```bash
kubectl apply -f metallb.yaml
```

![Foto2](imgs/2.png)

Ahora editamos el servicio kuard de la práctica anterior para que sea de tipo LoadBalancer. Para eso, usaremos un fichero .yaml en el que se indica tipo como LoadBalancer:

```bash
apiVersion: v1       # Versión de la API
kind: Service        # Tipo de objeto
metadata:    
  namespace: dydvictor       # Metadatos del objeto
  name: kuardgreen        # Nombre del servicio
spec:                # Especificaciones del servicio
  ports:             # Puertos del servicio
  - port: 8080       # Puerto expuesto
    targetPort: 8080 # Puerto al que se redirige
    protocol: TCP    # Protocolo utilizado
  selector:          # Selección de pods
    app: kuard       # Etiqueta para seleccionar los pods
  type: LoadBalancer    # Tipo de servicio
```
Aplicamos los cambios:
```bash
kubectl apply -f service.yaml
```

Para comprobar los cambios, verificamos que el servicio tiene una IP externa asignada usando el siguiente comando:

```bash
kubectl get all -o wide
```

![Foto2](imgs/3.png)

La columna EXTERNAL-IP muestra la IP asignada por MetalLB. Vemos que es una IP dentro del rango que nosotros le hemos indicado para que entregue, y que no interfiere con el rango de direcciones ya asignadas a otros equipos.

Accedemos al servicio usando la IP externa en un navegador o con curl:

```bash
curl http://<EXTERNAL-IP>:8080
```

Si accedemos repetidamente, veremos que cambia la direccion IP del equipo que sirve contenido, siendo una de las 3 IPs que tiene cada uno de los PODs desplegados.

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
