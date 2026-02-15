import winrm
import time

class WindowsCollector:

    def __init__(self, target_ip, username, password):
        self.target_ip = target_ip
        self.username = username
        self.password = password
        self.port = 5985

        self.results = {
            "log_collection_attempted": False,
            "defender_events_found": False,
            "powershell_events_found": False,
            "events": [],
            "error": None,
            "timestamp": None
        }

    def run(self):
        print("[*] Starting Windows Defender Log Collection...")
        self.results["log_collection_attempted"] = True
        self.results["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            session = winrm.Session(
                f"http://{self.target_ip}:{self.port}/wsman",
                auth=(self.username, self.password),
                transport="ntlm"
            )

            # Query last 10 Defender events
            defender_query = """
            Get-WinEvent -LogName "Microsoft-Windows-Windows Defender/Operational" -MaxEvents 10 |
            Select-Object TimeCreated, Id, Message
            """

            response = session.run_ps(defender_query)

            output = response.std_out.decode()

            if output.strip():
                self.results["defender_events_found"] = True
                self.results["events"].append(output)
                print("[+] Defender events collected.")
            else:
                print("[!] No Defender events found.")

            # Query last 10 PowerShell logs
            ps_query = """
            Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" -MaxEvents 10 |
            Select-Object TimeCreated, Id, Message
            """

            ps_response = session.run_ps(ps_query)
            ps_output = ps_response.std_out.decode()

            if ps_output.strip():
                self.results["powershell_events_found"] = True
                self.results["events"].append(ps_output)
                print("[+] PowerShell logs collected.")

        except Exception as e:
            self.results["error"] = str(e)
            print(f"[-] Log collection failed: {e}")

        print("[*] Log Collection Completed.\n")
        return self.results
