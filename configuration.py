import pathlib
import os
import shutil

# gets the default firefox profile
profiles = pathlib.Path.home().glob(".mozilla/firefox/*default-release*/")
firefox_default_profile = next(profiles, None)

# reads the directory back to the user for potential debugging
print("found firefox user profile @ \"", end="")
print(firefox_default_profile, end="")
print("\"")

# the path for the chrome directory
profile_chrome_dir = os.path.join(firefox_default_profile, "chrome/")

# the path for the userChrome file
profile_chrome_file = os.path.join(profile_chrome_dir, "userChrome.css")

# the path for the userContent file
profile_content_file = os.path.join(profile_chrome_dir, "userContent.css")

# the path for the user preferences file
profile_user_prefs = os.path.join(firefox_default_profile, "user.js")

was_successful = False;

def copy_files():
    global was_successful
    # checks to make sure that a userChrome file doesn't already exist
    if not os.path.exists(profile_chrome_file):
        shutil.copyfile("./styles/userChrome.css", profile_chrome_file)
        print("Replicating userChrome.css")
        was_successful = True;
    else:
        print("A userChrome.css file already exists! Please remove it or add to the configuration yourself.")

    # checks to make sure that a userContent file doesn't already exist
    if not os.path.exists(profile_content_file):
        shutil.copyfile("./styles/userContent.css", profile_content_file)
        print("Replicating userContent.css")
        was_successful = True;
    else:
        print("A userContent.css file already exists! Please remove it or add to the configuration yourself.")


def create_user_prefs():
    global was_successful
    # checks to make sure we aren't overwriting the user's pre-existing data
    if os.path.exists(profile_user_prefs):
        print("It looks like you already have a \"user.js\" file!")
        print("All this script is trying to do is enable \"toolkit.legacyUserProfileCustomizations.stylesheets\"")
        print("If you already have this enabled, no sweat. If not, please add it manually.")
    else:
        with open(profile_user_prefs, 'w') as file:
            file.write("user_pref(\"toolkit.legacyUserProfileCustomizations.stylesheets\", true);")
        print("Enabling legacy toolkit profile customization")
        was_successful = True;


# checks if a chrome directory already exists, and creates a new one if it doesn't already exist
if os.path.exists(profile_chrome_dir):
    print("Found chrome directory")
    copy_files()
else:
    os.mkdir(profile_chrome_dir)
    print("Creating chrome directory")
    copy_files()

create_user_prefs()
if was_successful:
    print("\nDone!\nPlease restart Firefox to allow your changes to take effect")
else:
    print("\nLooks like nothing happened! Please review the logs and try again.")