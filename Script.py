import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""SE PODRÍA AUTOMATIZAR LA BUSQUEDA DE LOS NOMBRES DE LOS LIBROS, PERO ESTA OPCIÓN TAMBIÉN ME GUSTA"""
# tipos de libros
tag_books = ('LMP','MLA','PAA','PCA','PEA','SDA','TPA','CMA','SHA')

#URL bases para la descarga de las imagenes y la busqueda del libro
base_url = 'https://www.conaliteg.sep.gob.mx/2023/c/'
base2_url = 'https://www.conaliteg.sep.gob.mx/2023/'

#Contador para P
for i in range (0,8):
    #Contador para los Titulos de los libros    
    for le in range (0,len(tag_books)):
        #Try y cach por si no encuentra la pagina
        try:
            # URL de los libros
            url =f'{base_url}P{i}{tag_books[le]}/'
            #url para buscar si existe el libro
            urlbusqueda =f'{base2_url}P{i}{tag_books[le]}.htm#page/2'
                        
            # Realizar la solicitud HTTP a la página web
            response = requests.get(urlbusqueda)
            response.raise_for_status()

            # Analizar el contenido HTML utilizando BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            #INTENTA ENCONTRAR LAS IMAGENES, DA OTRA COSA 
            img_tags = soup.find_all('img')

            #Donde se va a guardar
            output_folder = f'P{i}{tag_books[le]}'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            absolute_path = os.path.abspath(output_folder)
		"""SE PODRIA OMITIR EL USO DE LA VARIABLE BASE Y USAR EL CONTADOR DEL CICLO"""
            #Base para el numero de pagina
            base = "000"  

            # Descargar las imágenes
            for img_cont in range (1,400):
                img_num = f"{base}{img_cont}"[-len(base):]  # Asegura que solo los últimos caracteres se conserven
                # Obtener la URL de la imagen
                img_url =f'{url}{img_num}.jpg'
                img_name = img_url.split('/')[-1]  # Obtener el nombre de archivo de la URL
                img_path = os.path.join(output_folder, img_name)  # Ruta completa de destino
                
                
                response = requests.get(img_url)  # Realizar la solicitud HTTP


                if response.status_code == 200:
                    with open(img_path, 'wb') as img_file:
                        img_file.write(response.content)
			print(f'Imagen descargada: {img_name}')
                else:
			print(f'Imagen: {img_name} no pudo ser descargada')
                 	break

        except requests.exceptions.RequestException as e:
            print(f'No existe el libro {url}: {e}')
            continue

        print('Descarga completada.')
        print(f'Ruta absoluta de la carpeta de imágenes descargadas: {absolute_path}')
