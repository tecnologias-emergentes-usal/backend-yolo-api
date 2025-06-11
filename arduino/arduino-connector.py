import requests

class ControladorLuzWiFi:
    def __init__(self, ip_arduino):
        """
        Inicializa el controlador con la IP del Arduino.
        :param ip_arduino: Dirección IP del ESP (ej: '192.168.0.123')
        """
        self.base_url = f"http://{ip_arduino}"

    def controlar_luz(self, cantidad_autos):
        """
        Envía una solicitud al Arduino para encender o apagar la luz.
        :param cantidad_autos: Número de autos detectados
        """
        try:
            if cantidad_autos > 10:
                response = requests.get(f"{self.base_url}/luz/on", timeout=3)
                print(f"Luz encendida (autos: {cantidad_autos}) | Respuesta: {response.text}")
            else:
                response = requests.get(f"{self.base_url}/luz/off", timeout=3)
                print(f"Luz apagada (autos: {cantidad_autos}) | Respuesta: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error al contactar al Arduino: {e}")

    def test_conexion(self):
        """
        Testea la conexión al servidor del Arduino.
        """
        try:
            response = requests.get(f"{self.base_url}", timeout=3)
            print(f"Arduino disponible. Respuesta: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"No se pudo conectar al Arduino: {e}")
