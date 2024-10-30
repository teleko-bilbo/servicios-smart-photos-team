# Practica 2 - Parte MaaS


## Introduccion


## Red

### Equipos Workers:
Se configuran sin sistema operativo

Equipo Z34 --> Nombre MV: Worker_2_Z34 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> NOK (El PC no tiene un interfaz de red)

Equipo Z42 --> Nombre MV: Worker_3_Z42 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Equipo Z40 --> Nombre MV: Worker_4_Z40 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Equipo Z19 --> Nombre MV: Worker_5_Z19 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Equipo Z20 --> Nombre MV: Worker_6_Z20 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Equipo Z21 --> Nombre MV: Worker_7_Z21 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK

Equipo Z22 --> Nombre MV: Worker_8_Z22 --> RAM: 10240 MB, Procesadores x4, Memoria video 64 MB, Disco duro: 50 GB, Red: 1x NAT y 1x puente en Realtec --> Solo arranque red y sin SSOO. ----> OK


### Equipos K8s controladores todos sobre el equipo Z10:

Nombre MV: K8s_Etcd --> RAM: 8192 MB, Procesadores x2, Memoria Video 16 MB (por defecto), Disco duro: 25 GB, Red: 1x puente en Realtec --> Solo arranque red y sin SSOO. ---->

