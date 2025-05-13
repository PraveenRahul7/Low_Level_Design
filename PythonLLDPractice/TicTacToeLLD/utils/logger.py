import logging
import os

# Create logs directory if it does not exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Logger Configuration
logging.basicConfig(
    filename='logs/game.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'   # Overwrites log file each run; change to 'a' for append mode
)

# Console handler for live display
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)

# Add to the main logger
logging.getLogger().addHandler(console)

# Log functions
def log_info(message):
    logging.info(message)

def log_debug(message):
    logging.debug(message)

def log_error(message):
    logging.error(message)
