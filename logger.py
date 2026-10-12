import sys
from datetime import datetime

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 logger.py <log_file>", file=sys.stderr)
        return 1

    try:
        # we create file if not there and append if there
        with open(sys.argv[1], "a", encoding="utf-8") as log_file:
            for line in sys.stdin: # check lines input
                line = line.strip()
                if line == "QUIT": # we automatically quit
                    break
                if not line:
                    continue

                parts = line.split(maxsplit=1) # split for before and after first space
                action = parts[0] # the command like start
                message = parts[1] if len(parts) == 2 else "" # message
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M") # format in project instrucitons
                log_file.write(f"{timestamp} [{action}] {message}\n")
                log_file.flush() # deal w buffered text if there
    except OSError as error:
        print(f"Logger error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
