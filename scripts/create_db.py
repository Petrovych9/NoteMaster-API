from app.db import Base, get_engine


def create_all_tables_in_main_db():

    Base.metadata.create_all(bind=get_engine())

    current_function = create_all_tables_in_main_db.__name__
    current_file = create_all_tables_in_main_db.__code__.co_filename
    print(f"Script: {current_file} --------- DONE")


if __name__ == '__main__':
    create_all_tables_in_main_db()
