import requests
import base64
import time
import io
from PIL import Image
from datetime import datetime
import os
import cv2

def yolo_fire_prediction(url, image_path, download_path, save_img=True, verbose=True):
    """
    Predicción de incendios - YOLO - SoF/TT:
    ########################################

    Realiza una predicción de detección de incendios utilizando el modelo YOLO alojado en el servidor.

    -----

    :Example:

    Por ejemplo:
    ############

    Código::

        # URL de la API
        url_endpoint = 'http://ec2-15-228-222-79.sa-east-1.compute.amazonaws.com:5000'

        # Ruta de la imagen que deseas enviar
        image_path_fire = '../data/test_facu/quema_controlada132.jpg'

        predic, posi = yolo_fire_prediction(url_endpoint, image_path_fire, '../notebooks', save_img = True, verbose=True)

    Esto devuelve por consola::

        >> Cargando quema_controlada132.jpg
        >> El servidor recibió la imagen correctamente. Procesando... Id de tarea: 8008e8b8-bcfd-4dd3-b648-5a012e909bf2
        >> Obteniendo imagen procesada, espere
        >> Imagen guardada en: ../notebooks/quema_controlada132.jpg_predicted_at_19_58_13.jpg
        >> Imagen procesada con éxito. 19:58:13
        >> Detecciones realizadas: Detección: Fuego
        >> [['humo', 11, 284, 210, 124], ['humo', 72, 213, 925, 214], ['humo', 999, 352, 97, 76], ['humo', 105, 346, 123, 70]]

    Parametros y returns:
    #####################

    -----

    :param url: URL del servicio de detección de incendios (str).
    :param image_path: Ruta de la imagen que se desea enviar para la predicción (str).
    :param download_path: Ruta del directorio donde se guardarán las imágenes procesadas (str).
    :param save_img: Indica si se debe guardar la imagen procesada. Valor predeterminado: True (bool).
    :param verbose: Indica si se deben imprimir mensajes de información durante la ejecución. Valor predeterminado: True (bool).

    :return: Texto con las predicciones realizadas (str).
    :return: Texto con las posiciones de las detecciones (str).

    """
    nombre_imagen = image_path.split('/')[-1]
    if verbose:
        print(f'Cargando {nombre_imagen}')
    # Leer la imagen
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # Realizar la solicitud POST con la imagen
    response = requests.post(f'{url}/detect', files={'image': image_bytes})

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Obtener los datos de la respuesta JSON
        response_data = response.json()
        if verbose:
            print(f"El servidor recibió la imagen correctamente. Procesando... Id de tarea: {response_data['job_id']}")

        # Obtener el ID del trabajo encolado
        job_id = response_data['job_id']

        # Ruta para obtener el resultado del trabajo
        result_url = f'{url}/result/{job_id}'

        if verbose:
            print('Obteniendo imagen procesada, espere')
        while True:
            time.sleep(0.5)

            # Realizar la solicitud GET para obtener el resultado
            result_response = requests.get(result_url)

            # Verificar el estado de la respuesta
            if result_response.status_code == 200:

                # Obtener los datos del resultado JSON
                result_data = result_response.json()

                try:
                    img_base64 = result_data['image']
                    img_bytes = base64.b64decode(img_base64)

                    predicción = result_data['text']
                    pos = result_data['posiciones']

                    # Crear un objeto de imagen a partir de los bytes decodificados
                    image = Image.open(io.BytesIO(img_bytes))
                    if save_img == True:
                        # Guardar la imagen recibida con las cajas dibujadas
                        output_image_path = f'{download_path}/{nombre_imagen}_predicted_at_{datetime.now().strftime("%H_%M_%S")}.jpg'
                        if not os.path.exists(download_path):
                            print(f'directorio "{download_path}" no existe')
                            break
                        if verbose:
                            print(f'Imagen guardada en: {output_image_path}')
                        image.save(output_image_path)
                    if verbose:
                        print(f'Imagen procesada con éxito. {datetime.now().strftime("%H:%M:%S")}')
                        print(f'Detecciones realizadas: {predicción}')
                        print(f'{pos}')
                    return predicción, pos

                except:
                    pass

            else:
                print('Error en la solicitud del resultado:', result_response.text)
    else:
        print('Error en la solicitud:', response.text)



