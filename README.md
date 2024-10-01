# timing-attack
Python Script used to attempt a brute force timing attack against a password protected binary. 
This Python script performs a timing-based brute-force attack on an external binary program (vault.o). The program guesses a password character by character using the time it takes for each guess to be processed by the binary. By measuring the response time for each character, it determines the correct password one character at a time.

Features
-Brute-force attack based on timing: The script uses statistical timing analysis to find the correct password for the vault.o binary.
-Logging: All password guesses, results, and errors are logged to a file (timing_attack_log.txt) as well as printed to the console.
-Customization: You can modify the maximum password length and the number of trials for each password guess.

How It Works

The script calls the external program (vault.o) using Python's subprocess.run() function.
It guesses a password, character by character, and measures the time it takes for the external program to process each guess.
By running multiple trials and averaging the response times, the script identifies which character takes the longest, indicating that it is the correct character for that position in the password.
The process repeats until the full password is discovered.
