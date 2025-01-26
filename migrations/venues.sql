create table if not exists venues (
    id integer  primary key autoincrement,
    title text not null,
    city text not null
);