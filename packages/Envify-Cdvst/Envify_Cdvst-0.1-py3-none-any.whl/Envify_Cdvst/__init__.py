import os
import re
import logging
import yaml
from typing import List, Dict, Optional

class ConfigLoaderError(Exception):
    """
    Benutzerdefinierte Exception für Fehler beim Laden von Konfigurationen.
    """
    pass

class ConfigLoader:
    """
    Eine Klasse zum Laden von Konfigurationsdateien und Umgebungsvariablen.
    """

    def __init__(self, env_file_formats: List[str], default_env: Optional[str] = None,
                 logger: Optional[logging.Logger] = None, excluded_lines: Optional[List[str]] = None,
                 separator: Optional[str] = None) -> None:
        """
        Erzeugt eine Instanz von ConfigLoader.

        :param env_file_formats: Liste der zu berücksichtigenden Dateiformate.
        :param default_env: Optionale Standardeinstellung für die Umgebung.
        :param logger: Optionale Logger-Instanz für Logging.
        :param excluded_lines: Optionale Liste der auszuschließenden Zeilen.
        :param separator: Optionales Trennzeichen für das Parsen von Umgebungsvariablen.
        """
        self.env_vars: Dict[str, str] = {}
        self.env_file_formats = env_file_formats
        self.default_env = default_env
        self.logger = logger or logging.getLogger(__name__)
        self.excluded_lines = excluded_lines or ['#', '']
        self.separator = separator or '='

    def load(self, paths: List[str]):
        """
        Lädt Umgebungsvariablen aus den angegebenen Dateipfaden.

        :param paths: Liste der zu ladenden Dateipfade.
        :throws ConfigLoaderError: Wenn keine Dateipfade angegeben wurden oder beim Lesen einer Datei ein Fehler auftritt.
        """
        if not paths:
            raise ConfigLoaderError("Keine Dateipfade zum Laden der Konfiguration angegeben.")
        for path in paths:
            if not os.path.isfile(path):
                self.logger.warning(f"Dateipfad {path} ist nicht gültig.")
                continue
            for format in self.env_file_formats:
                if path.endswith(format):
                    self.logger.info(f"Lade Umgebungsvariablen für Dateipfad {path}.")
                    try:
                        with open(path, 'r') as f:
                            raw_contents = f.read()
                    except Exception as e:
                        raise ConfigLoaderError(f"Fehler beim Laden von Umgebungsvariablen aus {path}: {str(e)}")
                    contents = self._parse_env_vars(raw_contents)
                    if self.default_env and self.default_env in contents:
                        default_vars = self._parse_env_vars(contents[self.default_env])
                        contents.update(default_vars)
                        contents.pop(self.default_env)
                    for excluded_line in self.excluded_lines:
                        contents.pop(excluded_line, None)
                    self.env_vars.update(contents)
    
    def _parse_env_vars(self, raw_contents: str) -> Dict[str, str]:
        """
        Parst Umgebungsvariablen aus den rohen Inhalten einer Datei.

        :param raw_contents: Rohe Inhalte einer Datei.
        :return: Ein Dictionary der geparsten Umgebungsvariablen.
        """
        env_vars = {}
        lines = raw_contents.split('\n')
        for line in lines:
            if any(excluded_line in line for excluded_line in self.excluded_lines):
                continue
            try:
                key, value = line.split(self.separator, 1)
                env_vars[key.strip()] = value.strip()
            except ValueError:
                self.logger.warning(f"Konnte die Zeile {line} nicht in Schlüssel/Wert aufteilen.")
        return env_vars

    def create_config_from_template(self, template_path: str, dest_path: str, replacements: Dict[str, str]):
        """
        Erstellt eine Konfigurationsdatei basierend auf einer Vorlage.

        :param template_path: Pfad zur Vorlagendatei.
        :param dest_path: Zielweg für die neue Konfigurationsdatei.
        :param replacements: Ein Dictionary der zu ersetzenden Werte in der Vorlage.
        :throws ConfigLoaderError: Wenn beim Lesen der Vorlage oder beim Schreiben der neuen Datei ein Fehler auftritt.
        """
        try:
            with open(template_path, 'r') as f:
                template = f.read()
        except Exception as e:
            raise ConfigLoaderError(f"Fehler beim Lesen der Vorlage {template_path}: {str(e)}")
        for key, value in replacements.items():
            template = template.replace(f"${{{key}}}", value)
        try:
            with open(dest_path, 'w') as f:
                f.write(template)
        except Exception as e:
            raise ConfigLoaderError(f"Fehler beim Schreiben der neuen Konfigurationsdatei {dest_path}: {str(e)}")

    def get_env_var(self, var_name: str) -> Optional[str]:
        """
        Gibt den Wert einer Umgebungsvariable zurück.

        :param var_name: Name der Umgebungsvariable.
        :return: Der Wert der Umgebungsvariable oder None, wenn sie nicht gefunden wurde.
        """
        return self.env_vars.get(var_name)

    def set_env_var(self, var_name: str, var_value: str):
        """
        Setzt den Wert einer Umgebungsvariable.

        :param var_name: Name der Umgebungsvariable.
        :param var_value: Der zu setzende Wert.
        """
        self.env_vars[var_name] = var_value

    def delete_env_var(self, var_name: str):
        """
        Löscht eine Umgebungsvariable.

        :param var_name: Name der Umgebungsvariable.
        """
        self.env_vars.pop(var_name, None)
