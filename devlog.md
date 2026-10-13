##  10/12/2026 4:56 pm

According to the project details, I have to create three processes: a driver, an encryption backend, and a logger. The driver is supposed to  start the other programs using Python's subprocess module and then the pipes connect the driver to the child programs' I/O. I then use the python starter code to demonstrate the entire process and handle commands as needed.

I'm intially just setting up the files that I need and will plan below. The next thing I plan to do is create the logger first. I need to think about how to properly parse the input and discard anything that is not right (wrong input) properly. I have a question about how to handle the various problems I might face like wrong files or wrong input, but I think I can work it out by just running through input validation before any proper actions are done.

##  10/12/2026 5:43 pm

Logger.py can now accept a file name for logging and reads the user's messages from input. If there is already a file, then it appends but if not then it creates a new one. The process basically works by splitting message based on action and message to know what to log. Initially, I understood that I needed to command arguments, but forgot midway and started coding it as if user is inputing through regular I/O. I was able to fix this once I check the requirements again.

I still have to implement it so that the logger receieves messages from a pipe rather than a user, so I still have to figure out how to connect it. I wonder whether errors from pipe will cascade down but I have to ensure I can catch them properly. 

## 10/13/2026 1:07 pm

Now that I finished logger, I'm going to be working on encryption. I use a Vigenère cypher to encrypt and decrypt based on passkey. It only works on letters and is case-insentive so I wonder whether if non-letters just stay the same. 

I don't fully understand what it means by pass and setting it for encryption so I'm going to watch a quick video to understand it. As of right now, that is the main problem that I am facing. Later, I once start implementing the encryption, I'll think about to connect my driver to these two programs.

## 10/13/2026 2:54 pm

I was able to finish the encryption, but I ran into quite a few problems. First, I didn't realize that the pass command was supposed to return an error without replacing the older valid key when given an invalid password. I was originally changing the previous key, but found that it wasn't supposed to.

I also used isalpha() to check letters, but found that the cipher only wants regular letters not like é. After realizing that, I added it with isascii() so it is only uppercase and lowercase letters. Additionally, I had to fix my code to have the cipher wrap letters around the alphabet with modulo. I originally thought of the size as fixed so I didn't account for wrapping. I was able to understand it better after watching a small video on how the cipher works.

After encountering all of these problems, I tested it with the HELLO example and was able to encrypt it to OIWWC and decrypt it back to HELLO.

The next step is to determine how to use the driver to run the pipe between the encryption and logger files without losing information.