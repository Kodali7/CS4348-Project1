# CS4348 Project 1

In the project, I had to show how processes communicate based on the project's task using processes. A driver will start an encryption process and a logger process, then passes commands and results between them where one an output of one becomes the input of another (pass through). Users can also encrypt and decrypt strings with a Vigenere cipher, reuse strings from the current session's history, and record activity through a log file.

## Files

- `driver.py`: Handles user commands, session history, and communication with the child processes.
- `encryption.py`: Sets the password and encrypts or decrypts strings using the Vigenère cipher.
- `logger.py`: Writes timestamped activity messages to the specified log file.
- `devlog.md`: Records development progress and problems encountered.

## Running the program

From the project directory, run:

```sh
python3 driver.py activity.log
```

Use `password` to set a key before using `encrypt` or `decrypt`. The other commands are `history` and `quit`. Passwords and strings must contain only letters A–Z; lowercase input is converted to uppercase (there should already be error checking for this). If there is no log file, it will get created by the program and new entires will get appended in case it already exists. 
