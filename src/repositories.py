import sqlite3

class BandRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_band(self, bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO band (bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname)
                VALUES (?, ?, ?, ?)
            ''', (bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname))
            conn.commit()

    def read_band(self, band_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM band WHERE id = ?', (band_id,))
            return cursor.fetchone()

    def update_band(self, band_id, bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE band
                SET bandgearbundle_id = ?, bandname = ?, bandimage_path = ?, bandsocmedgroupname = ?
                WHERE id = ?
            ''', (bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname, band_id))
            conn.commit()

    def delete_band(self, band_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM band WHERE id = ?', (band_id,))
            conn.commit()

class ArtistRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_artist(self, artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO artist (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2))
            conn.commit()

    def read_artist(self, artist_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM artist WHERE id = ?', (artist_id,))
            return cursor.fetchone()

    def update_artist(self, artist_id, artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE artist
                SET artistband_id = ?, artistgearbundle_id = ?, artistname = ?, artistpassw = ?, artistrole_1 = ?, artistrole_2 = ?
                WHERE id = ?
            ''', (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2, artist_id))
            conn.commit()

    def delete_artist(self, artist_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM artist WHERE id = ?', (artist_id,))
            conn.commit()

class GearRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_gear(self, gearbundle_id, gearname, gearquantity, gearimage_path):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO gear (gearbundle_id, gearname, gearquantity, gearimage_path)
                VALUES (?, ?, ?, ?)
            ''', (gearbundle_id, gearname, gearquantity, gearimage_path))
            conn.commit()

    def read_gear(self, gear_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gear WHERE id = ?', (gear_id,))
            return cursor.fetchone()

    def update_gear(self, gear_id, gearbundle_id, gearname, gearquantity, gearimage_path):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE gear
                SET gearbundle_id = ?, gearname = ?, gearquantity = ?, gearimage_path = ?
                WHERE id = ?
            ''', (gearbundle_id, gearname, gearquantity, gearimage_path, gear_id))
            conn.commit()

    def delete_gear(self, gear_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM gear WHERE id = ?', (gear_id,))
            conn.commit()

class GearBundleRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_gearbundle(self, gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO gearbundle (gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide))
            conn.commit()

    def read_gearbundle(self, gearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gearbundle WHERE id = ?', (gearbundle_id,))
            return cursor.fetchone()

    def update_gearbundle(self, gearbundle_id, gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE gearbundle
                SET gearbundleband_id = ?, gearbundleartist_id = ?, gearbundlesound_id = ?, gearbundlename = ?, gearbundleimage_path = ?, gearbundleuserguide = ?
                WHERE id = ?
            ''', (gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide, gearbundle_id))
            conn.commit()

    def delete_gearbundle(self, gearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM gearbundle WHERE id = ?', (gearbundle_id,))
            conn.commit()

class GearBundleSoundRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_gearbundlesound(self, gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO gearbundlesound (gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path)
                VALUES (?, ?, ?, ?)
            ''', (gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path))
            conn.commit()

    def read_gearbundlesound(self, gearbundlesound_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gearbundlesound WHERE id = ?', (gearbundlesound_id,))
            return cursor.fetchone()

    def update_gearbundlesound(self, gearbundlesound_id, gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE gearbundlesound
                SET gearbundle_id = ?, gearbpresetname = ?, gearbpreset_path = ?, gearbpsoundclip_path = ?
                WHERE id = ?
            ''', (gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path, gearbundlesound_id))
            conn.commit()

    def delete_gearbundlesound(self, gearbundlesound_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM gearbundlesound WHERE id = ?', (gearbundlesound_id,))
            conn.commit()

class BandGearBundleRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_bandgearbundle(self, band_id, gearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bandgearbundle (band_id, gearbundle_id)
                VALUES (?, ?)
            ''', (band_id, gearbundle_id))
            conn.commit()

    def read_bandgearbundle(self, bandgearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bandgearbundle WHERE id = ?', (bandgearbundle_id,))
            return cursor.fetchone()

    def update_bandgearbundle(self, bandgearbundle_id, band_id, gearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bandgearbundle
                SET band_id = ?, gearbundle_id = ?
                WHERE id = ?
            ''', (band_id, gearbundle_id, bandgearbundle_id))
            conn.commit()

    def delete_bandgearbundle(self, bandgearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bandgearbundle WHERE id = ?', (bandgearbundle_id,))
            conn.commit()

class ArtistGearBundleRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_artistgearbundle(self, artist_id, gearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO artistgearbundle (artist_id, gearbundle_id)
                VALUES (?, ?)
            ''', (artist_id, gearbundle_id))
            conn.commit()

    def read_artistgearbundle(self, artistgearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM artistgearbundle WHERE id = ?', (artistgearbundle_id,))
            return cursor.fetchone()

    def update_artistgearbundle(self, artistgearbundle_id, artist_id, gearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE artistgearbundle
                SET artist_id = ?, gearbundle_id = ?
                WHERE id = ?
            ''', (artist_id, gearbundle_id, artistgearbundle_id))
            conn.commit()

    def delete_artistgearbundle(self, artistgearbundle_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM artistgearbundle WHERE id = ?', (artistgearbundle_id,))
            conn.commit()
