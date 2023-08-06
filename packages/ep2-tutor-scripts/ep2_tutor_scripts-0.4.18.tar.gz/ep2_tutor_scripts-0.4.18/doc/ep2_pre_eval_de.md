# EP2 Vorbewertungsskript

Dieses Skript automatisiert die Schritte der Vorbewertung und organisiert die Speicherung der Daten im Tutor*innen Repository.

## Workflow

Die Abgaben werden am Dienstag um 12:00 vom Technik-Team getaggt und dann automatisiert vorbewertet.
Dabei werden auch die notwendigen Vorbewertungsdateien und diverse andere Dateien angelegt.
Sobald das Testen abgeschlossen ist, wird per E-Mail informiert, dass die Abgaben zur Bewertung bereit sind.

Dann sind folgende Schritte durchzuführen:

* **Checkout** Die Abgaben werden vom Git Repository heruntergeladen und in den lokalen Repositories zum Bewerten mit dem korrekten Tag ausgecheckt.
* **Vorbewertung** Die Dateien werden durchgeschaut, ob die Aufgabenstellung erfüllt wurde. Optional kann dieser Schritt in einer IDE durchgeführt werden.
* **Eintragen der Vorbewertung** Das Ergebnis der Vorbewertung wird eingetragen und ein Issue erstellt, in dem die Studierenden über das Ergebnis der Vorberwertung informiert werden.

Auf diesem Workflow ergeben sich auch die Kommandos des Skripts.

## Kommandos

Um den Workflow abzubilden, unterstütz das Skript folgende Kommandos:

* `checkout` Klont oder pullt die Repositories und checked den entsprechenden Tag aus
* `idea` kopiert die Inhalte eines Repositories in einen Ordner. Dieser Ordner kann in IntelliJ IDEA geöffnet werden, um ein schnelles Durchschauen der Abgabe zu ermöglichen.
* `grade` bewertet eine Abgabe, trägt das Ergebnis in das CSV ein und erstellt ein Issue mit dem Ergebnis, sowie optionalen Anmerkungen

Zusätzlich gibt es noch folgendes Kommando, die nicht direkt im Workflow verwendet werden

* `list` Listet bestimmte Elemente auf
  * `ungraded` gibt die Liste von unbewerteten Abgaben zu einer Übung aus

### `checkout`

Dieses Kommando klont oder pullt die Repositories zu einer Übung einer Gruppe und checked den entsprechenden Übungstag aus. 
Zusätzlich legt `checkout` eine Anwesenheitsliste und eine Bewertungsliste an. Sollte bereits eine Anwesenheitsliste oder eine Bewertungsliste bestehen, wird keine neue angelegt.

```
Options:
  --group TEXT  name of the group  [required]
  --ue TEXT     number of the exercise, WITHOUT leading zero  [required]
  --help        Show this message and exit.
```

Diese Dateien befinden sich im TutorInnen Repository im Gruppenverzeichnis und heißen `attendance_<ue>.csv` bzw. `pre_eval_<ue>.csv`.

In der Anwesenheitsliste befindet sich das Feld `attended`, in dem eingetragen werden kann, ob Studierende während der Übung anwesend waren. 
Dazu wird der Wert von `0` auf `1` geändert.

In der Bewertungsliste befindet sich eine Spalte, in der die Bewertung eingetragen werden kann, sowie Spalten für Rückmeldungen an die Studierenden und eine Spalte für die Anmerkugen an die Übungsgruppenleitenden. 

### `grade`

Dieses Kommando trägt die Vorbewertung in das entsprechende CSV ein.

```
Options:
  --group TEXT             name of the group  [required]
  --ue TEXT                number of the exercise, WITHOUT leading zero
                           [required]
  --student TEXT           matriculation of the student, that should be graded
                           [required]
  --student-feedback TEXT  feedback for the student, will be part of the
                           created issue
  --solution-remarks TEXT  remarks for the lecturer (keep short)
  --grading TEXT           grade for the submission
  --points INTEGER RANGE   points for team exercise
  --help                   Show this message and exit.
  --tasks INTEGER          number of tasks for this exercise
```

Das Feedback, dass in `--student-feedback` angegeben wird, wird im Text des Issues angezeigt. 
Anmerkungen, die in `--solution-remarks` angegeben werden, werden nur intern gespeichert und stehen die Übungsgruppenleitenden während der Übung zur Verfügung.

`grading` ist eine Liste von Bewertungen, die direkt aneinandergehängt werden. 
Das erste Zeichen wird für Task 1, das zweite für Task 2, ... verwendet. 
Mit `tasks` kann zudem eine Überprüfung der Anzahl der Bewertungen durchgeführt werden.

Im StudentInnenfeedback wird zu den Zeichen noch folgende Beschreibung angehängt:

| Bewertung | Beschreibung                                     |
| --------- | ------------------------------------------------ |
| `-`       | Lösung nicht zielführend                         |
| `~`       | es gibt Fehler, die nicht nur Kleinigkeiten sind |
| `+`       | bis auf Kleinigkeiten richtig gelöst             |

`points` wird verwendet, um die Punkte für die Teamaufgabe einzutragen. Dies ist nur für die Übung 7 möglich und bei anderen
Übungen wird das Tool beendet. Wenn `points` und `grading` gleichzeitig angegeben werden, wird das Tool ebenfalls abgebrochen.


### `grade-interactive`

