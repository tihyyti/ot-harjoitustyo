
Requirements
------------

- Python 3.10+ (Linux in VMWare Horizon/Cubbli client)
- tkinter (GUI)

Quick setup
-----------

1. Create the database (includes demo user/admin/one food):

   python3 src/repositories create_db.py

2. Optionally import sample foods:

   python3 scripts/import_foods.py data/sample_foods.csv

3. Populate demo logs (creates food logs for demo user for last 3 days):

   python3 scripts/populate_demo_logs.py

4. Run the GUI:

   python3 laihdutanyt_v1.py

   Use demo credentials: username `demo`, password `demopass` (or register a new user).

Notes
-----

- The GUI import uses the import module `scripts.import_foods`.
- The Food Logging UI displays logs for the chosen date; you can change the date in the date field.
