create table if not exists bands (
    id integer primary key autoincrement,
    name text not null,
    hometown text not null
);