Mit diesem Kommando können die Vorbewertungen interaktiv eingetragen werden. 
Die Abgabe der Studierenden wird gemeinsam mit den Ergebnissen der Vorbewertung und der Angabe in das IDEA Verzeichnis geladen.

> **ACHTUNG:** Das Tool verwendet Symlinks um die Dateien ins IDEA Verzeichnis zu laden. 
> Unter Windows benötigen Symlinks besondere Berechtigungen die unter Windows 10 Pro eingerichtet werden können.
> ([https://stackoverflow.com/a/65504258](https://stackoverflow.com/a/65504258))
> 
> Unter anderen Windows 10 Varianten (Home, ...) müssen die Tools als Administrator ausgeführt werden, damit die Symlinks erstellt werden können.
> 
> Unter POSIX Systemen ist eine Schreibberechtigung für das Verzeichnis ausreichend.

```
Options:
  --group TEXT        name of the group  [required]
  --ue INTEGER        number of the exercise, WITHOUT leading zero  [required]
  --idea / --no-idea  load project into the folder, that is monitored by
                      IntelliJ Idea
  --help              Show this message and exit.
```

Um eine Gruppe zu bewerten wird das Kommando mit der Gruppe und der gewünschten Übungsnummer aufgerufen.
Das Tool beginnt dann für bislang nicht bewertete Studierende Bewertungen abzufragen.
Wenn `--idea` angegeben wird, wird das Projekt auch ins IDEA Verzeichnis geladen. 
Neben dem Sourcecode der Angabe in `src/` wird die Angabe nach `angabe/` und auch das Ergebnis der automatisierten Vorbewertung in die Datei `pre_eval_<ue>.yml` geladen.

Um die Bewertung zu vereinfachen werden die verschiedenen Unterpunkte der Bewertung angezeigt.
Für die erste Aufgabe im Semester 2021S sieht das folgendermaßen aus:

```
Gradable subtasks:
    1. Korrekte Sichtbarkeit von Objektvariablen in `Vector3` und `Body` und Initialisierung mittels Konstruktoren (1.0 P)
    2. Korrekte Objektmethoden in `Vector3` (1.0 P)
    3. Korrekte Objektmethoden in `Body` (1.5 P)
    4. Korrekte Verwendung der Objektmethoden in `Simulation` (1.0 P)
    5. Korrekte Beantwortung der Zusatzfragen (0.5 P)
Grading (q for quit):
```

Die Bewertung besteht aus einem Zeichen pro Unterpunkt (im obigen Beispiel also 5).
Die Bedeutung der Zeichen kann der obigen Tabelle entnommen werden.
Neben der Beschreibung des Unterpunkts werden auch die maximal erreichbaren Punkte angezeigt.

Um die Bewertung zu unterbrechen kann statt einer Bewertung `q` eingegeben werden.
Die Bewertung wird bei einem neuerlichen Aufruf an der Stelle fortgesetzt.

Nach der Eingabe der Bewertung können Feedback und Anmerkungen wie gewohnt eingetragen werden.

Wenn alle Studierenden bewertet wurden, beendet sich der interaktive Modus automatisch.
Wenn der interaktive Modus aufgerufen wird, nachdem bereits alle Studierenden bewertet wurden, kann keine weitere Bewertung mehr eingetragen werden.
Um zusätzliche Bewertungen einzutragen, kann das Kommando `ep2_eval grade` verwendet werden.

### `submit`

Listet alle Issues auf, die erzeugt werden würden und ermöglicht das automatische Erzeugen aller Issues auf Gitlab.

```
Options:
  --group TEXT  name of the group  [required]
  --ue TEXT     number of the exercise, WITHOUT leading zero  [required]
  --help        Show this message and exit.
```

Zu Beginn der Ausgabe wir eine Challenge ausgegeben.
Diese muss am Schluss eingegeben werden, um die Issues zu erzeugen. Dadurch soll verhindert werden, dass durch unbeabsichtigte Eingaben die Issues vorzeitig erstellt werden.
Solange die Challenge nicht eingegeben wurde, kann das Kommando nebenwirkungsfrei beendet werden.

Für die Issues wird das Template `templates/eval.tmpl` aus dem TutorInnen Repository verwendet.
Änderungen im lokalem Repository sind möglich und werden in den erzeugten Issues auch angezeigt.

Eine Challenge besteht aus drei zufälligen Zeichen [A-Z1-9] und wird auf Terminals, die dies unterstützen Fett angezeigt.

Nach dem Eingeben der korrekten Challenge werden die Issues erzeugt.
Um den Fortschritt verfolgen zu können, wird eine einfache Progress Bar angezeigt.

Sollten während dem Erzeugen der Issues Fehler auftreten, werden diese am Schluss ausgegeben.

### `list ungraded`

Dieses Kommando gibt alle unbewerteten Abgaben einer Übung einer Gruppe aus.

```
Options:
  --group TEXT  name of the group  [required]
  --ue TEXT     number of the exercise, WITHOUT leading zero  [required]
  --help        Show this message and exit.
```

Dazu wird das CSV durchgegangen und die Arbeitsrepos der Einträge mit leerer Bewertung ausgegeben.

Wenn das CSV noch nicht angelegt wurde, wird dies wie bei `checkout` gehandhabt.

Wenn keine Abgaben unbewertet sind, wird `empty` ausgeben, ansonsten eine Liste von Matrikelnummern, der Repositories, die noch bewertet werden müssen.