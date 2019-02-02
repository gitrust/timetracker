create table task(
  id integer PRIMARY KEY,
  taskid integer not null,
  name char(255) not null,
  startdate int not null,
  duration integer not null,
  tasktype char(15) not null,
  taskstatus char(15) not null,
  createddate integer not null
);