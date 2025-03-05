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

    picture         creates an "image vs 3 input" from file pathway
    color           creates a "color source" at 100% opacity (put in hex, script will account # in sheets) 
                        Hexes are converted in reverse order for BGRA, and the result is ARGB to send to OBS. 
    browser         creates a "browser source" from the URL
    media           creates a "media source" from file pathway
    text            creates a "text source"

    All other labels will create a text field by default. 

Scenes and inputs:
- All inputs will be created/updated on "Sources" Scene on the first run. 
- After the first run, if inputs are found in other scenes, GUI will update all scenes and create new inputs on "Sources"
- If you delete the "Sources" scene, GUI will only create unused inputs in the new "Sources" scene. All other scenes are still updated.  

How to use: (Gui.py is main file, open in compiler or CMD Prompt/Terminal)
- Browse: locate the CSV file that you want as your source.
- Add new Source: Manually add a new source to OBS quickly. This will not update your CSV file. 
- Configure CSV Mapping: Adjust CSV input naming protocols. Rerun this when adding additional values from CSV
- Reload CSV: Update changes of existing fields of CSV inside of program. Keybind- F5
- Save & Send to OBS: Updates CSV and Creates/updates sources inside of OBS. Keybind - Control/Command + s
- Connect to Websocket: If OBS CSV disconnects from OBS websocket, click connect to OBS to attempt a reconnection. The program will attempt 3 times.
- Double-clicking values will allow you to edit source name and values. Press Enter or Click to Save Changes. Press Escape to cancel changes. Values can be input however you need to, and when you reload/save changes, the GUI will convert the hex properly. This also will updates the CSV automatically.  

Known/untested bugs:
1) What happens to GUI above x number of inputs.  
2) Browser sources default as transparent
3) Keybinds for reload and save only work after clicking within the source/value box. 
4) Add New Source does not save to CSV

Planned implementations:
1) GUI displays short hex and not decimal hex
2) GUI displays short pathways
3) Move "Save Changes" to below "Reload"
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