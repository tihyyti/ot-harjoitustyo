CREATE TABLE IF NOT EXISTS sounds_v1.band
(
    id serial NOT NULL,
    bandgearbundle_id integer NOT NULL,
    bandname varchar(40) NOT NULL,
    bandimage_path varchar(255),
    bandsocmedgroupname varchar(40),
    CONSTRAINT band_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_bandname ON band (bandname);

CREATE TABLE IF NOT EXISTS sounds_v1.artist
(
    id serial NOT NULL,
    artistband_id integer NOT NULL,
    artistgearbundle_id integer NOT NULL,
    artistname varchar(40) NOT NULL,
    artistpassw varchar(80) NOT NULL,
    artistrole_1 integer NOT NULL,
    artistrole_2 integer NOT NULL,
    CONSTRAINT artist_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_artistname ON artist (artistname);

CREATE TABLE IF NOT EXISTS sounds_v1.gear
(
    id serial NOT NULL,
    gearbundle_id integer NOT NULL,
    gearname varchar(50) NOT NULL,
	gearquantity integer NOT NULL,
    gearimage_path varchar(255),
    CONSTRAINT gear_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_gearname ON gear (gearname);

CREATE TABLE IF NOT EXISTS sounds_v1.gearbundle
(
    id serial NOT NULL,
    gearbundleband_id integer,
    gearbundleartist_id integer NOT NULL,
    gearbundlesound_id integer NOT NULL,
    gearbundlename varchar(50) NOT NULL,
    gearbundleimage_path varchar(255),
    gearbundleuserguide varchar(255) NOT NULL,
    CONSTRAINT gearbundle_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_gearbundlename ON gearbundle (gearbundlename);

CREATE TABLE IF NOT EXISTS sounds_v1.gearbundlesound
(
    id serial NOT NULL,
    gearbundle_id integer NOT NULL,
    gearbpresetname varchar(50) NOT NULL,
    gearbpreset_path varchar(255),
    gearbpsoundclip_path varchar(255),
    CONSTRAINT gearbundlesound_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_gearbpresetname ON gearbundlesound (gearbpresetname);

CREATE TABLE IF NOT EXISTS sounds_v1.artistgearbundle
(
    id serial NOT NULL,
    artist_id integer NOT NULL,
    gearbundle_id integer NOT NULL,
    CONSTRAINT artistgearbundle_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sounds_v1.bandgearbundle
(
    id serial NOT NULL,
    band_id integer NOT NULL,
    gearbundle_id integer NOT NULL,
    CONSTRAINT bandgearbundle_pkey PRIMARY KEY (id)
);
