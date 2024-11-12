
CREATE TABLE IF NOT EXISTS sc_sounds_v1.band
(
    id serial NOT NULL,
    bandgearbundle_id integer NOT NULL,
    bandname varchar(40) NOT NULL,
    bandimage_path varchar(255),
    bandsocmedgroupname varchar(40),
    CONSTRAINT band_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_bandname ON sc_sounds_v1.band (bandname);

CREATE TABLE IF NOT EXISTS sc_sounds_v1.artist
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
CREATE INDEX idx_artistname ON sc_sounds_v1.artist (artistname);

CREATE TABLE IF NOT EXISTS sc_sounds_v1.gear
(
    id serial NOT NULL,
    gearbundle_id integer NOT NULL,
    gearname varchar(50) NOT NULL,
    gearimage_path varchar(255),
    CONSTRAINT gear_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_gearname ON sc_sounds_v1.gear (gearname);

CREATE TABLE IF NOT EXISTS sc_sounds_v1.gearbundle
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
CREATE INDEX idx_gearbundlename ON sc_sounds_v1.gearbundle (gearbundlename);

CREATE TABLE IF NOT EXISTS sc_sounds_v1.gearbundlesound
(
    id serial NOT NULL,
    gearbundle_id integer NOT NULL,
    gearbpresetname varchar(50) NOT NULL,
    gearbpreset_path varchar(255),
    gearbpsoundclip_path varchar(255),
    CONSTRAINT gearbundlesound_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_gearbpresetname ON sc_sounds_v1.gearbundlesound (gearbpresetname);

CREATE TABLE IF NOT EXISTS sc_sounds_v1.artistgearbundle
(
    id serial NOT NULL,
    artist_id integer NOT NULL,
    gearbundle_id integer NOT NULL,
    CONSTRAINT artistgearbundle_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sc_sounds_v1.bandgearbundle
(
    id serial NOT NULL,
    band_id integer NOT NULL,
    gearbundle_id integer NOT NULL,
    CONSTRAINT bandgearbundle_pkey PRIMARY KEY (id)
);

ALTER TABLE sc_sounds_v1.artist
    ADD CONSTRAINT fk_artist_band
    FOREIGN KEY (artistband_id) REFERENCES sc_sounds_v1.band(id);

ALTER TABLE sc_sounds_v1.artist
    ADD CONSTRAINT fk_artist_gearbundle
    FOREIGN KEY (artistgearbundle_id) REFERENCES sc_sounds_v1.gearbundle(id);

ALTER TABLE sc_sounds_v1.gear
    ADD CONSTRAINT fk_gear_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES sc_sounds_v1.gearbundle(id);

ALTER TABLE sc_sounds_v1.gearbundle
    ADD CONSTRAINT fk_gearbundle_band
    FOREIGN KEY (gearbundleband_id) REFERENCES sc_sounds_v1.band(id);

ALTER TABLE sc_sounds_v1.gearbundle
    ADD CONSTRAINT fk_gearbundle_artist
    FOREIGN KEY (gearbundleartist_id) REFERENCES sc_sounds_v1.artist(id);

ALTER TABLE sc_sounds_v1.gearbundle
    ADD CONSTRAINT fk_gearbundle_gearbundlesound
    FOREIGN KEY (gearbundlesound_id) REFERENCES sc_sounds_v1.gearbundlesound(id);

--ALTER TABLE sc_sounds_v1.gearbundlesound
--    ADD CONSTRAINT fk_gearbundlesound_gearbundle
--    FOREIGN KEY (gearbundle_id) REFERENCES sc_sounds_v1.gearbundle(id)
--    DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE sc_sounds_v1.artistgearbundle
    ADD CONSTRAINT fk_artistgearbundle_artist
    FOREIGN KEY (artist_id) REFERENCES sc_sounds_v1.artist(id);

ALTER TABLE sc_sounds_v1.artistgearbundle
    ADD CONSTRAINT fk_artistgearbundle_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES sc_sounds_v1.gearbundle(id);

ALTER TABLE sc_sounds_v1.bandgearbundle
    ADD CONSTRAINT fk_bandgearbundle_band
    FOREIGN KEY (band_id) REFERENCES sc_sounds_v1.band(id);

ALTER TABLE sc_sounds_v1.bandgearbundle
    ADD CONSTRAINT fk_bandgearbundle_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES sc_sounds_v1.gearbundle(id);