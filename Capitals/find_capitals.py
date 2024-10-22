import logging

from src.utils.utils import clean_and_fill_db, push_capitals, fetch_world_capitals

def main():
    try:
        world_capitals = fetch_world_capitals()
        logging.info(f'Found {len(world_capitals)} world capital entries')

        clean_and_fill_db(world_capitals)
        logging.info('Database entries cleaned and filled successfully.')

        push_capitals(world_capitals)
        logging.info('A total of {len(world_capitals)} pushed to Notion successfully.')
    
    except Exception as e:
        logging.error(f'An error occurred: {e}', exc_info=True)

if __name__ == "__main__":
    capitals = main()