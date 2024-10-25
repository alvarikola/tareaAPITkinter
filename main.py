from pickle import FRAME
from tkinter import ttk
from typing import List
from tkinter import messagebox as alert
from weasyprint import HTML
import requests
import tkinter as tk
from textwrap import wrap

from PIL import Image, ImageTk
from dataclass_wizard import fromdict
from models.apiResponse import ApiResponse
from models.empresa import Empresa
from models.product import Product

response = requests.get("https://dummyjson.com/products")
data_dict = response.json()
product_list = fromdict(ApiResponse, data_dict)


indice = 0
label_titulos_productos = None
label_descripcion_productos = None
label_categoria_productos = None
label_imagen_producto = None
label_precio_producto = None


def inicializarLabels(pantalla):
    global label_titulos_productos, label_descripcion_productos, label_categoria_productos, label_imagen_producto, label_precio_producto

    label_titulos_productos = ttk.Label(pantalla, text="", font=("Arial", 25, "bold"), background="white")
    label_titulos_productos.pack(padx=20, pady=10)

    label_descripcion_productos = ttk.Label(pantalla, font=("Arial", 15), background="white")
    label_descripcion_productos.pack(padx=20, pady=0)

    label_categoria_productos = ttk.Label(pantalla, text="", font=("Arial", 12), background="white", justify="left", width=83)
    label_categoria_productos.pack()

    label_imagen_producto = ttk.Label(pantalla, text="cargando...", background="white", borderwidth=2, relief="solid")
    label_imagen_producto.pack(padx=20, pady=20)

    label_precio_producto = ttk.Label(pantalla, text="", font=("Arial", 15), background="white")
    label_precio_producto.pack(padx=20, pady=20)


def mostrarProducto():
    global indice
    if indice < len(product_list.products):
        label_titulos_productos.config(text=product_list.products[indice].title)
        description_wrapped = wrap(product_list.products[indice].description, width=80)
        description = ""
        for line in description_wrapped:
            description += line + "\n"
        label_descripcion_productos.config(text=description)
        label_categoria_productos.config(text="Categoría: " + product_list.products[indice].category)
        bits_imagen = requests.get(product_list.products[indice].thumbnail, stream=True)
        imagen = Image.open(bits_imagen.raw)
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen_producto.config(image=imagen_tk)
        label_imagen_producto.image = imagen_tk
        label_precio_producto.config(text="Precio: " + str(product_list.products[indice].price) + " euros")


def siguiente():
    global indice
    indice += 1
    if indice < len(product_list.products):
        mostrarProducto()
    else:
        indice = -1


def atras():
    global indice
    indice -= 1
    if indice < len(product_list.products):
        mostrarProducto()
    else:
        indice = len(product_list.products) - 1


def buscar():
    global product_list
    texto = buscarProducto.get().lower()
    productos_busqueda = list(filter(lambda producto: texto in producto.title.lower(), product_list.products))
    productos_busqueda.sort(key=lambda producto: producto.title)
    mostrar_listado(productos_busqueda)

def mostrar_listado(productos: List[Product]):
    pantalla_listado_productos = tk.Tk()
    pantalla_listado_productos.title("Alvarikola Store")
    pantalla_listado_productos.resizable(False, False)
    pantalla_listado_productos.config(background="white")
    ttk.Label(pantalla_listado_productos, text="Productos", font=("Arial", 18, "bold"), background="white").pack()
    for producto in productos:
        ttk.Label(pantalla_listado_productos, text=producto.title, background="white", justify="left", width=50).pack()

    boton_pdf = ttk.Button(pantalla_listado_productos, text="Generar PDF", command=lambda: generar_pdf(productos))
    boton_pdf.pack(padx=(0, 0))


def generar_pdf(productos: List[Product]):
    empresa: Empresa = Empresa (
        nombre="Alvarikola Soft S.L",
        titular= "Alvarotech Industries López",
        cif="123456789",
        direccion="Calel",
        email="hola@alvarikola.com",
    )
    contenido_pdf = """
    <html>
        <head>
            <h1>Productos</h1>
        </head>
        <body>
    """
    indice = 0
    for producto in productos:
        indice += 1
        contenido_pdf += """
            <table>
                <tr>
                    <td>""" + str(indice) + """</td>
                    <td><img src='""" + producto.thumbnail + """'/></td>
                    <td>""" + producto.title + """</td>
                    <td>""" + producto.category + """</td>
                    <td>""" + str(producto.price) + """</td>
                </tr>
            </table>
        """
    contenido_pdf += """
        </body>
    </html>
    """
    # Genero PDF (nombre=bsuqueda_resultado_202410241344SS.pdf)
    htmldoc = HTML(string=contenido_pdf)
    htmldoc.write_pdf(target="archivo.pdf")
    # alert.showinfo("PDF generado", "Se ha generado el PDF correctamente")
    # print(contenido_pdf)

def main():
    global buscarProducto
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("1200x800")
    root.title("Alvarikola Store")
    root.config(background="white")

    label_titulo = ttk.Label(root, text="Productos", font=("Arial", 35, "bold"), background="white", foreground="#0077c8")
    label_titulo.pack(side="top")

    busquedaBarra = tk.Frame(root, bg="white")
    busquedaBarra.pack(side="top", fill="x", padx=20, pady=20)

    busquedaElementos = tk.Frame(busquedaBarra, bg="white")
    busquedaElementos.pack(side="top")

    label_buscador = ttk.Label(busquedaElementos, text="Buscar producto: ", font=("Arial", 18, "bold"), background="white")
    label_buscador.pack(side="left")

    buscarProducto = ttk.Entry(busquedaElementos, width=50)
    buscarProducto.pack(side="left")

    boton_buscar = ttk.Button(busquedaElementos, text="Buscar", command=buscar)
    boton_buscar.pack(side="left", padx=(20, 0))

    inicializarLabels(root)

    boton_siguiente = ttk.Button(root, text="Siguiente", command=siguiente)
    boton_siguiente.pack()

    boton_atras = ttk.Button(root, text="Atrás", command=atras)
    boton_atras.pack()


    mostrarProducto()
    root.mainloop()


main()
