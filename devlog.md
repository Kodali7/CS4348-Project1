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

## 10/15/2026 11:13 am

Now I have to complete the driver part of the project and connect pipes, logger, and encryption all together here. I need to use the subprocess library/module like the description stated to work with processes in python. With the subprocesses, I think I have to create separate child processes to read output from encryption to handle properly.

Since I'm in the driver which is mainly for user to use, I can't just have commands that make sense to me. I think I will have to create commands like password, encrypt, decrypt, etc and make it clear so user knows what they are selecting. I also need to find a way to log or have history for commands so I might have to keep track with numbers and show to user to display/select. I believe for input validation it should be the same as encryption and logger like how I have to split for commands and message info.

## 10/15/2026 4:46 pm

Creating the driver program took way longer than expected because I kept messing up using processes. I then used three process where two were child process which were for the other functionality like encrypting and logging. Also, I was originally doing the encryption request and response separately and that made the code more complex without a valid reason. However, I realized that I can handle them in the same command loop instead of creating separate functions for it.

To help me understand the code, I kept printing and did a bunch of error handling to let me know what parts are breaking within the code. One part I needed to understand was that the PASS command only returns RESULT without any message. To make that clearer, I made it so that the driver displays and logs RESULT Password set after the encryption program confirms that it was successful.

Another problem I initially faced was how to connect programs especially for logger to get the inputs from pipe. After looking at the code, I realized that I'm already using sys.stdin in other parts so I can just use that as well for the logger. While talking about logging, when dealing with QUIT, I made sure I let the child processes finish before we force kill the processes 

I tried the test provided again in the decription with HELLo and OIWWC and got the result that I was expecting without anything breaking. 

## 10/18/2026 4:32 pm
I plan to create a readme file so that people that aren't familiar with the project will be able to understand the overview of what I was trying to acheive. In the readme, I want to just give a very brief outline of what each file does so in case anyone wants to modify something, it's easier to find the responsible file.

## 10/18/2026 4:57 pm
I was able to create the readme file. I had no problems as all I was doing was just very briefly summarizing what I had done in this project and letting whoever reads it know the overview of this project.