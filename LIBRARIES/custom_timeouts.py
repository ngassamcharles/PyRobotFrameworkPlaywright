import time
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn

@library
class DynamicTimeouts:
    def __init__(self):
        self.default_timeout = 10  # secondes
        self.slow_connection_factor = 1.5
        self.fast_connection_factor = 0.8

    @keyword("Attendre Avec Timeout Dynamique")
    def wait_with_dynamic_timeout(self, condition_function, base_timeout=None,
                                  connection_type="normal", max_retries=3):
        """
        Attend qu'une condition soit remplie avec un timeout dynamique.

        Args:
            condition_function: Fonction qui retourne True quand la condition est remplie
            base_timeout: Timeout de base en secondes (utilise default_timeout si None)
            connection_type: "slow", "normal" ou "fast"
            max_retries: Nombre maximal de tentatives
        """
        timeout = base_timeout if base_timeout is not None else self.default_timeout

        # Ajuster le timeout selon le type de connexion
        if connection_type.lower() == "slow":
            timeout *= self.slow_connection_factor
        elif connection_type.lower() == "fast":
            timeout *= self.fast_connection_factor

        start_time = time.time()
        attempts = 0

        while attempts < max_retries:
            try:
                if condition_function():
                    return True
            except Exception as e:
                BuiltIn().log(f"Exception lors de la vérification: {str(e)}", "WARN")

            if time.time() - start_time > timeout:
                if attempts < max_retries - 1:
                    BuiltIn().log(f"Timeout dépassé, nouvelle tentative {attempts+1}/{max_retries}")
                    attempts += 1
                    # Augmenter le timeout pour les tentatives suivantes
                    timeout *= 1.5
                    start_time = time.time()
                else:
                    raise TimeoutError(f"Timeout dépassé après {max_retries} tentatives")
            time.sleep(0.5)  # Pause avant nouvelle vérification
