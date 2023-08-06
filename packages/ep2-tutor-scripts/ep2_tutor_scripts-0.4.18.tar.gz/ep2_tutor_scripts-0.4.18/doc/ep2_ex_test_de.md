Übungstest Abgabe und Bewertung
===

Dieses Tool behandelt die Abgabe und Bewertung der Übungstests. 

## Workflow

Das Bewerten eines Übungstests wird in folgende Schritte unterteilt.

1. **Taggen**:  Der letzte Commit wird auf Gitlab getaggt um die Abgabe später verlässlich verwenden zu können.
2. **Eintragen**: Die Teams dieser Ad-hoc Übung werden in den Abgabelisten eingetragen.
3. **Checkout**: Die getaggten Commits werden gepullt und in den entsprechenden Verzeichnissen ausgecheckt.
4. **Bewerten**: Nach der Bewertung trägt der/die Tutor*in, dass Ergebnis in eine Abgabenliste ein.
5. **Informieren**: Die eingetragenen Ergebnisse werden nochmals überprüft und anschließend werden die Issues in allen Repositories erzeugt.

Dieser Workflow kann für alle Übungen durchgeführt werden.

> **ACHTUNG**: Nachdem dieses Jahr die Teams bereits vorab bekannt sind, arbeiten diese Kommandos auf Basis der Teams!
> Die meisten Eingaben erwarten sich den Namen eines Teams, nicht mehr die Matrikelnummern von Studierenden.

## Kommandos

Aus dem Workflow ergeben sich folgende Kommandos für die Kernfunktionalität:

* `tag` taggt alle Projekte auf Gitlab mit dem übungsspezifischem Tag
* `submission` interaktives Kommando, um die Abgaben einzutragen
* `checkout` Kommando, um alle Abgaben herunterzuladen
* `grade` Kommando zur Bewertung einer einzelnen Abgabe
* `submit` Kommando zur abschließenden Überprüfung und dem Erzeugen der Issues

Zusätzlich können mit der Zeit noch weitere Kommandos eingebaut werden, um das Bewerten und die Einrichtung zu vereinfachen:

* `list`  gibt Listen bestimmter Daten aus
  * `ungraded` Gibt die unbewerteten Abgaben einer Gruppe auf

### `tag`

Dieses Kommando taggt alle Projekte einer Gruppe mit dem Tag der Übung (`ex_test_<ue>`). 

```
Options:
  --group TEXT        name of the group  [required]
  --ue TEXT           number of the exercise, WITHOUT leading zero  [required]
  --late / --on-time  if submission was late
  --yes               Confirm the action without prompting.
  --help              Show this message and exit.
```

Bevor die Tags erstellt werden, muss dem aktiv zugestimmt werden. 
Um dem Fortschritt folgen zu können, wird beim Taggen der Repositories eine Progress Bar angezeigt.

Mit der Option `--late` können Abgaben als zu spät abgegeben gekennzeichnet werden.
Es werden wieder alle Projekte getaggt, diesmal jedoch mit dem Tag `ex_test_<ue>_late`.
Um nachzusehen, welche Projekte zu spät abgegeben wurden, können die Commits verglichen werden, die getaggt wurden.
Wurde derselbe Commit mit beiden Tags getaggt, wurde nicht zu spät abgegeben.
Wenn es jedoch verschiedene Commits sein sollten, wurde der Commit mit `adhoc_<ue>_late` später abgegeben.

### `submission`

Ein interaktives Kommando, um die Abgaben einzutragen.
Für jedes Team kann das Repository angegeben werden, in dem die Lösung bearbeitet wurde.

Wenn das Kommando mit der Flag `--grade` aufgerufen wird, wird auch nach der Eingabe der Rollen das Grading abgefragt.
In diesem Modus muss weder `checkout` noch `grade` aufgerufen werden.

Wenn die Flag `--idea` angegeben wird, wird das Projekt in den IntelliJ-Ordner gelinkt, bevor die Bewertung abgefragt wird.

```
Options:
  --group TEXT          name of the group  [required]
  --ue TEXT             number of the exercise, WITHOUT leading zero
                        [required]
  --idea / --no-idea    load project into the folder, that is monitored by
                        IntelliJ Idea
  --grade / --no-grade  also add grading with submission
  --help                Show this message and exit.
```

Es wird folgende Ausgabe angezeigt:

```
Enter repository owner for team test
0: 11777729
1: 11777728
Repo Owner (0, 1, s): 
```

