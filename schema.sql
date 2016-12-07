drop table if exists projects;
create table projects (
  id integer primary key autoincrement,
  title text not null,
  description text not null,
  img text not null,
  language text not null
);
