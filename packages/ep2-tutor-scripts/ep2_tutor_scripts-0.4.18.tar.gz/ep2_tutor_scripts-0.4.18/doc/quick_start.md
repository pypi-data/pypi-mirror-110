# Quick Start Guide

This document describes the setup process for the ad-hoc exercise submission and grading script. 
It assumes, you have basic knowledge of the command line, and the following tools installed:

* `python 3.6`, `pip`
* `git`
* `ssh`

## Installation

The package has been uploaded to the python package index. Installation is therefore possible without downloading files from any repositories.

This script requires python 3.6 to run. 
As python 2.7 has reached end of life on January 1st 2020, this tool will only support python 3.6 or newer. 
Therefore `pip` is assumed to use python >=3.6.

```shell
pip install --user ep2-tutor-scripts=0.4.3
```

and `pip` will download the dependencies and install the packages locally for your user. `pip` will also create a launch script for the scripts.

### Linux/Unix Installation

To be able to use the script directly, add the following two lines to your `~/.bashrc` (or other shell configuration file)

```bash
export PY_USER_BIN=$(python -c 'import site; print(site.USER_BASE + "/bin")')
export PATH=$PY_USER_BIN:$PATH

export EP2_GIT_HOME=~/ep2/git_home
export EP2_IDEA_EVAL_PATH=~/ep2/idea
```

After adding the exports to your `~/.bashrc`, either restart your shell or `source ~/.bashrc`.  
The latter keys will be used in setting up the tools.

### Windows Installation

On Windows add the result of `python -c 'import site; print(site.USER_BASE + "\\Scripts")'` to your `PATH` variable. 
If the installation of all dependencies was successful, the scripts should now be available.

After the tool presentation it was found, that this path is not always valid. 
If the tools cannot be found after the installation (and a logout, because Windows), try to open the tools as python modules:

```shell
ep2_util    -> python -m ep2_tutors.ep2_util
ep2_eval    -> python -m ep2_tutors.ep2_eval
ep2_ex_test -> python -m ep2_tutors.ep2_ex_test
```

If you need to use the above commands you have to replace the command with the call to python in all further commands.

To resolve the issue encoding issue with Windows set `PYTHONUTF8=1` before every call to the tools.
You can do this for your entire (Powershell) session using:

```shell
$env:PYTHONUTF8 = '1'
```

There seems to be a problem with the Command Prompt (CMD) and encrypted key files when using the tools.
Either create a new key and configure it using `~/.ssh/config` or use a different sheel.
Generally: use Powershell, the Git Bash or Windows Subsystem for Linux instead.

## Updates

To install updates, use the same commands as above (you might have to adjust the version), but include `--upgrade` in the command.

## Configuration

To configure the script run `ep2_util init` once. You can configure the script to store your Gitlab access token or to read it from an environment variable for every run.