def yolo_fire_prediction_no_img(url, image_path, model, threshold, image_size, verbose=True):
    """
    Predicción de incendios - YOLO - SoF/TT:
    ########################################

    Realiza una predicción de detección de incendios utilizando el modelo YOLO alojado en el servidor.

    -----

    :Example:

    Por ejemplo:
    ############

    Código::

        import time
        # URL de la API
        url_endpoint = 'http://ip:puerto'

        # Ruta de la imagen que deseas enviar
        image_path_fire = '../data/test_facu/quema_controlada132.jpg'

        predic, posi = yolo_fire_prediction_no_img(url=url_endpoint,
                                            image_path=image_path_fire,
                                            model = 'v3',
                                            threshold = 0.1,
                                            image_size = (416,416),
                                            verbose=True)
    Esto devuelve por consola::

        >> Cargando quema_controlada132.jpg
        >> El servidor recibió la imagen correctamente. Procesando... Id de tarea: 8008e8b8-bcfd-4dd3-b648-5a012e909bf2
        >> Obteniendo imagen procesada, espere
        >> Imagen procesada con éxito. 00:04:34
        >> Detecciones realizadas: Detección: Fuego
        >> [['humo', 2, 109, 45, 47, '0.71'], ['humo', 15, 81, 202, 84, '0.6'], ['humo', 216, 135, 21, 29, '0.48'], ['humo', 23, 132, 26, 27, '0.46']]

    Parametros y returns:
    #####################

    -----

    :param url: URL del servicio de detección de incendios (str).
    :param image_path: Ruta de la imagen que se desea enviar para la predicción (str).
    :param model: Modelo a utilizar para la inferencia (str).
    :param threshold: sensibilidad a utilizar para la inferencia (float).
    :param image_size: Indica el tamaño de la imagen de entrada al modelo (tuple).
    :param verbose: Indica si se deben imprimir mensajes de información durante la ejecución. Valor predeterminado: True (bool).

    :return: Texto con las predicciones realizadas (str).
    :return: Texto con las posiciones de las detecciones (str).

    """


    nombre_imagen = image_path.split('/')[-1]
    if verbose:
        print(f'Cargando {nombre_imagen}')


    # Leer la imagen
    img = cv2.imread(image_path)

    # Redimensionar la imagen a 416x416 píxeles
    resized_img = cv2.resize(img, image_size)

    # Crear un diccionario que contenga la imagen redimensionada y el string
    data = {'image': cv2.imencode('.jpg', resized_img)[1].tobytes(), 'sensibilidad': f'{threshold}'}

    # Realizar la solicitud POST con la imagen
    response = requests.post(f'{url}/detect_{model}', files=data)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Obtener los datos de la respuesta JSON
        response_data = response.json()
        if verbose:
            print(f"El servidor recibió la imagen correctamente. Procesando... Id de tarea: {response_data['job_id']}")

        # Obtener el ID del trabajo encolado
        job_id = response_data['job_id']

        # Ruta para obtener el resultado del trabajo
        result_url = f'{url}/result/{job_id}'

        if verbose:
            print('Obteniendo imagen procesada, espere')
        while True:
            time.sleep(0.5)

            # Realizar la solicitud GET para obtener el resultado
            result_response = requests.get(result_url)

            # Verificar el estado de la respuesta
            if result_response.status_code == 200:

                # Obtener los datos del resultado JSON
                result_data = result_response.json()

                try:
                    predicción = result_data['text']
                    pos = result_data['posiciones']

                    if verbose:
                        print(f'Imagen procesada con éxito. {datetime.now().strftime("%H:%M:%S")}')
                        print(f'Detecciones realizadas: {predicción}')
                        print(f'{pos}')
                    return predicción, pos

                except:
                    pass

            else:
                print('Error en la solicitud del resultado:', result_response.text)
    else:
        print('Error en la solicitud:', response.text)