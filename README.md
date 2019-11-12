# timetracker

A time tracker for personal usage, written in python, for command-line usage

# Prerequisites

-  python 2.7


# How to start

1. Setup database 

    python setup.py
  
2. Copy created sqlite database `timer.db` to your %USERPROFILE% directory

   Check %USERPROFILE% env variable exists

3. Start timetracker

    python tracker.py

    type `help`


# Storage

Uses an Sqlite database to store all task data.
Database file `timer.db` is located in directory %USERPROFILE%.
When you close timer applic

# List of available commands


    #<id>          reschedule an existing task using its id
    add,a          add a new task and set it to active
	adjust         adjust time of a task
    clear,cl       clear all tasks
    commit,ci      commit a task by id
    done           set task to done
	exit           exit application
    export,exp     export data (current day) as JSON
    help,h         this help
    list,l,ls      list all available tasks (ls all; ls yd; ls)
    pause,p        pause tasks
    push           push all done tasks to store and remove them from current list
    rename,ren     rename a task by id
    remove,rm      delete task by id
    status,st      status information

# Command description

## schedule a task

Syntax: #`task-id`

Set a task with given task-id as active

## add

Add a new task

Alias: add, a

Syntax:  add `taskname`

A new task is created and set as active. Its status will become ON.

## adjust

Syntax: adjust `task-id` `time`

Adjust time of a task. Specify a time value in seconds. The value can be negative or positive.

## clear

Remove all tasks from current list

Alias: clear, c

Tasks in the storage are not removed with this command.

## commit

Commits a task by id 

Alias: commit, ci  

Syntax: commit `task-id`

Commit time from given task to storage, add a new task with the same taskname to current task list 
and set new task as active.

## done 

Set a task to complete

Syntax: done `task-id`

Sets a task' status to DONE. Hide it in current list by default.
Set pause task as active task.

## exit

Alias: exit, q

Write schedules to storage and exit application.

## help

Alias: help, h

Print help and usage

## list 

List all current tasks 

Alias: list, ls

Syntax: 

	ls      // list tasks from current list  
	
	ls all  // list alls tasks from current list, also the DONE tasks 
	
	ls yd   // list all tasks you created yesterday (loading them from storage)

## pause

Pause current tasks

Alias: pause, p

Syntax: pause `task-id`

Set default pause task as active task

## push

Push all tasks with status DONE to storage and remove them from current list

## rename

Syntax: rename `task-id` `new-taskname`

Rename a task

## remove

Alias: remove, rm

Syntax: remove `task-id`

Delete a task permanently.

## status

Alias: status, st

Print status information

# Task status

ON - an active task 

OFF - a task is paused

DONE - a task is done

# Console Output

    time tracker V0.9.10
    
    20:10 > ls
       id  spend     upd   created  status  name
        1  00:00   20:10     20:10  ACTIVE  pause

	20:10 > add New Task
      added new task #2

	  20:10 > add Second Task
      added new task #3

    20:10 > ls
       id  spend     upd   created  status  name
        3  00:00   20:10     20:10  ACTIVE  Second Task
        1  00:00   20:10     20:10  ACTIVE  pause
        2  00:00   20:10     20:10  ACTIVE  New Task

    20:10 > done 2
      set task #2 to done

    20:10 > ls
       id  spend     upd   created  status  name
        3  00:00   20:10     20:10  ACTIVE  Second Task
        1  00:00   20:10     20:10  ACTIVE  pause

    20:10 > ls all
       id  spend     upd   created  status  name
        3  00:00   20:11     20:10  ACTIVE  Second Task
        1  00:00   20:10     20:10  ACTIVE  pause
        2  00:00   20:10     20:10  DONE    New Task


    20:11 > status

      active:       #3 Second Task
      pause:        00:00h
      worktime:     00:00h
      started:      20:10
      tasks:        3
    20:11 > exit
