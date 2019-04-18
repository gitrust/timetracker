# timetracker

A time tracker for personal usage, written in python, command-line

# How to start

1. Setup database 

    python setup.py
  
2. Copy created sqlite database `timer.db` to your HOME directory

3. Start timetracker

    python tracker.py
    type `help`


# Store

Uses a Sqlite database to store all task data

# List of available commands


    #<id>          reschedule an existing task using its id
    add,a          add and start a new task
    clear,cl       clear all tasks
    commit,ci      commit a task with specific id
    done           set task to done
    export,exp     export data (current day) as JSON
    help,h         this help
    list,l,ls      list all available tasks (ls all; ls yesterday; ls)
    pause,p        pause tasks
    push           push all done tasks to store and remove them from current list
    rename,ren     rename a task
    remove,rm      remove task
    status,st      status about current task

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