Mit der Eingabe einer Zahl kann die Person angegeben werden, indem der Übungstest bearbeitet wurde.
Wenn `s` eingegeben wird, wird dieses Team übersprungen und kann manuell hinzugefügt werden. (siehe [man-submission](#man-submission))

Die Bewertung kann eine Zahl im Bereich `0 - 4` sein.
Das Feedback wird den Studierenden im Issue angezeigt und die Remarks können von den Übungsgruppenleitern verwendet werden.

### `man-checkout`

Mit diesem Kommando können Abgaben manuell hinzugefügt werden.
Dies kann notwendig sein, wenn z.B. ein Teammitglied einer Gruppe fehlt und die verbleibende Person bei einem anderen Team mitarbeitet.

In diesem Fall kann das Team in dem abgegeben wurde mit dem interaktiven Kommando bewertet werden und die dritte Person im Nachhinein manuell hinzugefügt werden.

Bestehende Bewertungen für ein Team werden für manuell hinzugefügte Personen übernommen.

```shell
Options:
  --group TEXT        name of the group [required]
  --ue INTEGER        number of the exercise, WITHOUT leading zero [required]
  --student TEXT      student id of the student, that should be graded [required]
  --role [o|w|t]      the role of the student for this exercise test
  --team TEXT         the name of the team to add (this will not be verified!)
  --help              Show this message and exit.
```

Um eine Person mit der Matrikelnummer `11777727` als dritte Person zum Team `test` hinzuzufügen, würde das Kommando folgendermaßen aufgerufen werden:

```shell
ep2_ex_text man-submission --group test --ue 1 --student 11777727 --role t --team test
```

### `checkout`

Lädt alle Arbeitsrepositories einer Gruppe herunter und checkt die Abgabe zur entsprechenden Übung aus.

```
Options:
  --group TEXT  name of the group  [required]
  --ue TEXT     number of the exercise, WITHOUT leading zero  [required]
  --help        Show this message and exit.
```

Das entsprechende CSV wird geöffnet und die Arbeitsrepositories aus diesem ausgelesen.
Wenn diese bereits auf dem lokalen Rechner existieren wird `git fetch` durchgeführt, wenn nicht wird das Repository geklont.
Abschließend wird der entsprechende Tag der Übung ausgecheckt.

Wenn das CSV nicht existiert, wird eine Fehlermeldung ausgegeben.

### `grade`

Führt die Bewertung einer einzelnen Abgabe durch.

```
Options:
  --team TEXT        the name of the team or the student id of the
                     student that should be graded  [required]
  --points TEXT      points graded for this exercise  [required]
  --group TEXT       name of the group  [required]
  --ue TEXT          number of the exercise, WITHOUT leading zero  [required]
  --remarks TEXT     optional remarks for the submission
  --help             Show this message and exit.
```

Im CSV der Gruppe wird die Anzahl der Punkte aktualisiert.
Wenn das CSV noch nicht angelegt wurde, wird dies wie bei `checkout` gehandhabt.

Um ein schnelles Eintragen zu ermöglichen, müssen nicht alle Parameter beim Aufruf des Programms angegeben werden.
Nicht angegebene Parameter werden durch entsprechende Prompts abgefragt.
Um eine Benotung für eine Abgabe der Gruppe `test` für die 4te Übung einzutragen, kann das Skript folgendermaßen aufgerufen werden:

```shell
ep2_ex_test grade --group test --ue 4
```

Die Punkte und das Team werden dann mit Prompts abgefragt.

Wenn das Eintragen der Punkte funktioniert hat, wird `ok` ausgegeben.
Ansonsten werden entsprechende Fehlermeldungen ausgegeben.

### `submit`

Listet alle Issues auf, die erzeugt werden würden und ermöglicht das automatische Erzeugen aller Issues auf Gitlab.

```
Options:
  --group TEXT  name of the group  [required]
  --ue TEXT     number of the exercise, WITHOUT leading zero  [required]
  --help        Show this message and exit.
```

Zu Beginn der Ausgabe wir eine Challenge ausgegeben.
Diese muss am Schluss eingegeben werden, um die Issues zu erzeugen.
Dadurch soll verhindert werden, dass durch unbeabsichtigte Eingaben die Issues vorzeitig erstellt werden.
Solange die Challenge nicht eingegeben wurde, kann das Kommando nebenwirkungsfrei beendet werden.

Für die Issues wird das Template `templates/ex_test.tmpl` aus dem TutorInnen Repository verwendet.
Änderungen im lokalen Repository sind möglich und werden in den erzeugten Issues auch angezeigt.

Eine Challenge besteht aus drei zufälligen Zeichen [A-Z1-9] und wird auf Terminals, die dies unterstützen Fett angezeigt.

Nach dem Eingeben der korrekten Challenge werden die Issues erzeugt.
Um den Fortschritt verfolgen zu können, wird eine einfache Progress Bar angezeigt.

Sollten während dem Erzeugen der Issues Fehler auftreten, werden diese am Schluss ausgegeben.

**Während dem submitten wird die Abgabedatei neu geschrieben, um sie kompatibel mit den Tools, die sie weiterverabeiten, zu machen.
Nach diesem Schritt unbedingt die Dateien nochmal pushen!**

### `list ungraded`

Dieses Kommando gibt alle unbewerteten Abgaben einer Übung einer Gruppe aus.

```
Options:
  --group TEXT  name of the group  [required]
  --ue TEXT     number of the exercise, WITHOUT leading zero  [required]
  --help        Show this message and exit.
```

Dazu wird das CSV durchgegangen und die Teams der Einträge mit keiner Bewertung ausgegeben.

Wenn das CSV noch nicht angelegt wurde, wird dies wie bei `checkout` gehandhabt.

Wenn keine Abgaben unbewertet sind, wird `empty` ausgeben, ansonsten eine Liste von unbewerteten Teams.
