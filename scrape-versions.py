import os

ghOutput = os.environ["GITHUB_OUTPUT"]

def getVersion(path, verDef, subverDef, subsubverDef):
    if not path:
        return None

    major = minor = patch = None
    with open(path, "r") as f:
        for line in f:
            if f"#define {verDef}" in line:
                major = line.split()[-1].strip()
            elif f"#define {subverDef}" in line:
                minor = line.split()[-1].strip()
            elif f"#define {subsubverDef}" in line:
                patch = line.split()[-1].strip()

    if major and minor and patch:
        return f"{major}.{minor}.{patch}"
    
    return None

# FEBio version
febioVersion = getVersion("febio4-sdk/include/FEBioLib/version.h", "VERSION", "SUBVERSION", "SUBSUBVERSION")

# SDK version
sdkVersion = getVersion("febio4-sdk/include/FECore/version.h", "FE_SDK_MAJOR_VERSION", "FE_SDK_SUB_VERSION", "FE_SDK_SUBSUB_VERSION")

# Find version.h in current package
versionHeader = None
for root, dirs, files in os.walk(".", followlinks=True):
    for name in files:
        if "febio4-sdk" in name:
            continue
        
        if name.endswith("version.h"):
            versionHeader = os.path.join(root, name)
            break
    
    if versionHeader:
        break

# Get current package version
packageVersion = getVersion(versionHeader, "VERSION", "SUBVERSION", "SUBSUBVERSION")

with open(ghOutput, "a") as f:
    if febioVersion:
        print(f"febio_version={febioVersion}", file=f)
    
    if sdkVersion:
        print(f"sdk_version={sdkVersion}", file=f)

    if packageVersion:
        print(f"package_version={packageVersion}", file=f)