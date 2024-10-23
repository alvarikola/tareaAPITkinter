from pickle import FRAME
from tkinter import ttk
import requests
import tkinter as tk
from textwrap import wrap

from PIL import Image, ImageTk
from dataclass_wizard import fromdict
from models.apiResponse import ApiResponse

response = requests.get("https://dummyjson.com/products")
data_dict = response.json()
product_list = fromdict(ApiResponse, data_dict)


indice = 0
label_titulos_productos = ""
label_descripcion_productos = ""
label_categoria_productos = ""
label_imagen_producto = ""
label_precio_producto = ""


def mostrarProducto():
    global indice, label_titulos_productos, label_descripcion_productos, label_categoria_productos, label_imagen_producto, label_precio_producto
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


def main():
    global label_titulos_productos, label_descripcion_productos, label_categoria_productos, label_imagen_producto, label_precio_producto
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

    boton_buscar = ttk.Button(busquedaElementos, text="Buscar", command=None)
    boton_buscar.pack(side="left", padx = (20,0))

    label_titulos_productos = ttk.Label(root, text="", font=("Arial", 25, "bold"), background="white")
    label_titulos_productos.pack(padx=20, pady=10)

    label_descripcion_productos = ttk.Label(root, font=("Arial", 15), background="white")
    label_descripcion_productos.pack(padx=20, pady=0)

    label_categoria_productos = ttk.Label(root, text="", font=("Arial", 12), background="white", justify="left", width=83)
    label_categoria_productos.pack()

    label_imagen_producto = ttk.Label(root, text="cargando...", background="white", borderwidth=2, relief="solid")
    label_imagen_producto.pack(padx=20, pady=20)

    label_precio_producto = ttk.Label(root, text="", font=("Arial", 15), background="white")
    label_precio_producto.pack(padx=20, pady=20)

    boton_siguiente = ttk.Button(root, text="Siguiente", command=siguiente)
    boton_siguiente.pack()

    boton_atras = ttk.Button(root, text="Atrás", command=atras)
    boton_atras.pack()


    mostrarProducto()
    root.mainloop()


main()
