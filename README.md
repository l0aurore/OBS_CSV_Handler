# OBS_CSV_Handler

Works on Windows and Mac OS. 

OBS CSV Handler is intended 

- To be used alongside Sheet Tools (Google Sheets API) to update remotely
        https://github.com/STS-Projects/Sheets-Tool
        -Sheet Tools will allow you to use up to 5 API keys to pull from a specific worksheet in a Google Sheet. 

- To be used with OBS websocket (enable websocket server in OBS. Have Websocket plugin or OBS ver 28+)
        You may need to adjust your IP, ports, and password settings in config.py
          If you are having trouble connecting to the OBS ws, adjust your firewall or remove the password requirements.    

OBS CSV Handler can use any CSV file to create inputs but requires name markers to generate specific inputs for OBS. 

    picture         creates an image vs 3 input from file pathway
    color           creates a color source at 100% opacity (put in hex, script will account # in sheets) 
                        Hexes are converted in reverse order for BGRA, and the result is ARGB to send to OBS. 
    browser         creates a browser source from the URL
    media           creates a media file from file pathway

    All other labels will create a text field by default. 

Scenes and inputs:
- All inputs will be created/updated on "Sources" Scene on the first run. 
- After the first run, if inputs are found in other scenes, GUI will update all scenes and create new inputs on "Sources"
- If you delete the "Sources" scene, GUI will only create unused inputs in the new "Sources" scene. All other scenes are still updated.  

How to use: (Gui.py is main file, open in compiler or CMD Prompt/Terminal)
- Browse: locate the CSV file that you want as your source.
- Add new Source: Manually add a new source quickly. This will not update your CSV file. 
- Configure CSV Mapping: Adjust CSV input naming protocols. Rerun this when adding additional values from CSV
- Refresh: Update changes of existing fields of CSV inside of OBS CVS Updater (not OBS yet)
- Save Changes: Creates/updates sources inside of OBS
- Connect to OBS: If OBS CSV disconnects from OBS websocket, click connect to OBS to attempt a reconnection. The program will attempt 3 times.
- Double-clicking values will allow you to edit source name and values. Hexes can be input however you need to, and when you refresh/save changes, the GUI will convert the hex. This updates the CSV.  

Known/untested bugs:
1) What happens to GUI above x number of inputs.  
2) Browser sources default as transparent

Planned implementations:
1) GUI displays short hex and not decimal hex
2) GUI displays short pathways
3) Move "Save Changes" to below "Refresh" and add shortcuts for refresh and save. 
4) Add Scene and Keybind creation
5) Implement embedded API collection
6) Global modifiers (transparency, rotation, etc) to source to affect across all scenes
    
Dependencies you may need to install (Win and OS) (beginner-friendly):

Python
    Install Python -> https://www.python.org/downloads/ 
    For Windows: CMD Prompt
        You can use the CMD (command) Prompt to run scripts or you can install another compiler. 
        https://code.visualstudio.com/
    For Mac, Python App will install IDLE(compiler) and Launcher. You can use Idle to edit and run scripts,  or the 'terminal' app. You may need to add terimal to your 'Finder'

pip command 
    Install Pip
    Win: using CMD prompt, 
        python -m ensurepip --upgrade
        pip --version
            Ensures which version is installed
    Mac: Using Terminal,
    'curl https://bootstrap.pypa.io/get-pip.py'  (python) OR 'curl https://bootstrap.pypa.io/get-pip.py' (python 3) 

Homebrew
    Homebrew (MAC only)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Now you have the fundation to install all of the modules, you need to run the specific prompts:

    Windows
    - pip install pandas
    - pip install requests
    - pip install TK
    - pip install obsws_python

    Mac
    - Sometimes pip does not work for specific modules, that's where you will need to use homebrew to install them.
    - Example: 
        $ brew install python-tk Or pip install tk

App still throwing errors? Please reach out and I'll trouble shoot with you. 

Even if you do not intend to edit the scripts very much, I find running them within compilers to have unique terminals is much easier for logging purposes. 