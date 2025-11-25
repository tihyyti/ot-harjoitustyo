
Requirements
------------

- Python 3.10+ (Linux in VMWare Horizon/Cubbli client)
- tkinter (GUI)

Quick setup
-----------

1. Create the database (includes demo user/admin/one food):

   python3 src/create_db.py

2. Optionally import sample foods:

   python3 src/scripts/import_foods.py data/sample_foods.csv

2. Optionally import sample activities:

   python3 src/scripts/import_activities.py data/sample_activities.csv

3. Run the GUI:

   python3 src/laihdutanyt_v1.py

   Use demo credentials: username `demouser`, password `demopass` (or register a new user).

Notes
-----

- The GUI import uses the import modules `scripts.import_foods` and `scripts.import_activities`.
- The Food Logging UI displays logs for the chosen date; you can change the date in the date field.
