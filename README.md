# Quinzena

[Català](#català) · [English](#english)

---

## Català

**Quinzena** és un calendari mensual que separa cada mes en dues quinzenes: la **1a quinzena** (dies 1 a 15) i la **2a quinzena** (del 16 a l'últim dia del mes). Inclou dues versions que comparteixen la mateixa lògica: una per al **terminal** i una **aplicació gràfica**. Els noms de mesos i dies són en català. No necessita cap dependència externa.

### Característiques

- Calendari mensual dividit en 1a i 2a quinzena.
- El dia d'avui queda marcat entre claudàtors, amb un resum de la quinzena actual.
- Versió de terminal amb opcions per triar mes i any.
- Aplicació gràfica (Tkinter) amb disseny inspirat en el Calendari de macOS.
- Dreceres de teclat a la versió gràfica: fletxes esquerra i dreta per canviar de mes, `Inici` o `T` per tornar a avui i `Esc` per sortir.

### Requisits

- Python 3.9 o superior.
- Tkinter (només per a l'aplicació gràfica; ve inclòs amb la majoria d'instal·lacions de Python).

### Com utilitzar-lo

```bash
git clone https://github.com/albertbosch/quinzena.git
cd quinzena

# Terminal: mes actual
python3 quinzena.py

# Terminal: un mes i un any concrets
python3 quinzena.py --month 11 --year 2026

# Terminal: sense marcar el dia d'avui
python3 quinzena.py --no-today

# Aplicació gràfica
python3 quinzena_gui.py
```

### Exemple de sortida

```text
Novembre 2026 - 1a QUINZENA
  Dl   Dt   Dc   Dj   Dv   Ds   Dg
                                1
  2    3    4    5    6    7    8
  9   10   11   12   13   14   15

Novembre 2026 - 2a QUINZENA
  Dl   Dt   Dc   Dj   Dv   Ds   Dg
 16  [17]  18   19   20   21   22
 23   24   25   26   27   28   29
 30

Avui és dia 17: 2a quinzena (16-30 de novembre).
```

### Crear una aplicació per a macOS i Linux

L'aplicació gràfica es pot empaquetar amb [PyInstaller](https://pyinstaller.org). Cal construir-la **a cada sistema operatiu**: PyInstaller no fa compilació creuada, així que el paquet de macOS es fa en un Mac i el de Linux en un Linux.

**macOS (`Quinzena.app`)**

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --windowed --name Quinzena quinzena_gui.py
```

L'app queda a `dist/Quinzena.app`. Pots arrossegar-la a la carpeta Aplicacions. Com que no està signada, la primera vegada macOS pot avisar-te: fes clic dret sobre l'app, tria Obrir i confirma.

**Linux**

```bash
sudo -S -p '' apt install python3-tk python3-venv   # Debian/Ubuntu; a altres distribucions, el paquet equivalent de Tkinter
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --onefile --windowed --name quinzena quinzena_gui.py
```

L'executable queda a `dist/quinzena`. Per tenir-lo al menú d'aplicacions, crea `~/.local/share/applications/quinzena.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Quinzena
Exec=/ruta/completa/a/dist/quinzena
Terminal=false
Categories=Utility;
```

> Les carpetes `build/` i `dist/` i el fitxer `Quinzena.spec` que genera PyInstaller no formen part del repositori.

### Estructura

```
quinzena.py       -> lògica compartida i versió de terminal
quinzena_gui.py   -> aplicació gràfica (Tkinter)
```

### Llicència

Aquest projecte està sota llicència [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.ca): pots usar-lo i adaptar-lo citant-ne l'autoria, però no amb finalitats comercials.

---

## English

**Quinzena** is a monthly calendar that splits each month into two fortnights: the **1st fortnight** (days 1 to 15) and the **2nd fortnight** (day 16 to the last day of the month). It ships in two versions that share the same logic: a **terminal** version and a **graphical app**. Month and day names are in Catalan. It has no external dependencies.

### Features

- Monthly calendar divided into a 1st and a 2nd fortnight.
- Today is marked with square brackets, plus a summary of the current fortnight.
- Terminal version with options to choose the month and year.
- Graphical app (Tkinter) with a design inspired by the macOS Calendar.
- Keyboard shortcuts in the graphical version: left and right arrows to change month, `Home` or `T` to jump back to today and `Esc` to quit.

### Requirements

- Python 3.9 or later.
- Tkinter (only for the graphical app; included with most Python installations).

### Getting started

```bash
git clone https://github.com/albertbosch/quinzena.git
cd quinzena

# Terminal: current month
python3 quinzena.py

# Terminal: a specific month and year
python3 quinzena.py --month 11 --year 2026

# Terminal: do not mark today
python3 quinzena.py --no-today

# Graphical app
python3 quinzena_gui.py
```

### Example output

```text
Novembre 2026 - 1a QUINZENA
  Dl   Dt   Dc   Dj   Dv   Ds   Dg
                                1
  2    3    4    5    6    7    8
  9   10   11   12   13   14   15

Novembre 2026 - 2a QUINZENA
  Dl   Dt   Dc   Dj   Dv   Ds   Dg
 16  [17]  18   19   20   21   22
 23   24   25   26   27   28   29
 30

Avui és dia 17: 2a quinzena (16-30 de novembre).
```

### Building an app for macOS and Linux

The graphical app can be packaged with [PyInstaller](https://pyinstaller.org). You must build **on each operating system**: PyInstaller does not cross-compile, so the macOS package is built on a Mac and the Linux one on Linux.

**macOS (`Quinzena.app`)**

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --windowed --name Quinzena quinzena_gui.py
```

The app ends up in `dist/Quinzena.app`; drag it to your Applications folder. Since it is not signed, macOS may warn you the first time: right-click the app, choose Open and confirm.

**Linux**

```bash
sudo -S -p '' apt install python3-tk python3-venv   # Debian/Ubuntu; on other distros, the equivalent Tkinter package
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --onefile --windowed --name quinzena quinzena_gui.py
```

The executable ends up in `dist/quinzena`. To add it to your application menu, create `~/.local/share/applications/quinzena.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Quinzena
Exec=/full/path/to/dist/quinzena
Terminal=false
Categories=Utility;
```

> The `build/` and `dist/` folders and the `Quinzena.spec` file generated by PyInstaller are not part of the repository.

### Structure

```
quinzena.py       -> shared logic and terminal version
quinzena_gui.py   -> graphical app (Tkinter)
```

### License

This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): you may use and adapt it with attribution, but not for commercial purposes.