If you want to configure the script, you can omit the option `--gitlab-access-token`, to not have it present in your shell history. The script will prompt you for your access token anyway.
You can create your Gitlab AccessToken at [https://b3.complang.tuwien.ac.at/profile/personal_access_tokens](https://b3.complang.tuwien.ac.at/profile/personal_access_tokens).
The token requires scope `api`.

The simplest way to configure the script for this year is to run the following command.

```bash
ep2_util init --semester=2021s \
				--git-home=$EP2_GIT_HOME \
				--idea-eval-dir=$EP2_IDEA_EVAL_PATH
```

`--semester=2021s` uses defaults for most other values which are valid for this semester.
It is important to either enter this option or to supply `--gitlab-url` and `--gitlab-repo-prefix`.

`--git-home` is used for locally storing the git repository you need to work with.

`--idea-eval-dir` is the folder, student projects are copied to, when `pre_eval idea` is called. (Copy a project to the directory which is monitored by IntelliJIDEA for quick evaluation).

> **Attention: The contents of the folder are deleted with every copy, DO NOT use a folder, that has any different purposes.**

## Exercise Evaluation

The command for evaluation is `ep2_eval`. 
It will help you checkout all necessary projects, load them into IDEA (or any other IDE of your choice), keep track of your progress and the grading.

### Checkout

To checkout the submissions for an exercise run

```shell
ep2_eval checkout --group <group> --ue <ue>
```

This command will clone or pull the working repositories of all submission for the given exercise and checkout the tag for the exercise. 

### Grading "Single" Exercises

After you have decided on how to grade a submission run

```shell
ep2_eval grade --group <group> --ue <ue> --grading <grading> --student <student>\
				[--student-feedback <feedback> --solution-remarks <remarks>]
```

`feedback` and `remarks` can be omitted if you don't want to add any feedback or remarks. 
The command will still prompt for their values, but they can be left empty.
`grading` consists of `+`, `~` and `-`. 
`+` through `-` offer a grading gradient. (100% - 50% - 0%)
The number of sub-grades is verified with the files in the `ex_info` folder.

For simplicity, you can also run

```shell
ep2_eval grade --group <group> --ue <ue>
```

The script will prompt you for the student, your grading decision, feedback and remarks for the solution. 

On success, the script will have updated the grading in the evaluation file. 
If you have entered student feedback, the feedback will be visible in the issue.

To check which submissions still need to be graded you can run

```shell
ep2_eval list ungraded --group <group> --ue <ue>
```

This command will output `empty` if no ungraded teams remain.

### Grading Team Exercise

The command to grade a team exercise is similar to the normal grading command.
The only difference is the `--points` option, which is used instead of `--grading` and `--tasks`.

```shell
ep2_eval grade --group <group> --ue <ue> --points <points> --student <student>\
				[--student-feedback <feedback> --solution-remarks <remarks>]
```

`points` is the amount of points you want to grade the submission.
The grading is also used for the other member(s) of the team.

### Creating Issues

To create the issues in the students repositories run

```shell
ep2_eval submit --group <group> --ue <ue>
```

This will print all issues, that will be created by this tool. Please verify all issues before continuing.

To actually create the issues, you will have to enter a challenge. The challenge is printed at the beginning of the output (running this in an empty shell is probably preferable) and consist of three uppercase letters and/or numbers.

After you have entered the challenge the tool will display a simple progress bar that tracks the issue creation. If any errors occured, they will be printed after the issues have been created.

## Exercise Tests

The command for the ad-hoc exercises is `ep2_ex_test`.
It will help you to do the submission of the exercise, the checkout of the necessary projects and the grading.

### Tag

At the end of the an exercise test, tag all repositories of the group by calling

```shell
ep2_ex_test tag --group <group> --ue <ue>
```

To keep the time window between hand-in and  tagging as narrow as possible, the tool tags all repositories of all students of the group at the beginning of the command. The progress is displayed with a progress bar. To avoid tagging too early, a simple confirmation prompt is shown before the tagging is done.

> **Start tagging only after all students have handed in the exercise tests!**

The latest commit in the working repository will be tagged with the current exercise number.

### Submission

To enter the information, which students worked together as a team call

```shell
ep2_ex_test submission --group <group> --ue <ue>
```

The script will start to prompt matriculation numbers. First of the working repository owner, then the editor and finally the matriculation number of a third person. The last one is optional and exists only for the rare case, a three person team is required.

```
Mat.No. Repo:   01234567
Mat.No. Writer: 12345678
Mat.No. Third:
```

All entered matriculation numbers are checked against the matriculation numbers of the students in the group. If a matriculation number cannot be found, an error message is displayed and you can enter the number again.

Submission stops after an empty working repository owner has been entered. Submission can be paused and continued at a later time. 

After submission, push the tutor repository, so others can access the submission file.

If you want to directly perform checkout and grading run the submission command with the `--idea` and `--grade` flags. This will load the current project of the exercise into the folder monitored by IntelliJ IDEA and wait for your grading input before continuing with the submission input.

From the second exercise onward the tool will propose the student id of the second member. This usually is the partner for the last exercise test. Single exercises are skipped for this auto fill mechanic.

### Checkout

To checkout the submissions for an exercise run

```shell
ep2_ex_test checkout --group <group> --ue <ue>
```

This command will clone or pull the working repositories of all submission for the given exercise and checkout the tag for the exercise.

If someone else has entered the submissions or you are using a different device to checkout the submissions, remember to pull the tutor repository.

### Grading

After checkout you can start grading the submissions. After you have decided on how to grade a submission run

```shell
ep2_ex_test grade --group <group> --ue <ue> --points <points> --repo-owner <working repo owner>
```

For simplicity you can also run

```shell
ep2_ex_test grade --group <group> --ue <ue>
```

The script will prompt you for points and the working repository owner. If you enter student feedback, the feedback will also be visible in the issue. On success, the script will have updated the grading in the submissions file.

To check which teams still need to be graded you can run

```shell
ep2_ex_test list ungraded --group <group> --ue <ue>
```

This command will output `empty` if no ungraded teams remain.

### Creating Issues

To create the issues in the students repositories run

```shell
ep2_ex_test submit --group <group> --ue <ue>
```

This will print all issues, that will be created by this tool. Please verify all issues before continuing.

To actually create the issues, you will have to enter a challenge. The challenge is printed at the beginning of the output (running this in an empty shell is probably preferable) and consist of three uppercase letters and/or numbers.

After you have entered the challenge the tool will display a simple progress bar that tracks the issue creation. If any errors occured, they will be printed after the issues have been created.