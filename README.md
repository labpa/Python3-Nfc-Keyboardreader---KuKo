# Python3 Nfc Keyboardreader

## Installation auf Ubuntu.2204
### 1. System Update
`sudo apt update`
### 2. Python installieren
Über das Terminal Python3 installieren.  
`sudo apt-get install python3`

### 3. Erforderliche Python-Pakete installieren
Installation **pyscard** und **pynput**:  
`pip3 install pyscard pynput`

### 4. Systempakete installieren
Installation *pcsc-tools**, **pcscd**, **libusb**:   
`sudo apt install pcsc-tools pcscd libusb-dev`

Installation **ccid**:  
`sudo apt -y install libacsccid1`

Installation **libnfc**:  
`sudo apt -y install libnfc-dev`

### 5. PCSC neu starten
Neustart **pcscd**:  
`sudo service pcscd restart`
### 6. System neu starten
Neustart des Rechners:
`sudo shutdown -r now`


### Skript ausführen

## NFC-Reader Testen
Um zu Testen ob der Angesteckte NFC-Reader verwendet werden kann,
im Terminal folgendes eingaben:  
`sudo pcsc_scan`

