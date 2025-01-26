create table if not exists concerts (
    id integer primary key autoincrement,
    brand_id integer not null,
    venue_id integer not null,
    date text not null,
    foreign key (band_id) references bands (id),
    foreign key (venue_id) references venues (id)
    );

