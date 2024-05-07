#! /usr/bin/env python3
import re
import argparse
from smartcard.System import readers
import datetime
import sys
from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

# ACS ACR122U NFC-Lesegerät
# Überraschenderweise ist es ein Handshake-Protokoll, um Daten vom Tag zu erhalten
# Sie senden dem Lesegerät einen Befehl, um Daten zurückzuerhalten
# Der folgende Befehl basiert auf dem "API-Treiberhandbuch des ACR122U NFC-Kontaktlosen Smartcard-Lesegeräts"
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Handshake-Befehl zum Initiieren des Datenübertragungsprozesses

# Liste aller verfügbarer NFC-Lesegeräte
r = readers()
print("Verfügbare Lesegeräte:", r)

# Überprüfen, ob die Liste der Lesegeräte leer ist
if not r:
    print("Keine Lesegeräte gefunden")
    sys.exit(1)

# Wählen des ersten Lesegeräts aus der Liste
reader = r[0]
waiting_for_beacon = 1

# Funktion zum Parsen von Daten in einen hexadezimalen String
def stringParser(dataCurr):
    if isinstance(dataCurr, tuple):
        # Wenn die Daten als Tupel vorliegen (Daten, Statuscode, Sonstiges)
        temp = dataCurr[0]
        code = dataCurr[1]
    else:
        # Wenn die Daten direkt vorliegen (ohne Statuscode)
        temp = dataCurr
        code = 0

    dataCurr = ''

    # Konvertierung der Daten in einen hexadezimalen String
    for val in temp:
        dataCurr += format(val, '#04x')[2:]  # Die Hexadezimaldarstellung jedes Bytes anhängen

    dataCurr = dataCurr.upper()  # Großschreibung des resultierenden Strings

    # Rückgabe des Datenstrings, wenn der Statuscode erfolgreich ist (144)
    if code == 144:
        return dataCurr

# Funktion zum Lesen der UID des NFC-Tags
def readUID():
    global lastUid
    readingLoop = 1
    while readingLoop:
        try:
            print("Versuche, Verbindung herzustellen...")
            connection = reader.createConnection()
            print("Verbindung erfolgreich hergestellt.")
            print("Versuche, zu verbinden...")
            status_connection = connection.connect()
            print("Verbindungsstatus:", status_connection)
            # Senden des Befehls zum Lesen der UID des NFC-Tags
            print("Sende Befehl zum Lesen der UID...")
            resp = connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
            print("Antwort vom Lesegerät:", resp)
            dataCurr = stringParser(resp)

            # Wenn die UID erfolgreich gelesen wurde
            if dataCurr is not None:
                print("UID erfolgreich gelesen:", dataCurr)
                # Tastatureingabe der UID gefolgt von der Enter-Taste
                keyboard.type(dataCurr)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                break
            else:
                # Fehlerbehandlung, wenn beim Parsen der Antwort etwas schiefgeht
                print("Fehler: Etwas ist beim Parsen der Antwort schiefgegangen.")
                break
        except Exception as e:
            if waiting_for_beacon == 1:
                continue
            else:
                readingLoop = 0
                print("Es ist ein Fehler aufgetreten:", str(e))
                break

# Endlosschleife zum kontinuierlichen Lesen von UID
while True:
    readUID()
    sleep(1)
