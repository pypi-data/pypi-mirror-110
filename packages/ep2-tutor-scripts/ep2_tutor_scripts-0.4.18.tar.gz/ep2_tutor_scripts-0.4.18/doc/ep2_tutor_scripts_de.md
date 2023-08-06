# EP2 TutorInnnen Skripts

Diese Skripten ermöglichen das Vorbewerten der Teamaufgabe und das Bewerten der Übungstests. 

* `ep2_util` Tool um die Skripten einzurichten und zu testen, sowie Tools, die allgemein verwendet werden können
* `ep2_ex_test` Tool um die Übungstests zu bewerten
* `ep2_eval` Tool um die Vorbewertung durchzuführen

Die Skripten laufen unter `python 3.6` und benötigen `git`. 

## Installation

Die genauen Anweisungen, wie die Skripts zu installieren sind, befinden sich im [Quick Start Guide](quick_start.md) und der [Vorstellunspräsentation](presentation.md). 

Eine fertig gepackte Version kann mit `pip` installiert werden. 
Wenn die Pfade korrekt eingestellt wurden, können die Tools bereits danach von der Kommandozeile ausgeführt werden.

## Dokumentation

Die Dokumentation befindet sich im Ordner `doc/`. Folgende Dateien beschreiben die einzelnen Komponenten:

* `doc/ep2_ex_test_de.md` Das Tool zur Bewertung der Übungstests
* `doc/ep2_csvs_en.md` Ort und Funktionalität der einzelnen CSV Files
* `doc/ep2_eval_de.md` Das Tool zur Vorbewertung der Abgaben
* `doc/ep2_tutor_scripts_de.md` Dieses Dokument
* `doc/ep2_util_de.md` Das Tool um die Skripten einzurichten
* `doc/quick_start.md` Quick Start Guide für TutorInnen, um die Skripte einfach zu installieren

## Abhängigkeiten

Folgende Pakete werden für das Ausführen des Skripts benötigt:

- `gitlab-python` Wrapper für die Gitlab API
- `click` Tool um einfach CLI Anwendungen zu erstellen
- `gitpython`  Git Interface für python (notwendig für checkout, kann evtl. durch die Gitlab API ersetzt werden)
- `cheetah3` Templating Engine
