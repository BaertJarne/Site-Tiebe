from mysql import connector
import os


class Database:

    # 1. connectie openen met classe variabelen voor hergebruik
    @staticmethod
    def __open_connection():
        try:
            db = connector.connect(option_files=os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.py")), autocommit=False)
            if "AttributeError" in (str(type(db))):
                raise Exception("\033[0mFoutieve database parameters in config\033[0m")
            cursor = db.cursor(dictionary=True, buffered=True)  # lazy loaded
            return db, cursor
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("\033[0mError: Er is geen toegang tot de database\033[0m")
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                print("\033[0mError: De database is niet gevonden\033[0m")
            else:
                print(err)
            return

    # 2. Executes READS
    @staticmethod
    def get_rows(sqlQuery, params=None):
        result = None
        db, cursor = Database.__open_connection()
        try:
            cursor.execute(sqlQuery, params)
            result = cursor.fetchall()
            cursor.close()
            if result is None:
                print(ValueError(f"\033[0mResultaten zijn onbestaand.[DB Error]\033[0m"))
            db.close()
        except Exception as error:
            print(error)  # development boodschap
            result = None
        finally:
            return result

    @staticmethod
    def get_one_row(sqlQuery, params=None):
        db, cursor = Database.__open_connection()
        try:
            cursor.execute(sqlQuery, params)
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                raise ValueError("\033[0mResultaten zijn onbestaand.[DB Error]\033[0m")
        except Exception as error:
            print(error)  # development boodschap
            result = None
        finally:
            db.close()
            return result

    # 3. Executes INSERT, UPDATE, DELETE with PARAMETERS
    @staticmethod
    def execute_sql(sqlQuery, params=None):
        result = None
        db, cursor = Database.__open_connection()
        try:
            cursor.execute(sqlQuery, params)
            db.commit()
            # bevestigig van create (int of 0)
            result = cursor.lastrowid
            # bevestiging van update, delete (array)
            # result = result if result != 0 else params  # Extra controle doen!!
            if result != 0:  # is een insert, deze stuur het lastrowid terug.
                result = result
            else:  # is een update of een delete
                if cursor.rowcount == -1:  # Er is een fout in de SQL
                    raise Exception("\033[0mFout in SQL\033[0m")
                elif (
                    cursor.rowcount == 0
                ):  # Er is niks gewijzigd, where voldoet niet of geen wijziging in de data
                    result = 0
                elif result == "undefined":  # Hoeveel rijen werden gewijzigd
                    raise Exception("\033[0mSQL error\033[0m")
                else:
                    result = cursor.rowcount
        except connector.Error as error:
            db.rollback()
            result = None
            print(f"\033[0mError: Data niet bewaard.{error.msg}\033[0m")
        finally:
            cursor.close()
            db.close()
            return result