import os

def versionTracker():
    version_file = "version_tracker.txt"
    
    default_version = "A"
    
    # Define the sequence of versions
    versions = ["A", "B", "C"]

    # Check if the file exists; if not, create it with the default version
    if not os.path.exists(version_file):
        with open(version_file, "w") as f:
            f.write(default_version)

    # Read the current version
    with open(version_file, "r") as f:
        current_version = f.read().strip()

    #Getting current version and next version
    current_index = versions.index(current_version)
    next_version = versions[(current_index + 1) % len(versions)]

    # Save the next version back to the file (this will be the current version for next time)
    with open(version_file, "w") as f:
        f.write(next_version)

    # Use `current_version` in your experiment
    print(f"Participant assigned to version: {current_version}")
    return current_version
