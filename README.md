# firefox-user-styles
Custom Firefox user styles automatic configuration utility<br>
#### Note:
The default style configuration is my custom stylesheet built for the vertical tabs extension which will remove the horizontal tabs on top, as well as the window control buttons, bookmark star, save-to-pocket button, and unpin extensions automatically. It also includes a centering fix for the search bar when the favorites are disabled on the start page. If you do not wish this, please edit the styles files to meet your needs by forking this repository.

### How to use
* fork and clone this repository on your local machine
* edit the `userChrome.css`, `userContent.css` and `user.js` files to fit your custom configuration
* push these changes to your fork
* run the `configure.py` script:
    * Argument options:
    1. **No argument** - will add configuration files like normal and won't touch anything that already exists
    2. `--wipe` - will remove any pre-existing configuration files before putting new ones in their place
    3. `--append` - will append the new data on top of existing configuration files
    4. `--delete` - deletes any existing configuration files and does not proceed with adding new files; this should be used if something breaks
* restart Firefox

Now, you can automatically set up this configuration on any machine by cloning your fork on said machine and running the configuration script.
