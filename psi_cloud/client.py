import requests
from typing import Union, List, Dict, Any

class PSIClient:
    """
    SDK Oficial para el Motor PSI (Proposición de Suficiencia Informativa).
    Permite evaluar la resolución determinística de sistemas complejos.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://psi-cloud-v1.onrender.com"):
        """
        Inicializa el cliente del motor PSI.
        
        :param api_key: Tu clave secreta de la plataforma PSI Cloud.
        :param base_url: La URL base de la API (útil si pruebas en localhost).
        """
        self.api_key = api_key
        # Limpiamos la URL por si el cliente pone un "/" al final por accidente
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def check_sufficiency(self, n: int, bits: Union[int, float, List[Union[int, float]]]) -> Dict[str, Any]:
        """
        Envía los parámetros al motor industrial para evaluar la suficiencia informativa.
        
        :param n: Número de elementos/nodos en el sistema.
        :param bits: Información cuantificada (puede ser un número o una lista de variables).
        :return: Diccionario con el diagnóstico, métricas y créditos restantes.
        """
        endpoint = f"{self.base_url}/api/sdk/v1/evaluate"
        payload = {"n": n, "bits": bits}

        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            
            # Todo salió perfecto
            if response.status_code == 200:
                return response.json()
            
            # Se acabaron los créditos (El 402 que programamos)
            elif response.status_code == 402:
                raise PermissionError(f"[PSI Error 402] Límite de créditos alcanzado. Por favor, actualiza a PRO.")
                
            # La llave es falsa o fue revocada
            elif response.status_code == 403:
                raise PermissionError("[PSI Error 403] API Key inválida o revocada.")
                
            # Error de parámetros
            elif response.status_code == 400:
                raise ValueError(f"[PSI Error 400] {response.json().get('detail', 'Parámetros incorrectos')}")
                
            # Error interno de tu lado
            else:
                raise RuntimeError(f"[PSI Error {response.status_code}] Falla en el motor: {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise ConnectionError("No se pudo conectar con los servidores de PSI Cloud. Verifica tu internet.")