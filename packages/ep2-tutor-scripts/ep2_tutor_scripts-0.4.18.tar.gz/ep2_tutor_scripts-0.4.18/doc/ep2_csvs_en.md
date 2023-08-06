# Tutor Data

This document describes the structure of the data files in the tutor repository.
The tutor tools operate on these files, which are always located in each group's directory.

**Files:**

| File | Description |
| ---- | ----------- |
| `students.csv` | Stores basic information about students (name, student id, ....) |
| `groups.csv` | Used to offer predictions for exercise tests and used for group exercise |
| `exercise_<ex. no>.csv` | Attendance and pre-evaluation for exercise \<ex. no \> |
| `ex_test_<ex. no>.csv` | Results for the exercise tests per group |

## `students.csv`

| Field                | Valid Values               | Description                                     |
| -------------------- | -------------------------- | ----------------------------------------------- |
| `id`         | Valid matriculation number | The matriculation number of the student |
| `last_name`  | Any valid UTF-8 string | The surname of the student                      |
| `first_name` | Any valid UTF-8 string | The name of the student                         |
| `gender`     | `male`/`female`/`diverse` | The gender of the student, used for salutations |
| `email` | Any valid UTF-8 string | Not validated e-mail address of the student |

## `groups.csv`

| Field | Valid Values | Description |
| ----- | ------------ | ----------- |
| `group_id` | `<ex_group_name>_00` with incrementing numbers starting from `01` | The name/id of the group |
| `member_0` | Valid student id | First member |
| `member_1` | Valid student id | Second member |
| `member_2` | Valid student id, emtpy | Optional third member |

## `exercise_<ex. no>.csv`

| Field                | Valid Values               | Description                             |
| -------------------- | -------------------------- | --------------------------------------- |
| `id`         | Valid matriculation number | The matriculation number of the student |
| `attendend`          | `0` = no/`1` = yes         | The student has attended the exercise   |
| `grading`           | (list of `+`/`~`/`-`)/`_`        | Result of tutor evaluation                |
| `pre_eval_ex_<x>` | `(?<points>\d*)\/(?<of>\d*)` where `of` &geq; `points` | The points the student got for the indiviual exercise |
| `remarks` |  | Remarks for the lecturer |
| `feedback` |  | Feedback for the student |

`remarks` and `feedback` should only be used for the team exercise (ex. 7), but will also be shown when used with other exercises if present. 

 ## `ex_test_<ex. no>.csv`

| Field                    | Valid Values                      | Description                                                  |
| ------------------------ | --------------------------------- | ------------------------------------------------------------ |
| `id`             | Valid matriculation number        | Mat. No. of student, in whose repository the exercise was done. |
| `role`     | `o`= owner/`e`= editor/`t`= third | Role, this student had in this ad-hoc exercise               |
| `points`   | Number/`_`                        | Points awarded for this ad-hoc exercise                      |
| `team`     | Same as id of group | The team, this student is a part in                          |
| `remarks`  |                                   | Remarks for yourself (lecturer will not read it)                                     |
| `feedback` |                                   | Feedback for the student                                     |