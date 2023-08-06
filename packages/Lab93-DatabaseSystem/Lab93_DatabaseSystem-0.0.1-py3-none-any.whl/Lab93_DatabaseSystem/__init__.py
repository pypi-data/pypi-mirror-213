#!/bin/python3

from Lab93Cryptogram import CryptographyMethodsAPI
from sqlite3 import connect

class MissingCredential(Exception):
    def __init__( self, user, platform ):
        print(
            f"Can't find any credentials "
            f"to {platform} for {user};\n"
            f"                           "
            f"  --Are you sure it exists?"
        )


class AdministratorDatabase:
    """
    The database handler provides an interface for
    encrypting and decrypting  sensitive values in a
    sqlite3.db file.
    """

    def __init__( self,
                  keyfile:  str = "",
                  database: str = "" ):


        if keyfile == "":
            keyfile = (
                f"/server/database"
                f"/.credentials"
                f"/.server.key"
            )


        if database == "":
            database = (
                f"/server/database"
                f"/admin"
                f"/sqlite3.db"
            )

        # Define a global pointer to the database.
        self.db = database

        # Initialize the cryptography module.
        cryptogram = CryptographyMethodsAPI()
        self.crypt = cryptogram

        # Recreate the encryption key from file.
        with open(keyfile, "r") as keyfile:
            self.key = cryptogram.BuildKey(
                "".join( keyfile.read()\
                                .split("\n")[1:-2] )\
                   .encode()
            )


    def Add( self, user, platform, hashmap ):
        """
        Adds the plaintext value `hashmap` to the
        database, for a specific `platform` in association
        with a specific `user`.
        """

        connection = connect( self.db )
        cursor = connection.cursor()


        hashmap = self.crypt\
                      .Encryption( self.key, hashmap )


        cursor.execute( """INSERT OR IGNORE INTO 
                           credentials( user,
                                        platform,
                                        hash      )
                           VALUES(?,?,?);""",
                        ( user, platform, hashmap ) )

        return connection.commit()


    def Retrieve( self, user, platform ):
        """
        """

        connection = connect( self.db )
        cursor = connection.cursor()

        _credential = cursor.execute("""SELECT hash
                                        FROM credentials
                                        WHERE user=?
                                        AND
                                        platform=?;""",
                                     ( user, platform ) )\
                            .fetchall()

        if len( _credential ) > 0: pass

        else: raise MissingCredential( user,
                                       platform )
        return self.crypt\
                   .Decryption( self.key,
                                _credential[0][0] )

