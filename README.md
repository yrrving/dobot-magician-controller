# Dobot Magician Controller

En enkel lokal app för att ansluta till en `Dobot Magician`, spara positioner och köra rörelser i loop.

## Ladda ner

Mac:
- `DobotKontroll_v2.zip`

Windows:
- `DobotKontroll_PC_buildkit.zip`

Releases:
- Kommer att finnas på projektets Releases-sida

## Funktioner

- Anslut till Dobot via USB
- Välj port och klicka `Connect`
- Kontrollera anslutningen med `Test Pose`
- Spara flera positioner för armen
- Kör de sparade positionerna i loop
- Stoppa loopen och koppla från armen

## Innehåll

- `DobotKontroll_v2.zip`: färdig Mac-app
- `dobot_manual.rtf`: manual för Mac
- `pc_manual.txt`: manual för Windows
- `source/dobot_ui.py`: plattformsoberoende källkod för Mac och Windows
- `windows/build_windows.bat`: bygg Windows-versionen på en Windows-dator
- `windows/requirements-windows.txt`: Python-beroenden för Windows-bygget

## Windows

Windows-versionen byggs på en Windows-dator genom att köra:

```bat
build_windows.bat
```

Den färdiga filen blir:

```text
windows\dist\DobotKontroll_PC.exe
```

## Användning

1. Koppla in Dobot med ström och USB.
2. Starta appen.
3. Klicka `Refresh`.
4. Välj port och klicka `Connect`.
5. Klicka `Test Pose`.
6. Flytta armen till önskade lägen och klicka `Spara punkt`.
7. Klicka `Start loop` för att köra rörelsen i loop.

## Viktigt

- Mac-appen är byggd för macOS.
- Windows-appen måste byggas på en Windows-dator.
- Ingen internetuppkoppling behövs för att använda verktyget.
- Inga konton behövs.
