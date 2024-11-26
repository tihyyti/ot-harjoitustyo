# Tässä on Copilot assistoinut listan loppuun saakka
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('soundslite_v1.db')
cursor = conn.cursor()

# Insert data into the gearbundlesound table
gearbundlesound_data = [
    (1, 'Sixties_Rock_Preset', 'presets/rock_preset1.json', 'sound_clips/rock_preset1.mp3'),
    (1, 'Southern_Rock_Preset', 'presets/rock_preset2.json', 'sound_clips/rock_preset2.mp3'),
    (1, 'Surfing_Preset', 'presets/rock_preset3.json', 'sound_clips/rock_preset3.mp3'),
    (1, 'Fifties_Rock_Preset', 'presets/rock_preset4.json', 'sound_clips/rock_preset4.mp3'),
    (1, 'Rickenbacker_Bass_Preset', 'presets/rock_preset5.json', 'sound_clips/rock_preset5.mp3'),
    (1, 'Mixer_Preset_Tascam_1', 'presets/rock_preset6.json', 'sound_clips/rock_preset6.mp3'),
    (1, 'Mixer_Preset_Tascam_2', 'presets/rock_preset7.json', 'sound_clips/rock_preset7.mp3'),
    (1, 'HardRockPreset_1', 'presets/rock_preset8.json', 'sound_clips/rock_preset8.mp3'),
    (1, 'HeavyrockPreset_1', 'presets/rock_preset9.json', 'sound_clips/rock_preset9.mp3')
]

cursor.executemany('''
INSERT INTO gearbundlesound (gearbundle_id, gearbpresetname, gearbpreset_path, gearbpsoundclip_path)
VALUES (?, ?, ?, ?)
''', gearbundlesound_data)

# Insert data into the gearbundle table
gearbundle_data = [
    (1, 1, 1, 'Solo_Guitar_Bundle_1', 'images/solo_guitar_setup.png', 'user_guides/solo_guitar_setup.pdf'),
    (1, 2, 1, 'Rhythm_Guitar_Bundle_1', 'images/Rhythm_guitar_setup.png', 'user_guides/rhythm_guitar_setup.pdf'),
    (1, 3, 1, 'Bass_Guitar_Bundle_1', 'images/Bass_guitar_setup.png', 'user_guides/bass_guitar_setup.pdf'),
    (1, 2, 1, 'Acoustic_Guitar_Bundle_1', 'images/Acoustic_guitar_setup.png', 'user_guides/acoustic_guitar_setup.pdf'),
    (1, 4, 1, 'Cymbalset_Bundle_1_Ziljian', 'images/Cymbalset_Ziljian_setup.png', 'user_guides/Ziljian_setup.pdf'),
    (1, 4, 1, 'Cymbalset_Bundle_2_Sabian', 'images/Cymbalset_Sabian_setup.png', 'user_guides/Sabian_setup.pdf'),
    (1, 4, 1, 'Mics_With_Overhead_Stands_bundle_1', 'images/Overhead_Stands_1_setup.png', 'user_guides/Overhead_Stands_setup.pdf'),
    (1, 4, 1, 'Mics_With_Overhead_Stands_bundle_2', 'images/Overhead_Stands_2_setup.png', 'user_guides/Overhead_Stands_setup.pdf'),
    (1, 1, 1, 'Mic_with_Stand_bundle_1', 'images/Mic_with_Stand_1_setup.png', 'user_guides/Mic_WithStand_1_setup.pdf'),
    (1, 2, 1, 'Mic_with_Stand_bundle_2', 'images/Mic_with_Stand_2_setup.png', 'user_guides/Mic_WithStand_2_setup.pdf'),
    (1, 3, 1, 'Mic_with_Stand_bundle_3', 'images/Mic_with_Stand_3_setup.png', 'user_guides/Mic_WithStand_3_setup.pdf'),
    (1, 1, 1, 'Drumset_mics_Bundle_1', 'images/Drumset_mics_1_setup.png', 'user_guides/Drumset_mics_1_setup.pdf'),
    (1, 1, 1, 'Drumset_mics_Bundle_2', 'images/Drumset_mics_1_setup.png', 'user_guides/Drumset_mics_2_setup.pdf')
]

cursor.executemany('''
INSERT INTO gearbundle (gearbundleband_id, gearbundleartist_id, gearbundlesound_id, gearbundlename, gearbundleimage_path, gearbundleuserguide)
VALUES (?, ?, ?, ?, ?, ?)
''', gearbundle_data)

# Insert data into the band table
cursor.execute('''
INSERT INTO band (bandgearbundle_id, bandname, bandimage_path, bandsocmedgroupname)
VALUES (1, 'Four Camels', 'images/FourCamels.png', 'VintageRockersGroup')
''')

# Insert data into the artist table
cursor.execute('''
INSERT INTO artist (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)
VALUES (1, 1, 'Jouni Porokorpi', 'password123', 1, 2)
''')
cursor.execute('''
INSERT INTO artist (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)
VALUES (1, 2, 'Pave Presonius', 'password123', 2, 2)
''')
cursor.execute('''
INSERT INTO artist (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)
VALUES (1, 2, 'Jari Paltamo', 'password123', 3, 2)
''')
cursor.execute('''
INSERT INTO artist (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)
VALUES (1, 2, 'Elmo Aalto', 'password123', 4, 3)
''')
cursor.execute('''
INSERT INTO artist (artistband_id, artistgearbundle_id, artistname, artistpassw, artistrole_1, artistrole_2)
VALUES (1, 2, 'Kisu Blomqvist', 'password123', 5, 2)
''')


