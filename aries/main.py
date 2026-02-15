import sys
import os

# Import your engine class
from core.aries_engine import AriesEngine

# Purple Team Color Scheme
PURPLE = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

VERSION = "0.5 Prototype"

def clear():
    os.system("clear")

def banner():
    print(f"""{PURPLE}
      █████╗ ██████╗ ██╗███████╗███████╗
     ██╔══██╗██╔══██╗██║██╔════╝██╔════╝
     ███████║██████╔╝██║█████╗  ███████╗
     ██╔══██║██╔══██╗██║██╔══╝  ╚════██║
     ██║  ██║██║  ██║██║███████╗███████║
     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝

   Adversarial Response & Integrity Evaluation System
   Purple Team Defensive Validation Framework
   Version: {VERSION}
{RESET}
    """)

def help_menu():
    print(f"""{CYAN}
──────────────────────────────────────────────
 Available Commands
──────────────────────────────────────────────
 set <IP>        → Define target system
 network         → Execute network simulation
 execution       → Execute execution simulation
 collect         → Collect defensive logs
 report          → Generate defensive report
 status          → Show current target
 help            → Show command list
 clear           → Clear screen
 exit            → Exit ARIES
──────────────────────────────────────────────
{RESET}
    """)

def main():
    # 🔥 FIXED: Create real engine object
    engine = AriesEngine()

    clear()
    banner()
    help_menu()

    while True:
        try:
            command = input(f"{PURPLE}aries > {RESET}").strip().lower()

            if command.startswith("set"):
                parts = command.split()
                if len(parts) == 2:
                    engine.set_target(parts[1])
                    print(f"{GREEN}[+] Target set to {parts[1]}{RESET}")
                else:
                    print(f"{RED}[-] Usage: set <IP>{RESET}")

            elif command == "network":
                engine.run_network_test()

            elif command == "execution":
                engine.run_execution_test()

            elif command == "collect":
                engine.collect_logs()

            elif command == "report":
                engine.generate_report()

            elif command == "status":
                if engine.target_ip:
                    print(f"{GREEN}[+] Target: {engine.target_ip}{RESET}")
                else:
                    print(f"{YELLOW}[!] No target configured.{RESET}")

            elif command == "help":
                help_menu()

            elif command == "clear":
                clear()
                banner()

            elif command == "exit":
                print(f"{PURPLE}Shutting down ARIES...{RESET}")
                sys.exit()

            else:
                print(f"{RED}[-] Unknown command. Type 'help'.{RESET}")

        except KeyboardInterrupt:
            print(f"\n{PURPLE}Session terminated.{RESET}")
            sys.exit()

if __name__ == "__main__":
    main()
