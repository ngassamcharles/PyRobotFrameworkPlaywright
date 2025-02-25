import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from robot.api.deco import keyword, library

@library
class EmailNotifier:
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        # Valeurs par défaut qui peuvent être surchargées
        self.smtp_server = smtp_server or os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.environ.get('SMTP_PORT', 587))
        self.username = username or os.environ.get('SMTP_USERNAME', '')
        self.password = password or os.environ.get('SMTP_PASSWORD', '')

    @keyword("Envoyer Notification Par Email")
    def send_email_notification(self, recipients, subject, body, attachments=None,
                                html_format=True, cc=None, bcc=None):
        """
        Envoie une notification par email avec les résultats des tests.

        Args:
            recipients: Liste des destinataires ou chaîne séparée par des virgules
            subject: Sujet de l'email
            body: Corps du message
            attachments: Liste des chemins de fichiers à joindre
            html_format: True pour envoyer en format HTML, False pour texte brut
            cc: Liste des destinataires en copie
            bcc: Liste des destinataires en copie cachée
        """
        # Convertir les chaînes en listes si nécessaire
        if isinstance(recipients, str):
            recipients = [r.strip() for r in recipients.split(',')]
        if isinstance(cc, str):
            cc = [r.strip() for r in cc.split(',')]
        if isinstance(bcc, str):
            bcc = [r.strip() for r in bcc.split(',')]

        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject

        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        # Ajouter le corps du message
        if html_format:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        # Ajouter les pièces jointes
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition',
                                        f'attachment; filename="{os.path.basename(file_path)}"')
                        msg.attach(part)

        # Envoyer l'email
        try:
            all_recipients = recipients + (cc or []) + (bcc or [])

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, all_recipients, msg.as_string())
            server.quit()
            return True, "Email envoyé avec succès"
        except Exception as e:
            return False, f"Erreur lors de l'envoi de l'email: {str(e)}"

    @keyword("Envoyer Rapport De Test Par Email")
    def send_test_report_email(self, recipients, report_file, log_file=None,
                               include_summary=True, custom_message=""):
        """
        Envoie un rapport de test par email avec les fichiers de rapport joints.

        Args:
            recipients: Liste des destinataires
            report_file: Chemin vers le fichier de rapport
            log_file: Chemin vers le fichier de log (optionnel)
            include_summary: Inclure un résumé des résultats dans le corps du message
            custom_message: Message personnalisé à inclure dans l'email
        """
        subject = "Rapport d'exécution des tests automatisés"

        # Créer le corps du message HTML
        body = f"""
        <html>
        <head>
                    <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }}
            .summary {{
                font-weight: bold;
                color: #007BFF;
            }}
        </style>
        </head>
        <body>
            <p>Bonjour,</p>
            <p>Veuillez trouver ci-joint le rapport d'exécution des tests automatisés.</p>
            {f"<p class='summary'>Résumé des résultats : {custom_message}</p>" if include_summary else ""}
            <p>Cordialement,</p>
            <p>L'équipe QA</p>
        </body>
        </html>
        """

        # Ajouter les fichiers en pièce jointe
        attachments = [report_file]
        if log_file:
            attachments.append(log_file)

        # Envoyer l'email
        return self.send_email_notification(recipients, subject, body, attachments, html_format=True)