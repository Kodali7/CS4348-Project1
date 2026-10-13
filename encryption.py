import sys

def vigenere(text, passkey, decrypt=False):
    if not (text.isascii() and text.isalpha()
            and passkey.isascii() and passkey.isalpha()):
        raise ValueError("Text and passkey must contain only letters A-Z")

    text = text.upper()
    passkey = passkey.upper()
    direction = -1 if decrypt else 1 # subtract vs add
    result = []
    for index, letter in enumerate(text):
        shift = ord(passkey[index % len(passkey)]) - ord("A") # repeat key; map letter to shift 0-25
        position = ord(letter) - ord("A")
        result.append(chr(ord("A") + (position + direction * shift) % 26))
    return "".join(result) # combine encrypted or decrypted letters into one string


def main():
    passkey = None

    for line in sys.stdin:
        parts = line.rstrip("\r\n").lstrip().split(maxsplit=1) # remove line ending; split command from argument
        if not parts:
            print("ERROR Missing command", flush=True)
            continue
        command = parts[0].upper() # first word, normalized to uppercase
        argument = parts[1] if len(parts) == 2 else ""

        if command == "QUIT": # exit here
            if argument:
                print("ERROR QUIT doesn't accept an argument", flush=True)
                continue
            return 0

        if command not in ("PASS", "ENCRYPT", "DECRYPT"): # not a valid command
            print("ERROR Unknown command", flush=True)
            continue

        if command in ("ENCRYPT", "DECRYPT") and passkey is None: # we need a passkey to base it off
            print("ERROR Password hasn't been set", flush=True)
            continue

        if not (argument.isascii() and argument.isalpha()): # validate our args
            print("ERROR Argument must contain only letters A-Z", flush=True)
            continue

        if command == "PASS":
            passkey = argument.upper()
            print("RESULT", flush=True)
        else: # time to decrypt/encrypt
            condition = command == "DECRYPT"
            result = vigenere(argument, passkey, condition)
            print(f"RESULT {result}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
