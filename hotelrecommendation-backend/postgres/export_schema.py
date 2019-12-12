import subprocess

# export = "\! pg_dump --schema-only -U postgres -d audioconverter > db_schema.sql"
# subprocess.check_call(['docker','exec','-i','postgresdb','psql','-U','postgres','-c', export])

# subprocess.check_call(['docker','exec','-t','postgresdb','pg_dumall','-c','-U','postgres','>','db.sql'])

subprocess.check_call('docker exec -t hoteldb pg_dumpall -c -U postgres > db.sql',shell=True)