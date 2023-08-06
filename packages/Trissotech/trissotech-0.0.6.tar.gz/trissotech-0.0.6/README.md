
<p align="center">
  <img src="https://trissotech.s3.sa-east-1.amazonaws.com/TT-icon.png" alt="TT" style="width: 200px; height: auto;">
</p>

# Trissotech

En esta librería se encuentran las utilidades de la empresa Trissotech

```bash
pip install Trissotech
```

---

## Trissotech.API:
- yolo_fire_prediction: Función para detectar incendios en imágenes utilizando un modelo YOLO.
- yolo_fire_prediction_no_img: Función para detectar incendios en imágenes utilizando un modelo YOLO.

---

### - yolo_fire_prediction()
Para ejecutar este proyecto, se deben seguir los siguientes pasos:



Ejemplo de aplicación

Código:
```python
# URL de la API
url_endpoint = 'endpoint:puerto'

# Ruta de la imagen que deseas enviar
image_path_fire = '/path/al/archivo.jpg'

# Ruta donde deseas recibir la imagen procesada
image_path_download = '/path/a/carpeta'

predicciones, posiciones = yolo_fire_prediction(url_endpoint, image_path_fire, image_path_download, save_img = True, verbose=True)
```

Esto devuelve por consola:

    >> Cargando quema_controlada132.jpg
    >> El servidor recibió la imagen correctamente. Procesando... Id de tarea: 8008e8b8-bcfd-4dd3-b648-5a012e909bf2
    >> Obteniendo imagen procesada, espere
    >> Imagen guardada en: ../notebooks/quema_controlada132.jpg_predicted_at_19_58_13.jpg
    >> Imagen procesada con éxito. 19:58:13
    >> Detecciones realizadas: Detección: Fuego
    >> [['humo', 11, 284, 210, 124], ['humo', 72, 213, 925, 214], ['humo', 999, 352, 97, 76], ['humo', 105, 346, 123, 70]]
