import os, shutil

os.mkdir("plugins")

for root, dirs, files in os.walk("pluginRepos", followlinks=True):
    for name in files:
        if name.endswith(".dll") or name.endswith(".dylib") or name.endswith(".so"):
            filename = name.split("/")[-1].split("\\")[-1]

            shutil.copy2(os.path.join(root,name), os.path.join("plugins", filename))
