# timetracker

A personal time tracker written in python

# How to start

1. Setup database 

    python setup.py 
  
2. Copy created sqlite database `timer.db` to your HOME directory

3. Start timer

    python timer.py
    
    type `help`


# Store

This tool uses a local sqlite database file to store tracking data

# List of available commands


    #<id>          reschedule an existing task using its id
    add,a          add and start a new task
    clear,cl       clear all tasks
    commit,ci      commit a task with specific id
    done           set task to done
    export,exp     export current data
    help,h         this help
    list,l,ls      list all available tasks
    pause,p        pause tasks
    push           push all done tasks to store and remove them from current list
    rename,ren     rename a task
    remove,rm      remove task
    status,st      status about current task
