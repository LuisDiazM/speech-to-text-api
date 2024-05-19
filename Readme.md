# API para transcribir audio

## Descripción

Este proyecto se encarga de exponer una API usando fast-api con una validación sencilla de x-api-key que se carga desde una variable de entorno, la API se encarga de transcribir el audio que se envíe a través de la petición, sólo se restrigió para archivos de audio .mp3 o .wav donde se devuelve la respuesta de la transcripción; el modelo utilizado es faster-whisper el cual es configurable de acuerdo a las variables de entorno MODEL_PATH, sin embargo, también tiene la posibilidad de usar el modelo desde un volumen k8s en este caso hostpath a modo de pruebas para que al levantar multiples PODS no tenga que descargar el modelo nuevamente, en lugar de ello lo carga directamente desde el volumen.

## Configuraciones

La variable de entorno MODEL_PATH puede tomar los siguientes valores de acuerdo a los modelos de faster whisper: tiny, tiny.en, base, base.en,
small, small.en, medium, medium.en, large-v1, large-v2, large-v3, or large, también se puede configurar el path que se carga desde el volumen con el siguiente valor ```/app/models``` (modo eficiente cuando existan múltiples réplicas).

Este proyecto se puede correr de tres formas:

#### Corriendo la aplicación directamente en python
Crear un entorno virtual e instalar las dependencias del *requirements.txt*

#### Corriendo la aplicación con docker compose

Usando docker-compose con configuraciones básicas sin configuración de volumenes. 
```docker compose up --build```

#### Usando k8s con minikube
1. Aplicar los manifiestos *.yaml 
```kubectl apply -f infraestructure/k8s/.```
2. Descargar el modelo faster whisper deseado, se recomienda descargar inicialmente uno liviano como *tiny* y luego aplicar la configuración con uno más completo.

Como paso previo se requiere crear un entorno virtual de python
en instalar el requirements.txt
una vez esté habilitado este entorno virtual con sus dependencias:
```
python download/download_model.py
```
esto descargará el modelo en una carpeta llamada download/models si se desea descargar otro modelo cambiar la variable size_available.

3. Crear el directorio dentro del cluster de minikube usando:
```
minikube ssh
mkdir mnt & mkdir data
```

4. Cargar la información del modelo descargado dentro del cluster, se recomienda desde el directorio download
```
minikube mount models:/mnt/data
```
5. Exponer un servicio tipo nodePort para poder comunicarnos con el API
```
kubectl expose service speechtotextapisvc --type=NodePort --target-port=8000 --name=speechtotextapisvc-ext --namespace=develop
```

6. Exponer el servicio del cluster con minikube para poder tener la IP y el puerto

```
minikube service speechtotextapisvc-ext --namespace=develop
```
Un ejemplo de la respuesta de este comando es la siguiente:
| NAMESPACE |          NAME          | TARGET PORT |            URL            |
|-----------|------------------------|-------------|---------------------------|
| develop   | speechtotextapisvc-ext |        8000 | http://192.168.49.2:30984 |

7. Consumir el endpoint 
``` 
curl --location 'http://192.168.49.2:30984/transcribe' \
--header 'x-api-key: OllCRxPK1EGZohP2IRLsCZShQikhL4N4' \
--form 'file=@"/home/luis-diaz/Escritorio/sin nombre.wav"' 
```
