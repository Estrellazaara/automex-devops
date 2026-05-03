# AutoMex - Plataforma de microservicios para agencia automotriz

# AutoMex DevOps

Proyecto integrador DevOps basado en microservicios para una agencia automotriz llamada **AutoMex**. La solución implementa contenedores Docker, Kubernetes, Helm, GitHub Actions, Prometheus, Grafana y una preparación para despliegue en Azure Kubernetes Service (AKS).

---

## 1. Descripción del proyecto

AutoMex es una plataforma simulada para una agencia automotriz que necesita administrar diferentes áreas funcionales mediante microservicios. El sistema permite consultar el catálogo de autos, gestionar citas de prueba de manejo y revisar el inventario disponible por almacén.

El objetivo principal del proyecto es demostrar una entrega de software moderna usando prácticas DevOps:

- Desarrollo de microservicios.
- Empaquetado en contenedores Docker.
- Despliegue en Kubernetes.
- Instalación y actualización con Helm.
- Automatización con GitHub Actions.
- Monitoreo con Prometheus y Grafana.
- Preparación para despliegue en Azure AKS.

---

## 2. Caso de estudio

El caso seleccionado es una agencia automotriz. Esta empresa necesita una solución que permita administrar autos disponibles, citas de clientes y control de inventario. Para evitar una aplicación monolítica difícil de mantener, la solución se organizó en tres microservicios independientes.

### Requerimientos funcionales

| Requerimiento | Descripción |
|---|---|
| Consulta de catálogo | Permitir consultar autos disponibles, detalle de autos y unidades disponibles. |
| Gestión de citas | Permitir consultar citas de prueba de manejo y registrar nuevas citas. |
| Control de inventario | Permitir consultar stock por modelo, almacén y disponibilidad. |
| Verificación de salud | Cada servicio debe exponer un endpoint `/health`. |
| Métricas | Cada servicio debe exponer `/metrics` para monitoreo con Prometheus. |

### Requerimientos no funcionales

| Requerimiento | Descripción |
|---|---|
| Escalabilidad | Kubernetes debe permitir aumentar réplicas de cada microservicio. |
| Disponibilidad | Los servicios deben ejecutarse con más de una réplica. |
| Automatización | GitHub Actions debe validar el código y el empaquetado. |
| Portabilidad | La solución debe poder ejecutarse en Minikube y prepararse para AKS. |
| Observabilidad | Prometheus y Grafana deben permitir observar el comportamiento de los servicios. |

---

## 3. Microservicios

| Microservicio | Puerto | Función principal |
|---|---:|---|
| `catalog-service` | 5001 | Consulta de catálogo de autos. |
| `appointments-service` | 5000 | Gestión de citas de prueba de manejo. |
| `inventory-service` | 5000 | Consulta de inventario por almacén. |

Cada microservicio expone:

- `/health` para validaciones de salud en Kubernetes.
- `/metrics` para recolección de métricas con Prometheus.

---

## 4. Tecnologías utilizadas

- Python 3.11
- Flask
- Docker
- Kubernetes
- Minikube
- Helm
- GitHub Actions
- Prometheus
- Grafana
- Azure CLI
- Azure Container Registry
- Azure Kubernetes Service
- PlantUML

---

## 5. Estructura del repositorio

```text
automex-devops/
├── services/
│   ├── catalog-service/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── appointments-service/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── inventory-service/
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
├── k8s/
│   ├── 00-namespace.yaml
│   ├── 01-catalog-deployment.yaml
│   ├── 02-appointments-deployment.yaml
│   └── 03-inventory-deployment.yaml
├── helm/
│   └── automex/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-aks.yaml
│       └── templates/
├── monitoring/
│   └── servicemonitor-automex.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
└── docs/
    ├── capturas/
    └── diagramas/
```

---

## 6. Ejecución local con Docker

### Construir imágenes

```bash
cd services/catalog-service
docker build -t automex/catalog-service:1.0 .

cd ../appointments-service
docker build -t automex/appointments-service:1.0 .

cd ../inventory-service
docker build -t automex/inventory-service:1.0 .
```

### Ejecutar contenedores

```bash
docker run -d -p 5001:5001 --name catalog-test automex/catalog-service:1.0
docker run -d -p 5002:5000 --name appointments-test automex/appointments-service:1.0
docker run -d -p 5003:5000 --name inventory-test automex/inventory-service:1.0
```

### Probar servicios

```text
http://localhost:5001/autos
http://localhost:5002/citas
http://localhost:5003/inventario
```

---

## 7. Despliegue en Kubernetes con Minikube

### Iniciar Minikube

```bash
minikube start --driver=docker
```

### Cargar imágenes en Minikube

```bash
minikube image load automex/catalog-service:1.0
minikube image load automex/appointments-service:1.0
minikube image load automex/inventory-service:1.0
```

### Desplegar con manifiestos YAML

```bash
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-catalog-deployment.yaml
kubectl apply -f k8s/02-appointments-deployment.yaml
kubectl apply -f k8s/03-inventory-deployment.yaml
```

