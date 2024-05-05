import subprocess
import regex

profile_regex = r"[a-zA-ZöÖüÜäÄ\s]+:(.+?)\r\n"
content_regex = r"(?<=(Key Content|Schl\x81sselinhalt)\s*:\s*)(.+?)\r\n"


def get_netsh_output(command: list) -> str:
    """Run a netsh command and return the output as a string"""
    try:
        output = subprocess.check_output(command).decode("iso-8859-1")
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return ""


def extract_profiles(data: str) -> list:
    """Extract profile names from netsh output"""
    return [profile.strip() for profile in regex.findall(profile_regex, data)]


def extract_key_content(data: str) -> str:
    """Extract key content from netsh output"""
    match = regex.search(content_regex, data)
    return match.group(0).strip() if match else "<No key found!>"


def scan_profiles() -> list:
    """Scan for Wi-Fi profiles and extract key contents"""
    data = get_netsh_output(["netsh", "wlan", "show", "profiles"])
    profiles = extract_profiles(data)
    results = []
    for profile in profiles:
        profile_data = get_netsh_output(
            ["netsh", "wlan", "show", "profile", profile, "key=clear"]
        )
        key_content = extract_key_content(profile_data)
        results.append(f"{profile:<30}|  {key_content:<}")
    return results


if __name__ == "__main__":
    for result in scan_profiles():
        print(result)
