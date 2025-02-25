from robot.api.deco import keyword
import re
import random
import string

class CustomKeywords:
    """Bibliothèque de mots-clés personnalisés pour les tests UI."""

    @keyword("Vérifier Format Texte")
    def verify_text_format(self, text, pattern, message=None):
        """Vérifie si un texte correspond à un format spécifique."""
        if not re.match(pattern, text):
            error_msg = message or f"Le texte '{text}' ne correspond pas au format attendu '{pattern}'"
            raise AssertionError(error_msg)
        return True

    @keyword("Générer Datas Aléatoires")
    def generate_random_data(self, data_type, length=10):
        """Génère des datas aléatoires selon le type spécifié."""
        if data_type.lower() == "email":
            username = ''.join(random.choices(string.ascii_lowercase, k=length))
            return f"{username}@example.com"
        elif data_type.lower() == "password":
            chars = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choices(chars, k=length))
        elif data_type.lower() == "phone":
            return ''.join(random.choices(string.digits, k=10))
        else:
            return ''.join(random.choices(string.ascii_letters, k=length))
