# Gumshoe Habit Tracker

[![Version](https://img.shields.io/pypi/v/gumshoe-cli)](https://img.shields.io/pypi/v/gumshoe-cli)
[![License](https://img.shields.io/github/license/philipcsaplar/gumshoe-cli)](https://github.com/philipcsaplar/gumshoe-cli/blob/master/LICENSE)

Your habit tracking command line tool.

---

## Installation

Gumshoe requires `python 3.7+` to be available on your system. You can install
`gumshoe` like any other python package using the pip installation package manager.

```shell
 pip install gumshoe-cli
```
## Commands overview

Here we will take a quick look at each `gumshoe` command.

### Creating a habit

The create habit command consists of the following.

####Expects

* A habit name of one or two words.
* An optional --quota to specify the amount of times the habit should be done in a given period.
* A period to specify whether the habit should be done daily, weekly or monthly.

####Syntax

```shell
Usage: gumshoe create [OPTIONS] NAME... PERIOD

  The create command creates new habits and will expect the following
  arguments and options:

  name, name of the task(habit) - required

  period, expecting one of the following , daily, weekly, monthly - required

Options:
  -q, --quota INTEGER  Use this option to increase your quota of times you
                       need to complete a habit, default is 1
  --help               Show this message and exit.

````

####Example
```shell
$ gumshoe create gym -q 2 weekly

New habit has been created!
```

### Complete a habit

Each habit you create will need to be completed in its given period to accumulate a streak. the complete command can accept a quota option to complete more habits task in one command.

####Expects

* The habit name.
* An optional --quota to specify the amount of times the habit should be completed.

####Syntax

```shell
Usage: gumshoe complete [OPTIONS] NAME...

  The complete command adds a completion time and date for a specified habit.
  Specify the name of the habit you wish to updated.

Options:
  -q, --quota INTEGER  Amount of quota your wish to complete.
  --help               Show this message and exit.

```

####Example
```shell
$ gumshoe complete gym

Habit gym completed 1 times
```

### Remove a habit

You can use the gumshoe remove command to remove a habit and all its tracking data.

####Expects

* A habit name.

####Syntax
```shell
Usage: gumshoe remove [OPTIONS] NAME...

  The remove command removes a habits and all its associated activities.
  Please specify the name of the habit you wish to remove. You can use the
  gumshoe show command to list all habits to get the habits name.

Options:
  --confirmation TEXT  Confirmation that you want to remove your habit.
  --help               Show this message and exit.
```
####Example
```shell
> gumshoe remove gym

Do you really want to remove this habit [y/n]: y
Habit removed successfully!

```

### Show a habit details

Using the gumshoe shot command you can view all habits created, view habits in a specific periodicity, view a habits current streak and also its longest streak.

Activity reporting follows below convention by default. Use the `-l` switch if
you'd like a date based view.

- <span style="color:green">■</span> Indicates your target has been met!
- ■ Indicates your have only partially met your target.
- □ Indicates no activity has been recorded.

####Expects

* Option -n for the habit name.
* Option -p for periodicity.
* Option -m for detailed information use with the -n option

####Syntax
```shell
Usage: gumshoe show [OPTIONS]

  The show commands allows you to see your progress on a specify habit as well 
  as view all habits you have created. You can also view your current 
  streak and longest streaks on a given habit

Options:
  -n, --name TEXT    Use this option to specify the name of the habit you wish
                     to show
  -m, --more         Use this option with the -n option to show more details
  -p, --period TEXT  Use this option to show all habits in a specific period,
                     example daily, weekly or monthly
  --help             Show this message and exit.
```
####Example
```shell
> gumshoe show -n gym

┌──────┬────────┬────────────────┬────────────────┬────────┬────────────────────────────────────┐
│ Name │ Target │ Current Streak │ Longest Streak │ Period │ Weekly Activities                  │
├──────┼────────┼────────────────┼────────────────┼────────┼────────────────────────────────────┤
│ gym  │ 2      │ 0              │ 0              │ weekly │ ■ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □  │
└──────┴────────┴────────────────┴────────────────┴────────┴────────────────────────────────────┘

> gumshoe show -p all

┌──────┬────────┬─────────────┐
│ Name │ Target │ Period      │
├──────┼────────┼─────────────┤
│ gym  │ 2      │ weekly      │
└──────┴────────┴─────────────┘

> gumshoe show -n gym -m

┌──────┬────────┬────────┬────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Name │ Target │ Streak │ Period │ 21-06-07 │ 21-05-31 │ 21-05-24 │ 21-05-17 │ 21-05-10 │ 21-05-03 │ 21-04-26 │ 21-04-19 │ 21-04-12 │ 21-04-05 │ 21-03-29 │ 21-03-22 │ 21-03-15 │ 21-03-08 │ 21-03-01 │ 21-02-22 │ 21-02-15 │
├──────┼────────┼────────┼────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ gym  │ 2      │ 0      │ weekly │ 1        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │ 0        │
└──────┴────────┴────────┴────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

```
