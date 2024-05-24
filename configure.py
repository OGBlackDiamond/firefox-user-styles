import argparse, os, pathlib, platform, shutil

# instantiate the argument parser
parser = argparse.ArgumentParser(description="Custom Firefox user styles automatic configuration utility")

# wipe any old configuration files and create new ones in their place
parser.add_argument("--wipe", action="store_true", help="Delete any old configuration files before creating the new ones")

# append new data to existing configuration files
parser.add_argument("--append", action="store_true", help="Append new data to existing configuration files")

# delete any configuration files in case something breaks
parser.add_argument("--delete", action="store_true", help="Delete existing configuration files")

# add support for other versions of firefox
parser.add_argument("-d", "--developer", action="store_true", help="Target a developer edition firefox profile")
parser.add_argument("-c", "--custom", type=str, default=None, help="Target your custom firefox profile")

# parse the arguemnts gotten
args = parser.parse_args()

# gets the home directory of the system
home_dir = pathlib.Path.home()

# gets the kernel type so the correct file system can be parsed
opsys = platform.system()

# create a release string for different firefox versions
release_name = ""

if args.custom != None:
    release_name = f"*{args.custom}*"
elif args.developer:
    release_name = "*dev-edition-default*"
else:
    release_name = "*default-release*"


# gets the default firefox profile based on kernel
if opsys == "Windows":
    profiles = home_dir.glob(f"AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\{release_name}\\")
elif opsys == "Linux":
    profiles = home_dir.glob(f".mozilla/firefox/{release_name}/")
elif opsys == "Darwin":
    profiles = home_dir.glob(f"Library/Application Support/Firefox/Profiles/{release_name}")
else:
    # why aren't you using any of these operating systems???
    print("Unrecognized file system!")
    print("I only support file systems for: Windows, GNU/Linux, and MacOS")
    exit()

firefox_default_profile = next(profiles, None)

if firefox_default_profile == None:
    print("Firefox profile could not be located!")
    print("Quitting...")
    exit()

# reads the directory back to the user for potential debugging
print("\033[1m" + "\nfound firefox user profile @ " + "\033[0m" + "\"", end="")
print(firefox_default_profile, end="")
print("\"\n")

# asks to make sure the directory that the user wants to edit is correct
print("Would you like to continue? (y/n)")
ans = input("--> ")

while ans != "y" and ans != "n":
    print("invalid option! (y/n)?")
    ans = input("--> ")


if ans == "n":
    print("Quitting...")
    exit()


print()
###########################################################################

# the path for the chrome directory
profile_chrome_dir = os.path.join(firefox_default_profile, "chrome/") #type: ignore

# the path for the userChrome file
profile_chrome_file = os.path.join(profile_chrome_dir, "userChrome.css")

# the path for the userContent file
profile_content_file = os.path.join(profile_chrome_dir, "userContent.css")

# the path for the user preferences file
profile_user_prefs = os.path.join(firefox_default_profile, "user.js") #type: ignore

# values of whether certain directories exist
chrome_exists = False;
user_chrome_exists = False;
user_content_exists = False;
user_prefs_exists = False;

# checks the existance of all files and directories
def check_existances():
    global chrome_exists, user_chrome_exists, user_content_exists, user_prefs_exists

    # checks the existance of certain files
    chrome_exists = os.path.exists(profile_chrome_dir)
    if chrome_exists:
        user_chrome_exists = os.path.exists(profile_chrome_file)
        user_content_exists = os.path.exists(profile_content_file)
    user_prefs_exists = os.path.exists(profile_user_prefs)

# replicates userChrome.css
def rep_usr_chrome():
    shutil.copyfile("./styles/userChrome.css", profile_chrome_file)
    print("Replicating userChrome.css\n")

# replicates userContent.css
def rep_usr_content():
    shutil.copyfile("./styles/userContent.css", profile_content_file)
    print("Replicating userContent.css\n")

# replicates user.js
def rep_usr_prefs():
    shutil.copyfile("./user-scripts/user.js", profile_user_prefs)
    print("Enabling legacy toolkit profile customization and cleaning up the toolbar\n")