# Insert data into the gear table
gear_data = [
    (1, 'Fender_Stratocaster_USA', 1, 'images/Fender_Stratocaster.png'),
    (2, 'Fender_Jazzmaster', 1, 'images/Fender_Jazzmaster.png'),
    (3, 'Gibson_320', 1, 'images/Gibson_320.png'),
    (4, 'Acoustic_Hummingbird', 1, 'images/Hummingbird_acoustic.png'),
    (5, 'Electro_Acoustic_Silvertone', 1, 'images/Silvertone_guitar.png'),
    (1, 'Pedal_FuzzBox', 2, 'images/Fuzz_pedal.png'),
    (2, 'Pedal_Electroharmonix_BigMuff', 2, 'images/BicMuff_pedal.png'),
    (1, 'Pedal_Octavia', 2, 'images/Octavi_pedal.png'),
    (1, 'Pedal_Crybaby_Wah', 2, 'images/Crybaby_pedal.png'),
    (3, 'Roland_RE201_tape_echo', 2, 'images/RE201_tape_echo.png'),
    (2, 'Roland_Reverb_echo', 2, 'images/Roland_Reverb_pedal.png'),
    (3, 'Roland_Flanger', 2, 'images/Roland_Flanger_pedal.png'),
    (3, 'Pedal_Boss_DM2_Delay', 2, 'images/Boss_DM2_Delay_pedal.png'),
    (1, 'Pedal_Vibe', 2, 'images/Vibe_pedal.png'),
    (1, 'Pedal_Chorus', 2, 'images/Chorus_pedal.png'),
    (6, 'Bass_Rickenbacker', 1, 'images/Rickenbacker_bass_guitar.png'),
    (6, 'Bass_Fender_Bassmaster', 1, 'images/Fender_Bassmaster_guitar.png'),
    (1, 'Bass_Burns', 1, 'images/Burns_bass_guitar.png'),
    (1, 'Gtr_Combo_VOX_C30', 1, 'images/Combo_VOX_C30.png'),
    (1, 'Gtr_Combo_Fender_Twin_blackface', 1, 'images/Fender_Twin_blackface_amp.png'),
    (1, 'Gtr_Combo_Selmer_Thunderbird', 1, 'images/Selmer_Thunderbird_combo_amp.png'),
    (1, 'Gtr_Combo_Ampeg_ReverbeRocket', 1, 'images/Ampeg_ReverbeRocket_combo_amp.png'),
    (1, 'Gtr_Combo_Sovtek_midi_USSR', 1, 'images/Sovtek_midi_USSR_combo_amp.png'),
    (1, 'Keyboard_Korg_stage_piano', 1, 'images/Korg_stage_piano.png'),
    (1, 'Yamaha_CX700', 1, 'images/Yamaha_CX700_keyboard.png'),
    (1, 'Mic_Shure_58', 3, 'images/Shure_58.png'),
    (1, 'Mic_Shure_57', 3, 'images/Shure_57.png'),
    (1, 'Mic_Shure_B52_kickdrum', 3, 'images/Shure_B52_kickdrum_mic.png'),
    (1, 'Mic_Drumset_Overhead', 3, 'images/Drumset_overhead_mic.png'),
    (1, 'Mic_kondensator_smare_mic', 3, 'images/Kondensator_smare_mic.png'),
    (1, 'Kick_Ludvig_1965', 1, 'images/Ludvig_1965_Kick_drum.png'),
    (1, 'Snare_Ludvig_1965', 1, 'images/Ludvig_1965_Snare_drum.png'),
    (1, 'TomTom_Ludvig_1965', 1, 'images/Ludvig_1965_TomTom_drum.png'),
    (1, 'FloorTom_Ludvig_1965', 1, 'images/Ludvig_1965_FloorTom_drum.png'),
    (1, 'HiHat_stand_Ludvig_1965', 1, 'images/Ludvig_1965_HiHat_stand.png'),
    (1, 'Mixing_Board_Tascam_D32', 1, 'images/Tascam_D32_mixing_board.png'),
    (1, 'Drumset_Ludvig_1965', 1, 'images/Ludvig_1965_drum_set.png'),
    (1, 'Drumset_Tama_1966', 1, 'images/Tama_1966_drum_set.png')
]

cursor.executemany('''
INSERT INTO gear (gearbundle_id, gearname, gearquantity, gearimage_path)
VALUES (?, ?, ?, ?)
''', gear_data)

# Insert data into the artistgearbundle table
artistgearbundle_data = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]

cursor.executemany('''
INSERT INTO artistgearbundle (artist_id, gearbundle_id)
VALUES (?, ?)
''', artistgearbundle_data)

# Insert data into the bandgearbundle table
bandgearbundle_data = [
    (1, 7),
    (1, 8),
    (1, 9),
    (1, 10),
    (1, 11),
    (1, 12),

]

cursor.executemany('''
INSERT INTO bandgearbundle (band_id, gearbundle_id)
VALUES (?, ?)
''', bandgearbundle_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
