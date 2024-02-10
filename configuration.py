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


def copy_files():
    # checks to make sure that a userChrome file doesn't already exist
    if not os.path.exists(profile_chrome_file):
        shutil.copyfile("./styles/userChrome.css", profile_chrome_file)
        print("Replicating userChrome.css")
    else:
        print("A userChrome.css file already exists! Please remove it or add to the configuration yourself.")

    # checks to make sure that a userContent file doesn't already exist
    if not os.path.exists(profile_content_file):
        shutil.copyfile("./styles/userContent.css", profile_content_file)
        print("Replicating userContent.css")
    else:
        print("A userContent.css file already exists! Please remove it or add to the configuration yourself.")

# checks if a chrome directory already exists, and creates a new one if it doesn't already exist
if os.path.exists(profile_chrome_dir):
    print("Found chrome directory")
    copy_files()
else:
    os.mkdir(profile_chrome_dir)
    print("Creating chrome directory")
    copy_files()