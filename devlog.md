##  10/12/2026 4:56 pm

According to the project details, I have to create three processes: a driver, an encryption backend, and a logger. The driver is supposed to  start the other programs using Python's subprocess module and then the pipes connect the driver to the child programs' I/O. I then use the python starter code to demonstrate the entire process and handle commands as needed.

I'm intially just setting up the files that I need and will plan below. The next thing I plan to do is create the logger first. I need to think about how to properly parse the input and discard anything that is not right (wrong input) properly. I have a question about how to handle the various problems I might face like wrong files or wrong input, but I think I can work it out by just running through input validation before any proper actions are done.

##  10/12/2026 5:43 pm

Logger.py can now accept a file name for logging and reads the user's messages from input. If there is already a file, then it appends but if not then it creates a new one. The process basically works by splitting message based on action and message to know what to log. Initially, I understood that I needed to command arguments, but forgot midway and started coding it as if user is inputing through regular I/O. I was able to fix this once I check the requirements again.

I still have to implement it so that the logger receieves messages from a pipe rather than a user, so I still have to figure out how to connect it. I wonder whether errors from pipe will cascade down but I have to ensure I can catch them properly. 