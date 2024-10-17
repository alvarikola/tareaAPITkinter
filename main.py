import requests
import tkinter as tk
from dataclass_wizard import fromdict
from models.apiResponse import ApiResponse


response = requests.get("https://dummyjson.com/products")
data_dict = response.json()
product_list = fromdict(ApiResponse, data_dict)

# print(product_list.total)

# for product in product_list.products:
#     print(product.title)


def main():
    root = tk.Tk()
    root.title("Tarea 3")
    titulo = "Titulos de productos"
    root.title("Titulos de productos")
    label_titulo = tk.Label(text=titulo, font=("Arial", 20))
    label_titulo.pack(padx=20, pady=20)
    for product in product_list.products:
        label_titulos_productos = tk.Label(text=product.title)
        label_titulos_productos.pack(padx=20, pady=20)

    root.mainloop()


main()