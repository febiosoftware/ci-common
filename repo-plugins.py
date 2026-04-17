import os, json

try:
    devRelease = int(os.getenv("DEV_RELEASE"))
except:
    devRelease = 0

if devRelease == 0:
    STAGE_PATH = "stage/"
    DEV_FLAG = ""
else:
    STAGE_PATH = "develop/stage/"
    DEV_FLAG = "-d"

try:
    with open("plugins/versions.json", "r") as file:
        versionInfo = json.load(file)

    febioVersion = versionInfo["febio"]
    del versionInfo["febio"]

    platform = os.environ["OS"]
    if platform == "Windows":
        osFlag = "-w"
    elif platform == "macOS":
        osFlag = "-m"
    else:
        osFlag = "-l"

    for name in versionInfo:
        os.system(f"scp plugins/{name}/* repo:/serverRoot/pluginRepo/files/{name}/{STAGE_PATH}")
        os.system(f'ssh repo "python3 /serverCode/serverTools/pluginTools.py {DEV_FLAG} {name} {versionInfo[name]} {febioVersion} {osFlag}"')

except FileNotFoundError:
    print("Error: 'plugins/versions.json' not found.")
except json.JSONDecodeError:
    print("Error: Invalid JSON format in 'plugins/versions.json'.")