def mk_chrom_dir():
    os.mkdir(profile_chrome_dir)
    print("Creating chrome directory\n")

# creates the chrome directory
def check_chrom_dir():
    if chrome_exists:
        print("Found chrome directory\n")
    else:
        mk_chrom_dir()

# copys all of the custom files into their respecive directories
def copy_files():

    # ensures the existance of the chrome directory
    check_chrom_dir()

    # checks to make sure that a userChrome file doesn't already exist
    if not user_chrome_exists:
        rep_usr_chrome()
    else:
        print("A userChrome.css file already exists! Please remove it with the \"--delete\" argument or append to it with the \"--append\" argument\n")

    # checks to make sure that a userContent file doesn't already exist
    if not user_content_exists:
        rep_usr_content()
    else:
        print("A userContent.css file already exists! Please remove it with the \"--delete\" argument or append to it with the \"--append\" argument\n")

    # checks to make sure we aren't overwriting the user's pre-existing data
    if not user_prefs_exists:
        rep_usr_prefs()
    else:
        print("It looks like you already have a user.js file!")
        print("All this script is trying to do is enable \"toolkit.legacyUserProfileCustomizations.stylesheets\" and clean up your toolbar\n")
        print("If you already have this enabled, no sweat; if not, append to it with the \"--append\" argument")


# deletes and creates a fresh set of configuration files
def copy_files_wipe():
    delete(True)
    mk_chrom_dir()
    rep_usr_chrome()
    rep_usr_content()
    rep_usr_prefs()


# appends whatever is in the local files, on top of whatever has already exists in the configuration
def copy_files_append():

    # ensures the existance of the chrome directory
    check_chrom_dir()

    # appends the userChrome file
    if user_chrome_exists:
        with open(profile_chrome_file, "a") as user_chrome:
            with open("./styles/userChrome.css", "r") as new_user_chrome:
                user_chrome.write("\n" + new_user_chrome.read())
        print("Appended to userChrome.css\n")
    else:
        print("userChrome.css doesn't exist - creating a fresh one\n")
        rep_usr_chrome()

    # appends the userContent file
    if user_content_exists:
        with open(profile_content_file, "a") as user_content:
            with open("./styles/userContent.css", "r") as new_user_content:
                user_content.write("\n" + new_user_content.read())
        print("Appended to userContent.css\n")
    else:
        print("userContent.css doesnt' exist - creating a fresh one\n")
        rep_usr_content()

    # appends the user preferences file
    if user_prefs_exists:
        with open(profile_user_prefs, "a") as user_prefs:
            with open("./user-scripts/user.js", "r") as new_user_prefs:
                user_prefs.write("\n" + new_user_prefs.read())
        print("Appended to user.js\n")
    else:
        print("user.js doesn't exist - creating a fresh one\n")
        rep_usr_prefs()

# delete any and all configuration files
def delete(is_for_wipe=False):
    print("Nuclear Launch Detected...")
    # checks if the chrome directory exists
    if chrome_exists:
        # checks if userChrome.css exists, and deletes it
        if user_chrome_exists:
            os.remove(profile_chrome_file)
            print("Nuking userChrome.css")

        # checks if userContent.css exists, and deletes it
        if user_content_exists:
            os.remove(profile_content_file)
            print("Nuking userContent.css")

        # deletes the chrome directory
        os.rmdir(profile_chrome_dir)
        print("Nuking chrome directory")

    # checks if user.js exists, and deletes it
    if user_prefs_exists:
        os.remove(profile_user_prefs)
        print("Nuking user.js")

    print("\nNuking complete\n")
    if not is_for_wipe:
        print("Your default Firefox profile should return to default settings upon restartarting the browser")
        quit()

# ensure that every function knows which files exist
check_existances()

# runs the needed command based on the arguemnt parser
if args.wipe:
    copy_files_wipe()
elif args.append:
    copy_files_append()
elif args.delete:
    delete()
else:
    copy_files()


print("\nDone!\nPlease restart Firefox to allow your changes to take effect")
