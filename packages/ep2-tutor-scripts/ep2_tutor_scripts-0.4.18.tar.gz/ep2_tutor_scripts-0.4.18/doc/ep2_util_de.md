# Utility Skript für EP2 TutorInnen

Dieses Skript bietet einige Funktionen an, um die EP2 TutorInnen Skripte auf einem Rechner einzurichten und zu testen.
Nach der erfolgreichen Installation kann mit `ep2_util init` die korrekte Konfiguration angelegt werden und diese abschließend mit `ep2_util test` getestet werden.

So wie die anderen Skripten, werden Optionen, die nicht angegeben werden abgefragt.
Dadurch müssen z.B. Access Tokens und andere relevante Daten nicht auf der Kommandozeile angegeben werden.

## Kommandos

### `init`

Dieses Kommando legt interaktiv die Konfigurationsdatei für das Skript an. 

```
Options:
  --semester [2019s|2020s|2021s] automatically provides values for gitlab-repo-
                                 prefix and gitlab-url
  --git-home TEXT                directory in which the repositories will be
                                 stored locally  [required]
  --gitlab-url TEXT              url of the gitlab instance
  --gitlab-repo-prefix TEXT      prefix for uebungs repositories
  --gitlab-access-token TEXT     your personal gitlab access token, can be
                                 omitted in the configuration file, but needs to
                                 be provided using EP2_GITLAB_KEY for all other
                                 calls
  --gender [male|female|diverse] the gender you identify with, used for greeting
                                 lines in issues  [required]
  --idea-eval-dir TEXT           directory to copy projects to, so idea will
                                 display them correctly
  --help                         Show this message and exit.
```

Um die Konfiguration für dieses Semester einfach und sicher zu erstellen, kann folgendes Kommando ausgeführt werden:

```shell
ep2_util --semester 2021s --git-home=/path/to/repositories --idea-eval-dir=/path/to/idea/dir
```

Die Option `--semester` muss angegeben werden, wenn `--gitlab-url` und `--gitlab-repo-prefix` nicht angegeben werden! 

Der Gitlab AccessToken wird dann interaktiv abgefragt.

Für genauere Details, siehe [Konfiguration](#konfiguration).

### `test`

Dieses Kommando führt eine Abfrage am Gitlab Server durch und testet damit, ob die Authentifizierung und die URL des Servers stimmen.
Das Kommando gibt `ok` aus, wenn die Konfiguration richtig ist.
Sollte die Konfiguration nicht stimmen, wird eine Fehlermeldung ausgegeben.

### `idea`

Dieses Kommando kopiert ein Repository in das Verzeichnis, dass von IntelliJ IDEA auf Änderungen überwacht wird.

```
Options:
  --project TEXT  matriculation number of the student, whose project should be
                  copied  [required]
  --help          Show this message and exit.
```

Mit diesem Kommando können Projekte schnell in IntelliJ IDEA oder einer anderen IDE betrachtet werden, wenn diese Dateisystemüberwachung unterstützen.

### `tag`

Dieses Kommando taggt alle Projekte einer Gruppe mit dem angegebenen Tag.

```
Options:
  --group TEXT  name of the group  [required]
  --tag TEXT    name of the tag  [required]
  --yes         Confirm the action without prompting.
  --help        Show this message and exit.
```

Bevor die Tags erstellt werden, muss dem aktiv zugestimmt werden. Um dem Fortschritt folgen zu können, wird beim Taggen der Repositories eine Progress Bar angezeigt.

## Konfiguration

Die gesamte lokale Konfiguration wird in einem `ini` File gespeichert.
Standardmäßig wird diese Datei im Benutzerverzeichnis als `.ep2_gitlab` gespeichert. Die Datei kann aber auch über Umgebungsvariablen angepasst werden.
Folgende Umgebungsvariablen werden unterstützt

| Variable         | Default                                           | Verwendung                                                   |
| ---------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| `EP2_PATH`       | `~/`                                              | Basispfad für alle Dateien und Verzeichnisse, die vom Skript angelegt werden. |
| `EP2_CONF_FILE`  | `$EP2_PATH/.ep2_gitlab`                           | Konfigurationsdatei für den Zugang zu Gitlab und die lokalen Dateien. |
| `EP2_GITLAB_KEY` | `Gitlab.AccessToken` in der Datei `EP2_CONF_FILE` | Der AccessToken, mit dem auf Gitlab zugegriffen werden kann. |

Die Konfiguration in der Konfigurationsdatei ist in zwei Abschnitte gegliedert. 

Der Abschnitt *Gitlab* beschreibt die Konfiguration der Gitlab Instanz und beinhaltet zumindest die URL des Gitlab Servers und das Prefix für die Repositories.
Zusätzlich kann der AccessToken für die API in der Konfiguration gespeichert werden, um diesen nicht immer als Umgebungsvariable angeben zu müssen.

Im Abschnitt *Local* wird der Ordner, in dem die Git-Repositories gespeichert werden angegeben und der Ordner, in den Projekte kopiert werden, um diese von IDEA anzeigen zu lassen.

Eine vollständige Konfiguration sieht dann folgendermaßen aus:

```ini
[Gitlab]
AccessToken=ohouewhiufhiwuehfiuwhefiuhweui
URL=https://b3.complang.tuwien.ac.at/
RepoPrefix=ep2/2020s/

[Local]
GitHome=~/tu/ep2_2020
IdeaEvalDir=~/tu/ep2_idea

[Personal]
Gender=[male,female,diverse]
```
