import requests
import functools
from typing import Union, List, Dict, Any, Callable, Optional

class PSIClient:
    """
    SDK Oficial para el Motor PSI (Proposición de Suficiencia Informativa).
    Permite evaluar la resolución determinística de sistemas complejos y
    proteger la ejecución de funciones pesadas.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://psi-cloud-v1.onrender.com"):
        """
        Inicializa el cliente del motor PSI.
        
        :param api_key: Tu clave secreta de la plataforma PSI Cloud.
        :param base_url: La URL base de la API.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def check_sufficiency(self, n: int, bits: Union[int, float, List[Union[int, float]]]) -> Dict[str, Any]:
        """
        Envía los parámetros al motor industrial para evaluar la suficiencia informativa.
        """
        endpoint = f"{self.base_url}/api/sdk/v1/evaluate"
        payload = {"n": n, "bits": bits}

        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 402:
                raise PermissionError(f"[PSI Error 402] Límite de créditos alcanzado. Por favor, actualiza a PRO.")
            elif response.status_code == 403:
                raise PermissionError("[PSI Error 403] API Key inválida o revocada.")
            elif response.status_code == 400:
                raise ValueError(f"[PSI Error 400] {response.json().get('detail', 'Parámetros incorrectos')}")
            else:
                raise RuntimeError(f"[PSI Error {response.status_code}] Falla en el motor: {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise ConnectionError("No se pudo conectar con los servidores de PSI Cloud. Verifica tu internet.")

    def psi_gated(self, n: int, bits_extractor: Callable[..., Union[int, float]], fallback_response: Any = None):
        """
        Decorador (Wrapper) para proteger la ejecución de funciones costosas.
        Solo ejecuta la función decorada si el sistema tiene información suficiente.
        
        :param n: El tamaño del espacio de estados del sistema.
        :param bits_extractor: Una función que extrae/calcula los 'bits' de los argumentos de la función decorada.
        :param fallback_response: Lo que devuelve la función si se bloquea por insuficiencia (Ej: {"error": "Insuficiente"}).
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 1. Extraer los bits actuales de los argumentos de la función
                current_bits = bits_extractor(*args, **kwargs)
                
                # 2. Consultar al Motor PSI
                try:
                    psi_result = self.check_sufficiency(n=n, bits=current_bits)
                    is_sufficient = psi_result.get("deterministic_achieved", False)
                except Exception as e:
                    # En caso de error de red o de API, fallamos de forma segura (ejecutamos igual o lanzamos error)
                    # Aquí decidimos lanzar el error para ser estrictos.
                    raise RuntimeError(f"Fallo en la validación PSI: {e}")

                # 3. La "Puerta Determinística" (The Entropy-Gate)
                if is_sufficient:
                    # ✅ Información suficiente -> Ejecutar la función pesada (GPU/IA)
                    return func(*args, **kwargs)
                else:
                    # ❌ Insuficiente -> Inhibir ejecución, ahorrar cómputo y retornar fallback
                    print(f"[PSI Gate] Inhibición activada. Faltan {psi_result.get('gap', 'X')} bits.")
                    if callable(fallback_response):
                        return fallback_response(*args, **kwargs)
                    return fallback_response
            return wrapper
        return decorator