### Verificar recursos

```bash
kubectl get all -n automex
```

---

## 8. Despliegue con Helm

El proyecto incluye un Helm Chart en `helm/automex`.

### Validar el Chart

```bash
helm lint ./helm/automex
```

### Instalar la aplicación

```bash
helm install automex ./helm/automex --namespace automex --create-namespace
```

### Actualizar la aplicación

```bash
helm upgrade automex ./helm/automex --namespace automex
```

### Ver historial de versiones

```bash
helm history automex -n automex
```

---

## 9. Acceso a los servicios desplegados en Kubernetes

```bash
kubectl port-forward -n automex service/catalog-service 8001:5001 &
kubectl port-forward -n automex service/appointments-service 8002:5000 &
kubectl port-forward -n automex service/inventory-service 8003:5000 &
```

URLs:

```text
http://localhost:8001/autos
http://localhost:8002/citas
http://localhost:8003/inventario
```

---

## 10. CI/CD con GitHub Actions

El pipeline se encuentra en:

```text
.github/workflows/ci.yml
```

El flujo automatizado ejecuta:

1. Lint del código Python.
2. Construcción de imágenes Docker.
3. Pruebas de endpoints `/health`.
4. Validación del Helm Chart.
5. Validación de manifiestos Kubernetes.

El pipeline se ejecuta automáticamente con cada `push` a la rama `main`.

---

## 11. Monitoreo con Prometheus y Grafana

El monitoreo se implementó con `kube-prometheus-stack`.

### Componentes utilizados

- Prometheus
- Grafana
- Alertmanager
- kube-state-metrics
- node-exporter
- ServiceMonitor

### Ver pods de monitoreo

```bash
kubectl get pods -n monitoring
```

### Acceder a Grafana

```bash
kubectl port-forward -n monitoring service/monitoring-grafana 3000:80
```

URL:

```text
http://localhost:3000
```

Credenciales usadas en el laboratorio:

```text
Usuario: admin
Password: admin123
```

### Acceder a Prometheus

```bash
kubectl port-forward -n monitoring service/monitoring-kube-prometheus-prometheus 9090:9090
```

URL:

```text
http://localhost:9090
```

### Métrica principal usada como evidencia

```text
flask_http_request_total
```

---

## 12. Preparación para Azure AKS

Para cumplir con el requisito de servicio administrado de Kubernetes, se seleccionó **Azure Kubernetes Service (AKS)**.

El flujo preparado para AKS es:

1. Crear un Resource Group.
2. Crear Azure Container Registry.
3. Publicar imágenes Docker en ACR.
4. Crear clúster AKS.
5. Conectar `kubectl` con `az aks get-credentials`.
6. Desplegar AutoMex con Helm usando `values-aks.yaml`.

Durante la prueba con Azure for Students, la creación del clúster AKS fue limitada por cuotas de vCPU de la suscripción. Por esta razón, la implementación funcional se validó en Minikube, manteniendo una arquitectura compatible con Kubernetes y lista para migrarse a AKS cuando exista cuota disponible.

---

## 13. Endpoints principales

### catalog-service

```text
GET /
GET /health
GET /metrics
GET /autos
GET /autos/{id}
GET /autos/disponibles
```

### appointments-service

```text
GET /
GET /health
GET /metrics
GET /citas
GET /citas/{id}
POST /citas
```

### inventory-service

```text
GET /
GET /health
GET /metrics
GET /inventario
GET /inventario/{auto_id}
GET /inventario/almacen/{almacen}
GET /inventario/disponibles
```

---

## 14. Diagramas

Los diagramas del proyecto se encuentran en:

```text
docs/diagramas/
```

Se incluyen diagramas de:

- Arquitectura general.
- Despliegue en Kubernetes / AKS.
- Pipeline CI/CD.
- Monitoreo con Prometheus y Grafana.
- Helm Chart y versionado.
- Flujo Azure AKS + ACR.
- Ciclo DevOps aplicado al proyecto.

---

## 15. Evidencias del proyecto

Las evidencias se encuentran en:

```text
docs/capturas/
```

Incluyen capturas de:

- Contenedores Docker funcionando.
- Pods desplegados en Kubernetes.
- Helm instalado y actualizado.
- Pipeline de GitHub Actions en verde.
- Prometheus recolectando métricas.
- Grafana mostrando métricas.
- Intento de implementación en Azure AKS.

---

## 16. Estado del proyecto

| Componente | Estado |
|---|---|
| Microservicios | Completado |
| Docker | Completado |
| Kubernetes local con Minikube | Completado |
| Helm Chart | Completado |
| GitHub Actions | Completado |
| Prometheus y Grafana | Completado |
| Azure AKS | Intentado; limitado por cuota de Azure for Students |

---

## 17. Autora

Proyecto desarrollado por: **Estrella Zarate**

Actividad integradora de Kubernetes, empaquetado y monitoreo en DevOps.
