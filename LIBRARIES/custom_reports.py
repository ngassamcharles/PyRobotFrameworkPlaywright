import os
import json
from datetime import datetime
from robot.api import ExecutionResult
from robot.api.deco import keyword

class CustomReporter:
    def __init__(self):
        self.report_dir = "custom_reports"
        os.makedirs(self.report_dir, exist_ok=True)

    @keyword("Générer Rapport Personnalisé")
    def generate_custom_report(self, output_xml_path, include_screenshots=True):
        """
        Génère un rapport personnalisé à partir du fichier output.xml de Robot Framework.

        Args:
            output_xml_path: Chemin vers le fichier output.xml
            include_screenshots: Inclure les captures d'écran dans le rapport
        """
        # Analyser le résultat d'exécution
        result = ExecutionResult(output_xml_path)
        result.configure(stat_config={'suite_stat_level': 2, 'tag_stat_combine': 'tagANDanother'})

        # Créer structure de données pour le rapport
        report_data = {
            "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_tests": result.statistics.total.all.total,
                "passed": result.statistics.total.all.passed,
                "failed": result.statistics.total.all.failed,
                "skipped": result.statistics.total.all.skipped,
                "pass_percentage": round((result.statistics.total.all.passed /
                                          result.statistics.total.all.total) * 100, 2)
            },
            "suites": []
        }

        # Extraire les données des suites et tests
        for suite in result.suite.suites:
            suite_data = {
                "name": suite.name,
                "status": suite.status,
                "tests": []
            }

            for test in suite.tests:
                test_data = {
                    "name": test.name,
                    "status": test.status,
                    "tags": list(test.tags),
                    "start_time": test.starttime,
                    "end_time": test.endtime,
                    "elapsed_time": test.elapsedtime / 1000,  # en secondes
                    "messages": [msg.message for msg in test.message]
                }

                if include_screenshots and hasattr(test, 'screenshots'):
                    test_data["screenshots"] = test.screenshots

                suite_data["tests"].append(test_data)

            report_data["suites"].append(suite_data)

        # Générer le rapport au format JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.report_dir, f"custom_report_{timestamp}.json")

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        # Générer aussi une version HTML simple
        html_report = os.path.join(self.report_dir, f"custom_report_{timestamp}.html")
        self._generate_html_report(report_data, html_report)

        return report_file, html_report

    def _generate_html_report(self, report_data, output_file):
        """Génère un rapport HTML à partir des données structurées."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport de test personnalisé</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .skipped {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h1>Rapport de test personnalisé</h1>
            <p>Généré le: {report_data['report_generated']}</p>
            
            <div class="summary">
                <h2>Résumé</h2>
                <p>Tests totaux: {report_data['summary']['total_tests']}</p>
                <p>Réussis: <span class="passed">{report_data['summary']['passed']}</span></p>
                <p>Échoués: <span class="failed">{report_data['summary']['failed']}</span></p>
                <p>Ignorés: <span class="skipped">{report_data['summary']['skipped']}</span></p>
                <p>Pourcentage de réussite: {report_data['summary']['pass_percentage']}%</p>
            </div>
        """

        for suite in report_data['suites']:
            html_content += f"""
            <h2>Suite: {suite['name']}</h2>
            <p>Statut: <span class="{suite['status'].lower()}">{suite['status']}</span></p>
            
            <table>
                <tr>
                    <th>Test</th>
                    <th>Statut</th>
                    <th>Tags</th>
                    <th>Durée (s)</th>
                </tr>
            """

            for test in suite['tests']:
                html_content += f"""
                <tr>
                    <td>{test['name']}</td>
                    <td class="{test['status'].lower()}">{test['status']}</td>
                    <td>{', '.join(test['tags'])}</td>
                    <td>{test['elapsed_time']}</td>
                </tr>
                """

            html_content += "</table>"

        html_content += """
        </body>
        </html>
        """

        with open(output_file, 'w') as f:
            f.write(html_content)
