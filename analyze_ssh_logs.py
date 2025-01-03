import subprocess
import pandas as pd

def extract_usernames():
    """
    Extracts usernames from SSH failed login attempts.

    Returns:
        pandas DataFrame containing extracted usernames.
    """
    command = "grep 'Failed password for' secure* | grep -v 'invalid user' | awk '{print $9}'"
    output = subprocess.run(command.split(), capture_output=True, text=True).stdout
    return pd.DataFrame({'username': output.splitlines()})

def user_exists(username):
    """
    Checks if a username exists in /etc/passwd.

    Args:
        username: The username to check.

    Returns:
        True if the username exists, False otherwise.
    """
    command = f"grep -q '^{username}:' /etc/passwd"
    result = subprocess.run(command.split(), shell=True, check=True)
    return result.returncode == 0

def analyze_logs():
    """
    Extracts usernames, checks for their existence, and identifies suspicious usernames.

    Returns:
        pandas DataFrame containing suspicious usernames.
    """
    usernames_df = extract_usernames()
    suspicious_usernames = usernames_df[~usernames_df['username'].apply(user_exists)]
    return suspicious_usernames

if __name__ == "__main__":
    suspicious_usernames = analyze_logs()

    if suspicious_usernames.empty:
        print("No suspicious usernames found.")
    else:
        print("Suspicious Usernames:")
        print(suspicious_usernames)