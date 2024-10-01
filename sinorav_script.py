import subprocess
import time
import string
import logging
import statistics

"""
This module performs a timing-based brute-force attack on the vault.o program to 
guess a password character by character.
"""

# Configure logging to output to a file and the console
logging.basicConfig(filename='timing_attack_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)


def check_password(guess, trials=100):
    """
    This function checks the guessed password by calling the vault.o program.
    It measures the execution time for each guess over multiple trials.
    
    Args:
        guess (str): The password guess to be tested.
        trials (int): Number of trials to average the timing over.

    Returns:
        tuple: The average time taken and the variance over the trials.
    """
    times = []
    
    logging.info("Testing password: %s", guess)
    
    for _ in range(trials):
        start_time = time.perf_counter()

        try:
            subprocess.run(['./vault.o', guess], capture_output=True, check=True)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            times.append(elapsed_time)

        except subprocess.CalledProcessError as e:
            logging.error("Exception occurred while running vault.o: %s", e)

    avg_time = sum(times) / trials if trials > 0 else 0  
    variance = statistics.variance(times) if len(times) > 1 else 0.0  
    
    return avg_time, variance


def brute_force_password_by_position(max_length=12, trials=100):
    """
    This function performs a brute-force attack to guess a password character by character,
    focusing on timing for each position.
    
    Args:
        max_length (int): Maximum possible length of the password.
        trials (int): Number of trials for each guess.

    Returns:
        str: The cracked password.
    """
    possible_chars = string.ascii_lowercase
    password = ""
    
    for position in range(max_length):
        best_time = 0
        best_char = ""
        
        for char in possible_chars:
            guess = password + char + 'a' * (max_length - len(password) - 1)
            elapsed_time, variance = check_password(guess, trials)
            
            logging.info(
                "Position %d, Guess %s, Elapsed Time: %.6f, Variance: %.6f", 
                position + 1, char, elapsed_time, variance
            )
            
            if elapsed_time > best_time:
                best_time = elapsed_time
                best_char = char
                logging.info(
                    "Best character at position %d: %s, time: %.6f", 
                    position + 1, best_char, best_time
                )
        
        password += best_char
        logging.info("Password so far: %s", password)
    
    return password


def find_password_by_timing(max_length=12, trials=100):
    """
    This function manages the overall brute-force attack, logging and returning the final cracked password.
    
    Args:
        max_length (int): Maximum possible length of the password.
        trials (int): Number of trials for each guess.

    Returns:
        str: The final cracked password.
    """
    logging.info("Starting brute-force attack focusing on timing per position")
    cracked_password = brute_force_password_by_position(max_length, trials)
    logging.info("Final Cracked Password: %s", cracked_password)
    return cracked_password


# Start the timing attack per character position
final_password = find_password_by_timing(max_length=12, trials=100)

if final_password:
    logging.info("Cracked Password: %s", final_password)
