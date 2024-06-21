-- Maak meetpunten tabel
create table test_db.meetpunten (
meetpuntid varchar(10),
straat varchar(255),
postcode varchar(10),
plaats varchar(255),
dba integer,
status varchar(20),
_size integer,
_alpha integer,
point varchar(255),
point_rd varchar(255),
_url varchar(255),
_fillcolor varchar(255),
_symbol varchar(255),
_scalemax integer,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- Maak hoge_vliegtuigen tabel
create table hoge_vliegtuigen (
altitude varchar(255),
speed varchar(255),
callsign varchar(255),
operator varchar(255),
type varchar(255),
registration varchar(255),
_alpha integer,
_angle integer,
_symbol varchar(255),
_Size integer,
point_rd varchar(255),
point varchar(255),
_fillcolor varchar(255),
_linecolor varchar(255),
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- Maak lage_vliegtuigen tabel
create table lage_vliegtuigen (
altitude varchar(255),
speed varchar(255),
callsign varchar(255),
operator varchar(255),
type varchar(255),
registration varchar(255),
_alpha integer,
_angle integer,
_symbol varchar(255),
_Size integer,
point_rd varchar(255),
point varchar(255),
_fillcolor varchar(255),
_linecolor varchar(255),
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
