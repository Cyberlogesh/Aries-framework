from modules.network import NetworkModule
from modules.execution import ExecutionModule
from collectors.windows_defender import WindowsCollector
from scoring.dsi import calculate_score


class AriesEngine:

    def __init__(self):
        self.target_ip = None
        self.username = None
        self.password = None

        self.execution_results = None
        self.log_results = None

    # -------------------------
    # Set Target & Credentials
    # -------------------------
    def set_target(self, ip):
        self.target_ip = ip
        print(f"[+] Target set to {ip}")

        self.username = input("Enter username: ")
        self.password = input("Enter password: ")

    # -------------------------
    # Run Execution Test
    # -------------------------
    def run_execution_test(self):
        if not self.target_ip:
            print("[-] Set target first.")
            return

        module = ExecutionModule(
            self.target_ip,
            self.username,
            self.password
        )

        self.execution_results = module.run()

    # -------------------------
    # Collect Logs
    # -------------------------
    def collect_logs(self):
        if not self.target_ip:
            print("[-] Set target first.")
            return

        collector = WindowsCollector(
            self.target_ip,
            self.username,
            self.password
        )

        self.log_results = collector.run()

    # -------------------------
    # Generate Report
    # -------------------------
    def generate_report(self):

        if not self.execution_results:
            print("[-] Run execution test first.")
            return

        if not self.log_results:
            print("[-] Collect logs first.")
            return

        report = calculate_score(
            self.execution_results,
            self.log_results
        )

        print("\n========== ARIES DEFENSIVE REPORT ==========")
        print(f"Network Exposure: {report['network_exposure']}")
        print(f"Execution Control: {report['execution_control']}")
        print(f"Final Defensive Strength Index: {report['final_score']}/100")
        print(f"Security Rating: {report['security_rating']}")
        print("============================================\n")
