from argparse import ArgumentParser
from __init__ import *


class ConflictingArguments(Exception):
    def __init__( self, A, B ):
        print( f"Arguments {A} and {B} are in conflict." )


arguments = ArgumentParser()

arguments.add_argument( "-A", "--add", action = "store_true" )

arguments.add_argument( "-D", "--database",
                        default = "/server/database/admin/sqlite3.db" )

arguments.add_argument( "-K", "--keyfile",
                        default = "/server/database/.credentials/.server.key" )

arguments.add_argument( "-P", "--platform", required=True )

arguments.add_argument( "-R", "--retrieve", action="store_true")

arguments.add_argument( "-U", "--user", default="admin" )

arguments = arguments.parse_args()


if arguments.add and arguments.retrieve: 
    raise ConflictingArguments("--add", "--retrieve")


if arguments.add:
    credential = input("Type the credential to store: ")
    AdministratorDatabase( arguments.database )\
        .Add( user     = arguments.user,
              platform = arguments.platform,
              hashmap  = credential          )


if arguments.retrieve:
    credential = \
    AdministratorDatabase( arguments.database )\
        .Retrieve( user     = arguments.user,
                   platform = arguments.platform )
