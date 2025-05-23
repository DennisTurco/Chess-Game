import logging
import sys
from Frame import Frame

def configure_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
    )

def main():
    configure_logger()
    Frame()

if __name__ == "__main__":
    try: main()
    except: logging.exception(f"{sys.argv[0]}")