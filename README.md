# OBS_CSV_Handler

Works on Windows and Mac OS. 

OBS CSV Handler is intended 

- To be used along side Sheet Tools so that information can be updated remotely.
        https://github.com/STS-Projects/Sheets-Tool
        -Sheet Tools will allow you to use up to 5 API keys to pull from a specific worksheet in a Google Sheet. 

- To be used with OBS websocket (enable websocket server in OBS. Have Websocket plugin or OBS ver 28+)
        Do not use a password currently. You may need to adjust your IP, ports, and firewall settings in config.py 

OBS CSV Handler can use any CSV file but requires name markers for generating specific inputs for OBS. 

    picture         creates an image vs 3 input from file pathway
    color           creates a color source at 100% opacity (put in hex, script will account # in sheets) 
                        Hexes are converted to in reverse order for BGRA, and compiles the result as ARGB to send to OBS. 
    browser         creats a browser source from the url
    media           creates a media file from file pathway

    All other labels will create a text field by default. 

How to use: (Gui.py is main file, open in compiler or CMD Prompt/Terminal)
- Browse: locate the CSV file that you want as your source.
- Add new Source: Manually add a new source quickly. This will not update your CSV file. 
- Configure CSV Mapping: Adjust CSV input naming protocols, Rerun this when adding additional values from CSV
- Refresh: Update changes of existing fields of CSV inside of OBS CVS Updater (not OBS yet)
- Save Changes: Creates/updates sources inside of OBS
- Connect to OBS: If OBS CSV disconnects from OBS websocket, click connect to OBS to attempt a reconnection. The program will attempt 3 times.
- Double clicking values will allow you to edit. 

Known/untested bugs:
1) ~~ Script overwrites CSV. Not an issue when used with sheets_program_5 but if you are using excel to locally update a CSV, be aware. ~~
2) What happens to GUI above x number of inputs. 
3) Sometimes the program will not update sources in OBS and it requires all sources to be deleted to be updated. I cannot replicate, and websocket connection is confirmed. 
4) Browser sources default as transparent
5) ~~ Program starts with error messaging saying it cannot read the CSV. Once user browses to CSV file, it is read correctly. ~~
    
Planned implentations:
1) GUI displays short hex and not decimal hex
2) GUI displays short pathways
3) Move "Save Changes" to below "Refresh" and add short cuts for refresh and save. 
4) Add Scene and Keybind creation
5) Implement embedded API collection
6) Global modifiers (transparency, rotation, etc) to source to affect across all scenes
    
Dependencies you may need to install (Win and OS) (beginner friendly):

- Install Python -> https://www.python.org/downloads/ 
    For Windows: CMD Prompt
        You can use the CMD (command) Prompt to run scripts or you can install another compiler. 
        https://code.visualstudio.com/
    For Mac, Python App will install IDLE(compiler) and Launcher. You can use Idle to edit and run scripts,  or the 'terminal' app. You may need to add terimal to your 'Finder'

- pip command 
    Win: using CMD prompt, 
        python -m ensurepip --upgrade
        pip --version
            Ensures which version is installed
    Mac: Using Terminal,
    'curl https://bootstrap.pypa.io/get-pip.py'  (python) OR 'curl https://bootstrap.pypa.io/get-pip.py' (python 3) 

- Homebrew (MAC only)
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