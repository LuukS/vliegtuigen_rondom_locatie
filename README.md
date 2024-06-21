# vliegtuigen_rondom_locatie
Ophalen van de vliegtuiggegevens van sensornet en omzetten van locatie naar WGS waarna alleen de gegevens binnen een blok rondom een locatie worden opgeslagen in een database

Voor het omzetten van WGS84 coordinaten naar RD wordt gebruik gemaakt van Python code van Jan van der Laan (https://github.com/djvanderlaan/rijksdriehoek).


Om data in een MySQL data op te slaan moet het bestand config.py.example hernoemd worden naar config.py en vervolgens de juiste waarden ingevuld worden zodat de database benaderd kan worden.
In het bestand config.py moeten de volgende gegevens ingevuld worden:
- database = MySQL of SQLite. Indien SQLite gekozen wordt zullen de andere gegevens niet gebruikt worden. In de directory data wordt een SQLite database gemaakt welke daarna gevuld moet worden met de drie tabellen. Er is een lege database met de drie tabellen in de data directory opgenomen, deze moet hernoemd worden van vliegtuigen_leeg.db in vliegtuigen.db.
SQLite voorbeeld:
class Config(object):
  database = "SQLite"
  DATABASE_CONFIG = {
          'host': '<ip_address>',
          'port': '<port_number>',
          'user': '<username>',
          'password': '<password>',
          'dbname': '<database_name>',
  }

Indien MySQL ingevuld gekozen wordt moet de toegangsgegevens van de database worden ingevuld. Dit zijn het ip adres, het poort nummer, de gebruikersnaam, het wachtwoord en de naam van de database.
MySQL voorbeeld:
class Config(object):
  database = "MySQL"
  DATABASE_CONFIG = {
          'host': '127.0.0.1',
          'port': '3306',
          'user': 'vliegtuig',
          'password': 'vleugels',
          'dbname': 'vliegtuigen',
  }

Het account waarmee de verbinding gemaakt wordt heeft SELECT en INSERT rechten nodig. SELECT rechten om te kijken of de benodigde 3 tabellen beschikbaar zijn en INSERT rechten om de gegevens in de tabellen op te slaan.

Met behulp van het bestand create_tables_mysql.sql uit de directory SQL zijn de drie benodigde tabellen te maken in MySQL. Met het bestand create_tables.sql zijn de tabellen in SQLite te maken.
