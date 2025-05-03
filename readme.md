# Startup Guide

## Clone de repo

Clone de repo naar VS Code en bekijk alle bestanden om een overzicht te krijgen van de verschillende backend en front-end bestanden.

## Virtual Environment

### Aanmaken van een nieuwe venv

Zoals tijdens elk project van FSWD maken we een nieuwe venv aan door in de terminal volgend commando in te tikken:

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `py -m venv --system-site-packages venv_fswd`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `python3 -m venv --system-site-packages venv_fswd`

Sluit hierna in VS Code de terminal en open een nieuwe en check of je in je venv aan het werken bent.

### Installeren van de benodigde packages via pip

Eerst zullen we nu de nodige packages installeren op onze nieuw gemaakte venv.
Voor het gemak hebben we alle nodige packages opgeslagen in het bestand requirements.txt.

Het installeren van de nodige packages kan met het volgende commando:

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `pip install -r ./requirements.txt`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `pip install -r requirements.txt`