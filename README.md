# OBS_CSV_Handler
OBS CSV Handler is intended 

    to be used along side Sheet Tools so that information can be updated remotely.
        https://github.com/STS-Projects/Sheets-Tool
        -Sheet Tools will allow you to use up to 5 API keys to pull from a specific worksheet in a Google Sheet. 

    To be used with OBS websocket (enable websocket server in OBS). 
        Do not use a password currently. You may need to adjust your IP, ports, and firewall settings. 


OBS CSV Handler can use any CSV file but requires name markers for generating specific inputs for OBS. 

    picture         creates an image vs 3 input from file pathway
    color           creates a color source at 100% opacity (put in hex)
    browser         creats a browser source from the url
    media           creates a media file from file pathway

    All other labels will create a text field by default. 

How to use: (Gui.py is main file)

    Browse: locate the CSV file that you want as your source.

    Add new Source: Manually add a new source quickly. This will not update your CSV file. 
    Configure CSV Mapping: Adjust CSV input naming protocols, Rerun this when adding additional values from CSV
    Refresh: Update changes of existing fields of CSV inside of OBS CVS Updater (not OBS yet)
    Save Changes: Creates/updates sources inside of OBS
    Connect to OBS: If OBS CSV disconnects from OBS websocket, click connect to OBS to attempt a reconnection. The program will attempt 3 times. 
    

 
