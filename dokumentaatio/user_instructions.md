
Requirements
------------

- Python 3.10+ (Linux or Linux in VMWare Horizon/Cubbli client)
- Tkinter (GUI)

Quick setup
-----------

1. Create the test database (includes demo user/admin and one food and one activity):

   RUN: python3 src/create_db.py

2. Optionally import more sample foods and activities:

   RUN: python3 ot-harjoitustyo/laihdutanyt_v1

3. Register and login (there are stored credentials for demo: user, pass)

   After Login: From Main button-menu page left upper corner find File-menu, with pull-down menu import options : 
      sample_foods.csv, browse to -> ot-harjoitustyo/src/data/sample_foods.csv
      sample_activities.csv -> ot-harjoitustyo/src/data/sample_activities.csv

4. After successful Login you land to Welcome-page with Main-menu buttons:
   - press View Food Logs or View Activity Logs

5. Those buttons each displays you the Food or Activity Dashboards respectively.
   Via them you can enter your daily food portions and activities you have done.
   Also you can enter a date YYYY-MM-DD-format to get all the logged food portions 
   you have eaten or activities done during that selected day as a list.

   Note 1:The Food Dashboard displays logs for the chosen date; 
   you can change the date in the date field.
   Note 2: The demo Food is "Apple" and Demo activity is "Walking". 
   You can enter or use pull-down menu of the related input-fields to select the items.

6. On the right side of the top row of either the Food Dashboard or Activity Dashboard there is a button with a label "View All Food Logs" or "View All Activity Logs".
By clicking those buttons you can open a window listing all the logged food or activity entries respectively, logged with the date-, item-name, portion or count and related Kcal-info.

7. On the bottom-row of "All Food or Activity Logs" you can find editing buttons. Just select a row from the log for editing and you can edit and save new count and date info of selected log-row. There is also a "Close" button for closing the "All Foods or Activity Logs"-window.

8. laihdutanyt_v1.py can be stopped by clicking "Exit" from the File-menu, located on the left upper corner of the Wellcome button-menu window or by typing ctrl-c via a Terminal.


Notes
-----

- The GUI import uses the import modules `scripts.import_foods` and `scripts.import_activities`.
- The Food Logging UI displays logs for the chosen date; you can change the date in the date field.
