import logging
from robot.api import logger
from datetime import datetime

class EnhancedLogging:
    def __init__(self):
        # Configuration du logger Python
        self.logger = logging.getLogger('enhanced_logger')
        self.logger.setLevel(logging.DEBUG)

        # Handler pour fichier avec rotation
        file_handler = logging.FileHandler('test_execution.log')
        file_handler.setLevel(logging.DEBUG)

        # Format personnalisé avec timestamp, niveau et message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_with_timestamp(self, message, level="INFO"):
        """Log un message avec timestamp et niveau personnalisé."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Utilise le logger de Robot Framework pour l'intégration dans les rapports
        if level.upper() == "INFO":
            logger.info(f"[{timestamp}] {message}")
        elif level.upper() == "DEBUG":
            logger.debug(f"[{timestamp}] {message}")
        elif level.upper() == "WARN":
            logger.warn(f"[{timestamp}] {message}")
        elif level.upper() == "ERROR":
            logger.error(f"[{timestamp}] {message}")

        # Log également dans le fichier
        self.logger.log(getattr(logging, level.upper()), message)

    def log_test_step(self, step_name, step_data=None):
        """Log une étape de test avec données optionnelles."""
        message = f"ÉTAPE: {step_name}"
        if step_data:
            message += f" | DONNÉES: {step_data}"
        self.log_with_timestamp(message)
