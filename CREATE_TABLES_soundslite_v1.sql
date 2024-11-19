-- Create band table
CREATE TABLE IF NOT EXISTS band
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bandgearbundle_id INTEGER NOT NULL,
    bandname VARCHAR(40) NOT NULL,
    bandimage_path VARCHAR(255),
    bandsocmedgroupname VARCHAR(40)
);

-- Create index on bandname
CREATE INDEX idx_bandname ON band (bandname);

-- Create artist table
CREATE TABLE IF NOT EXISTS artist
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artistband_id INTEGER NOT NULL,
    artistgearbundle_id INTEGER NOT NULL,
    artistname VARCHAR(40) NOT NULL,
    artistpassw VARCHAR(80) NOT NULL,
    artistrole_1 INTEGER NOT NULL,
    artistrole_2 INTEGER NOT NULL
);

-- Create index on artistname
CREATE INDEX idx_artistname ON artist (artistname);

-- Create gear table
CREATE TABLE IF NOT EXISTS gear
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gearbundle_id INTEGER NOT NULL,
    gearname VARCHAR(50) NOT NULL,
    gearquantity INTEGER NOT NULL,
    gearimage_path VARCHAR(255)
);

-- Create index on gearname
CREATE INDEX idx_gearname ON gear (gearname);

-- Create gearbundle table
CREATE TABLE IF NOT EXISTS gearbundle
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gearbundleband_id INTEGER,
    gearbundleartist_id INTEGER NOT NULL,
    gearbundlesound_id INTEGER NOT NULL,
    gearbundlename VARCHAR(50) NOT NULL,
    gearbundleimage_path VARCHAR(255),
    gearbundleuserguide VARCHAR(255) NOT NULL
);

-- Create index on gearbundlename
CREATE INDEX idx_gearbundlename ON gearbundle (gearbundlename);

-- Create gearbundlesound table
CREATE TABLE IF NOT EXISTS gearbundlesound
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gearbundle_id INTEGER NOT NULL,
    gearbpresetname VARCHAR(50) NOT NULL,
    gearbpreset_path VARCHAR(255),
    gearbpsoundclip_path VARCHAR(255)
);

-- Create index on gearbpresetname
CREATE INDEX idx_gearbpresetname ON gearbundlesound (gearbpresetname);

-- Create artistgearbundle table
CREATE TABLE IF NOT EXISTS artistgearbundle
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER NOT NULL,
    gearbundle_id INTEGER NOT NULL
);

-- Create bandgearbundle table
CREATE TABLE IF NOT EXISTS bandgearbundle
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER NOT NULL,
    gearbundle_id INTEGER NOT NULL
);

-- Add foreign key to artist table
ALTER TABLE artist
    ADD CONSTRAINT fk_artist_band
    FOREIGN KEY (artistband_id) REFERENCES band(id);

ALTER TABLE artist
    ADD CONSTRAINT fk_artist_gearbundle
    FOREIGN KEY (artistgearbundle_id) REFERENCES gearbundle(id);

-- Add foreign key to gear table
ALTER TABLE gear
    ADD CONSTRAINT fk_gear_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES gearbundle(id);

-- Add foreign key to gearbundle table
ALTER TABLE gearbundle
    ADD CONSTRAINT fk_gearbundle_band
    FOREIGN KEY (gearbundleband_id) REFERENCES band(id);

ALTER TABLE gearbundle
    ADD CONSTRAINT fk_gearbundle_artist
    FOREIGN KEY (gearbundleartist_id) REFERENCES artist(id);

ALTER TABLE gearbundle
    ADD CONSTRAINT fk_gearbundle_gearbundlesound
    FOREIGN KEY (gearbundlesound_id) REFERENCES gearbundlesound(id);

-- Add foreign key to gearbundlesound table
ALTER TABLE gearbundlesound
    ADD CONSTRAINT fk_gearbundlesound_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES gearbundle(id);

-- Add foreign key to artistgearbundle table
ALTER TABLE artistgearbundle
    ADD CONSTRAINT fk_artistgearbundle_artist
    FOREIGN KEY (artist_id) REFERENCES artist(id);

ALTER TABLE artistgearbundle
    ADD CONSTRAINT fk_artistgearbundle_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES gearbundle(id);

-- Add foreign key to bandgearbundle table
ALTER TABLE bandgearbundle
    ADD CONSTRAINT fk_bandgearbundle_band
    FOREIGN KEY (band_id) REFERENCES band(id);

ALTER TABLE bandgearbundle
    ADD CONSTRAINT fk_bandgearbundle_gearbundle
    FOREIGN KEY (gearbundle_id) REFERENCES gearbundle(id);

