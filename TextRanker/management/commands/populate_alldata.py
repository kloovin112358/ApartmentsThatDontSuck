import os
import subprocess

# List of scripts to execute
scripts = [
    "populate_neighborhoods",
    "populate_eventtypes",
    "populate_eventtypedetails",
    "populate_venuetypes",
    "populate_venues",
    "populate_ticketlistings",
]

# Function to handle database setup
def setup_database():
    db_file = os.path.join(os.getcwd(), 'db.sqlite3')
    if os.path.exists(db_file):
        print(f'Deleting existing db.sqlite3...')
        os.remove(db_file)

    # Run migrations
    print('Running migrations...')
    try:
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
    except subprocess.CalledProcessError:
        print('Failed to run migrations. Exiting.')
        return False
    
    return True

# Get the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Setup database and run scripts
if setup_database():
    for script in scripts:
        cmd = f"python manage.py {script}" 
        try:
            print(f"Running script: {script}")
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Error {script} failed.")
else:
    print('Database setup failed. Aborting script execution.')
