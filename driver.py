import subprocess
import sys
from pathlib import Path

def send(process, message):
    if process.poll() is not None: # a return code means the process already stopped
        raise RuntimeError("A child process stopped unexpectedly")
    process.stdin.write(message + "\n") 
    # send messaage to child process and flush so it gets through pipe
    process.stdin.flush()


def show_history(history):
    if not history: # we dont have any strings yet
        print("History is empty")
    for number, value in enumerate(history, 1): # go through strings and label them from 1
        print(f"{number}. {value}")



def choose_string(history, command):
    while True:
        choice = input("Use history or enter new string? (history/new): ").strip().lower()
        if choice in ("history", "h"): # user selected to use history
            while True:
                show_history(history)
                selection = input("Select a number or type new to enter a new string: ").strip()
                if selection.lower() in ("new", "n"):
                    break
                try: # error handle user input for number w value error
                    number = int(selection)
                except ValueError:
                    print("ERROR Enter a history number or new")
                    continue
                if 1 <= number <= len(history):
                    return history[number - 1], False
                print("ERROR History number is out of range") # account for misinput
        elif choice not in ("new", "n"): # user selected something unexpected so error
            print("ERROR Choose history or new")
            continue

        # now let's account for user selecting enter new
        label = "password" if command == "password" else "string"
        value = input(f"Enter {label}: ")
        if not (value.isascii() and value.isalpha()): # similar logic we did in encryption
            raise ValueError("Input must contain only proper letters A-Z")
        return value.upper(), True # new


# Run the menu, keep this run's history, and pass commands and results between programs.
def interact(encryption, logger):
    history = []
    while True:
        print("Commands: password, encrypt, decrypt, history, quit")
        command = input("Command: ").strip().lower()
        #not an input we wanted
        if command not in ("password", "encrypt", "decrypt", "history", "quit"):
            send(logger, "COMMAND Unknown command")
            send(logger, "ERROR Unknown command")
            print("ERROR Unknown command.")
            continue
        send(logger, f"COMMAND {command}") # user picked valid command
        if command == "quit":
            send(logger, "RESULT Quit requested") #log quit input
            return
        if command == "history":
            show_history(history) # call history method and log
            send(logger, f"RESULT History displayed ({len(history)} entries)")
            continue
        try:
            value, is_new = choose_string(history, command) # to account for other commadns
        except ValueError as error:
            print(f"ERROR {error}")
            send(logger, f"ERROR {error}")
            continue
        if command != "password":
            # save input but not adding password or repeating something selected
            if is_new:
                history.append(value)
            send(logger, f"{command.upper()} {value}")
        backend_command = "PASS" if command == "password" else command.upper() # we use PASS so use that
        send(encryption, f"{backend_command} {value}")
        response = encryption.stdout.readline().rstrip("\r\n") # remove the line ending

        #splitting so we get the parts that we need 
        parts = response.split(maxsplit=1)
        response_type = parts[0] if parts else ""
        result = parts[1] if len(parts) > 1 else ""

        if response_type not in ("RESULT", "ERROR"):
            #error handling to deal with process
            raise RuntimeError("Encryption program stopped or returned an invalid response")
        if response_type == "RESULT":
            if command == "password":
                # log more useful information to understand that we set our password rather than only saying like result
                response = "RESULT Password set"
            else:
                #else only proper and correct results will be appended for encrypt/decrypt
                history.append(result)

        print(response)
        send(logger, response)


def stop(process): # to make a child quit and related pipes
    # process is still running below then
    if process.poll() is None:
        try:
            send(process, "QUIT") # quit command takes care
        except (OSError, RuntimeError):
            pass
    if process.stdin:
        try:
            # we should be finished sending messages in this pipe
            process.stdin.close()
        except OSError:
            pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        # forcing in case quit command didn't execute properly
        # shouldn't happen but just in case 
        process.kill()
        process.wait()
    if process.stdout:
        process.stdout.close()
    return process.returncode # check if 0 -> success else failed



def main():
    if len(sys.argv) != 2: # script name and log filename
        print("Usage: python3 driver.py <log_file>", file=sys.stderr)
        return 1

    logger = None
    encryption = None
    status = 0
    # use Path to find other files
    directory = Path(__file__).resolve().parent
    try:
        logger = subprocess.Popen( # now we start connecting with our other files
            [sys.executable, str(directory / "logger.py"), sys.argv[1]],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            start_new_session=True,
        )
        # use the subprocess and make the input and output with the pipes to send between
        encryption = subprocess.Popen(
            [sys.executable, str(directory / "encryption.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
            start_new_session=True,
        )
        send(logger, "START Driver started") # log that we started
        interact(encryption, logger)
    except (EOFError, KeyboardInterrupt): # can manually interrupt to quit
        print("\nExiting.")
    except (OSError, RuntimeError) as error:
        # error handle from driver side
        print(f"Driver error: {error}", file=sys.stderr)
        status = 1
    finally:
        if encryption is not None and stop(encryption) != 0:
            status = 1
        if logger is not None:
            try:
                # we need to log that we are stopping before we actually stop 
                send(logger, "EXIT Driver stopped")
            except (OSError, RuntimeError):
                status = 1
            if stop(logger) != 0:
                status = 1
    return status # 0 is good anything else bad


if __name__ == "__main__":
    sys.exit(main())
