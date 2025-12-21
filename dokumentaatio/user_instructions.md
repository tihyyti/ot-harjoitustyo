
Requirements of Release laihdutanyt_v2
---------------------------------------

- Python 3.10+ (Linux or Linux in VMWare Horizon/Cubbli client)
- Tkinter (GUI)

Quick setup
-----------

1. Create the test database (includes demo user/admin and one food and one activity):

   RUN: python3 src/create_db.py

2. Optionally import more sample foods and activities:

   RUN: python ot-harjoitustyo/src/laihdutanyt_v2.py

3. Register and login 
   (there are stored credentials for a demo: user/pass and admin/apass)

   After Login: From Main button-menu page, left upper corner find File-menu, with a pull-down menu containing import-options : 
      sample_foods.csv, browse to -> ot-harjoitustyo/src/data/sample_foods.csv
      sample_activities.csv -> ot-harjoitustyo/src/data/sample_activities.csv

4. After successful Login you land to the Welcome-page with the Main-menu- 
   buttons and coloured "Card-UI"-management buttons: "Grid Layout", "Cascade" and "Hide/Show". In case you use a laptop with 2nd extension display, read the following guidance and make a ride with the "Card-UI": 
   - press first the coloured Card-UI-buttons (e.g. from left to right) to find out how the Card-UI-works:
   - the default screen size is 27 inch in diameter, also 32 inch and e.g. laptop screen (preferably in a cascaded-mode) can be used. if you have 2 screens (e.g. Laptop screen and 27 or 32 inch secondary expansion display ) drag the floating Main-menu-button-panel first e.g. to the upper left corner of the extension-display (2nd screen), after that you can press "Grid Layout" or "Cascade"-buttons and the other panels follow then the Main-menu panel like "a sheep herd following their leader". You can now practice a little by dragging around the Main-menu on both displays and pressing the management buttons. You can use both displays (for a small display Cascade-mode is better if all panels need to be open and active). The panels also behave like a normal TKinter panels with their traditional functions on the upper right  corner of each window.
   5. After practicing:
   - press then the other non-coloured menu-keys like e.g. View Food Logs and/or View Activity Logs.
   Those buttons each displays you the Food or Activity Dashboards respectively.
   Via them you can enter your daily food portions and activities you have done.
   After that you can push the Daily Foods/Activities Totals buttons (located in Main-menu) to get the lists of total calories eaten and burned on daily bases.

   Note 1:The Food Dashboard displays logs for the chosen date; 
   you can change the date in the date-field.
   Note 2: The demo Food is "apple" and Demo activity is "walking". 
   You can enter or use pull-down menu of the related input-fields to select the items.

6. On the right side, under the header of either the Food Dashboard or Activity Dashboard there is a button with a label "View All Food Logs" or "View All Activity Logs".
By clicking those buttons you can open a window listing all the logged food or activity entries respectively, logged with the date-, item-name, portion or count and related Kcal-info.

7. On the bottom-row of "All Food or Activity Logs" you can find editing buttons. Just select a row from the log for editing and you can edit and save new count and date info of selected log-row. There is also a "Close" button for closing the "All Foods or Activity Logs"-window.

8. laihdutanyt_v2.py can be quitted by just closing the Main Button-menu by clicking it on the right uppermost corner or by clicking "Exit" from the File-menu, located on the left upper corner of the Main button-menu window or by typing ctrl-c via a Terminal.


## How to Use the New Features of Release Laihdutanyt_v2.py

### As a User

1. Click "User Login" button
2. Login with your credentials (for regular user test use: user/pass)
3. Use dashboards as before but now with "Card-UI" management.
4. Notice that today's date is highlighted in yellow in totals view.
5. Add future dates for meal planning. They appear in green.

### As an Admin

1. Click "Admin Login" button
2. Login with admin credentials (for admin/coach test use: admin/apass)
3. Explore the 4 admin/coach-tabs:
   - Manage users
   - Create recommendations
   - Track health constraints
   - Preview of future AI features
4. Click "Logout" to return to login screen

-----
Notes for Release Laihdutanyt_v2:
- The Main button window File-menu imports use the import modules `scripts.import_foods` and `scripts.import_activities`for DB initialization.
