from repositories import BandRepository, ArtistRepository, GearRepository, GearBundleRepository, GearBundleSoundRepository, BandGearBundleRepository, ArtistGearBundleRepository

# A service layer that uses the repository classes to perform CRUD operations. 
# This layer is be independent of the UI framework used.
# Planned UI's are either PyGame or Tkinter, the choose is based on user experience testing
# This prototyping code is assisted by MS Copilot

class BandService:
    def __init__(self, db_path):
        self.repository = BandRepository(db_path)

    def create_band(self, bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname):
        self.repository.create_band(bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname)

    def read_band(self, band_id):
        return self.repository.read_band(band_id)

    def update_band(self, band_id, bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname):
        self.repository.update_band(band_id, bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname)

    def delete_band(self, band_id):
        self.repository.delete_band(band_id)

class ArtistService:
    def __init__(self, db_path):
        self.repository = ArtistRepository(db_path)

    def create_artist(self, artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2):
        self.repository.create_artist(artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)

    def read_artist(self, artist_id):
        return self.repository.read_artist(artist_id)

    def update_artist(self, artist_id, artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2):
        self.repository.update_artist(artist_id, artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)

    def delete_artist(self, artist_id):
        self.repository.delete_artist(artist_id)

class GearService:
    def __init__(self, db_path):
        self.repository = GearRepository(db_path)

    def create_gear(self, gearbundle_id, gearname, gearquantity, gearimage_path):
        self.repository.create_gear(gearbundle_id, gearname, gearquantity, gearimage_path)

    def read_gear(self, gear_id):
        return self.repository.read_gear(gear_id)

    def update_gear(self, gear_id, gearbundle_id, gearname, gearquantity, gearimage_path):
        self.repository.update_gear(gear_id, gearbundle_id, gearname, gearquantity, gearimage_path)

    def delete_gear(self, gear_id):
        self.repository.delete_gear(gear_id)

class GearBundleService:
    def __init__(self, db_path):
        self.repository = GearBundleRepository(db_path)

    def create_gearbundle(self, gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide):
        self.repository.create_gearbundle(gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide)

    def read_gearbundle(self, gearbundle_id):
        return self.repository.read_gearbundle(gearbundle_id)

    def update_gearbundle(self, gearbundle_id, gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide):
        self.repository.update_gearbundle(gearbundle_id, gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide)

    def delete_gearbundle(self, gearbundle_id):
        self.repository.delete_gearbundle(gearbundle_id)

class GearBundleSoundService:
    def __init__(self, db_path):
        self.repository = GearBundleSoundRepository(db_path)

    def create_gearbundlesound(self, gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path):
        self.repository.create_gearbundlesound(gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path)

    def read_gearbundlesound(self, gearbundlesound_id):
        return self.repository.read_gearbundlesound(gearbundlesound_id)

    def update_gearbundlesound(self, gearbundlesound_id, gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path):
        self.repository.update_gearbundlesound(gearbundlesound_id, gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path)

    def delete_gearbundlesound(self, gearbundlesound_id):
        self.repository.delete_gearbundlesound(gearbundlesound_id)

class BandGearBundleService:
    def __init__(self, db_path):
        self.repository = BandGearBundleRepository(db_path)

    def create_bandgearbundle(self, band_id, gearbundle_id):
        self.repository.create_bandgearbundle(band_id, gearbundle_id)

    def read_bandgearbundle(self, bandgearbundle_id):
        return self.repository.read_bandgearbundle(bandgearbundle_id)

    def update_bandgearbundle(self, bandgearbundle_id, band_id, gearbundle_id):
        self.repository.update_bandgearbundle(bandgearbundle_id, band_id, gearbundle_id)

    def delete_bandgearbundle(self, bandgearbundle_id):
        self.repository.delete_bandgearbundle(bandgearbundle_id)

class ArtistGearBundleService:
    def __init__(self, db_path):
        self.repository = ArtistGearBundleRepository(db_path)

    def create_artistgearbundle(self, artist_id, gearbundle_id):
        self.repository.create_artistgearbundle(artist_id, gearbundle_id)

    def read_artistgearbundle(self, artistgearbundle_id):
        return self.repository.read_artistgearbundle(artistgearbundle_id)

    def update_artistgearbundle(self, artistgearbundle_id, artist_id, gearbundle_id):
        self.repository.update_artistgearbundle(artistgearbundle_id, artist_id, gearbundle_id)

    def delete_artistgearbundle(self, artistgearbundle_id):
        self.repository.delete_artistgearbundle(artistgearbundle_id)
