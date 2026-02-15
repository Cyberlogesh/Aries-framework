import winrm
import base64
import time
import socket

class ExecutionModule:

    def __init__(self, target_ip, username, password):
        self.target_ip = target_ip
        self.username = username
        self.password = password
        self.port = 5985  # Default WinRM HTTP
        self.timeout = 10

        self.results = {
            "test_type": "Execution Simulation",
            "execution_attempted": False,
            "execution_success": False,
            "authentication_success": False,
            "network_reachable": False,
            "response": None,
            "error": None,
            "timestamp": None
        }

    # -------------------------
    # Connectivity Check
    # -------------------------
    def check_port(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.target_ip, self.port))
            sock.close()
            self.results["network_reachable"] = True
            return True
        except:
            return False

    # -------------------------
    # Encode PowerShell Payload
    # -------------------------
    def encode_command(self, command):
        command_bytes = command.encode("utf-16le")
        encoded = base64.b64encode(command_bytes).decode()
        return encoded

    # -------------------------
    # Run Remote Execution
    # -------------------------
    def run(self):
        print("[*] Initiating Hardened Remote Execution Module...")
        self.results["execution_attempted"] = True
        self.results["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Step 1: Validate Network Reachability
        print("[*] Checking WinRM service availability...")
        if not self.check_port():
            self.results["error"] = "WinRM port unreachable."
            print("[-] WinRM port not reachable.")
            return self.results

        print("[+] WinRM service reachable.")

        try:
            # Step 2: Establish Secure Session
            session = winrm.Session(
                f"http://{self.target_ip}:{self.port}/wsman",
                auth=(self.username, self.password),
                transport="ntlm"  # Stronger than basic
            )

            self.results["authentication_success"] = True

            # Step 3: Encoded Execution
            payload = "whoami"
            encoded_payload = self.encode_command(payload)
            ps_command = f"powershell -EncodedCommand {encoded_payload}"

            print("[*] Executing encoded PowerShell remotely...")

            response = session.run_cmd(ps_command)

            if response.status_code == 0:
                self.results["execution_success"] = True
                self.results["response"] = response.std_out.decode().strip()
                print(f"[+] Execution successful: {self.results['response']}")
            else:
                self.results["error"] = response.std_err.decode()
                print("[-] Execution returned error.")

        except winrm.exceptions.InvalidCredentialsError:
            self.results["error"] = "Authentication failed."
            print("[-] Authentication failed.")

        except Exception as e:
            self.results["error"] = str(e)
            print(f"[-] Execution error: {e}")

        print("[*] Execution Module Completed.\n")
        return self.results
