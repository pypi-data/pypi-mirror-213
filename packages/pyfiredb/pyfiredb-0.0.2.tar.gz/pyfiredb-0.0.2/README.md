# AlegraPy

Agiliza las consultas a la base de datos utilizando la librería "Pyrebase". Pyrebase es una biblioteca de Python que proporciona una interfaz para interactuar con Firebase, una plataforma de desarrollo de aplicaciones web y móviles.

## Características

- Permite actualizar, leer, buscar el máximo, buscar entre, buscar 

## Instalación y uso

### Instalación

```
pip install pyfiredb
```

### Uso

Un ejemplo para usar este paquete, la configuración de firebase y credenciales de acceso se han tomado desde las variables de entorno

```python
from pyfiredb import Credentials
from pyfiredb import Database
from pyfiredb import Session


def run():
    fire = Session(Credentials.user, Credentials.password)
    firebase = Database(fire)
    print(firebase.equal("alegra/products", "reference", "TP-19100"))
    print(firebase.get("woocommerce/products"))
    invoices = firebase.between("alegra/invoices", "date",
                                "2023-05-01", "2023-05-1")
    print(invoices[1])


if __name__ == "__main__":

    run()
```

## Créditos

- Camilo Andrés Rodriguez

## referencias

- https://developer.alegra.com/


## Licencia

Este proyecto está bajo la Licencia [MIT].

---

¡Puedes personalizarlo según las necesidades específicas de tu proyecto!

