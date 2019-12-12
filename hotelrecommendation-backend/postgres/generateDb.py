import subprocess
import time

# import os
# cwd = os.getcwd()

POSTGREST_CONTAINER = 'hoteldb'
USER = 'postgres'
PASSWORD = 'postgres'
DATABASE = 'estay'

image_path = 'postgresql-11.2.tar.gz'#'./postgres_11.2-alpine.tar'
core_db_path = './db'
create_db_command = "create database "+DATABASE
schema_path = 'db.sql'

try:
    subprocess.check_call(['docker', 'load', '--input', image_path])
except:
    print('Image already Exists!')

try:
    subprocess.check_call(["docker", "stop", POSTGREST_CONTAINER])
    subprocess.check_call(["docker", "rm", POSTGREST_CONTAINER])
except:
    print('container is not running')

try:
    subprocess.check_call(['docker', 'run', '-d', '--restart', 'unless-stopped', '--name', POSTGREST_CONTAINER, '-e', 'POSTGRES_PASSWORD='+PASSWORD, '-e', 'POSTGRES_DB=postgres-core_data_pg', '-v', core_db_path, '-p', '5434:5432', 'postgres:11.2-alpine'])
except:
    print('run failed')

time.sleep(10)
try:
    subprocess.check_call(['docker','exec','-i',POSTGREST_CONTAINER,'psql','-U','postgres','-c',create_db_command])
except Exception as e:
    print(e)

time.sleep(20)
try:
    proc = subprocess.Popen(['docker','exec','-i',POSTGREST_CONTAINER,'psql','-U',USER,'-d',DATABASE],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    out, err = proc.communicate(open(schema_path,'rb').read())
    print('cccccc')
except Exception as e:
    print(e)

print('Done')
time.sleep(10)



# try:
#     subprocess.check_call(['docker', 'run', '-d', '--restart', 'unless-stopped', '--name', POSTGREST_CONTAINER, '-e', 'POSTGRES_PASSWORD=postgres', '-e', 'POSTGRES_DB=postgres-core_data_pg', '-v', core_db_path, '-p', '5434:5432', 'postgres:11.2-alpine'])
# except:
#     print('Coredb already running!')

# time.sleep(5)

# try:
#     subprocess.check_call(['cat','dump_bk.sql','|','docker','exec','-i',POSTGREST_CONTAINER,'psql','-U','postgres'])
# except:
#     print('Backup failed')

# try:
#     subprocess.check_call(['docker','exec','-i',POSTGREST_CONTAINER,'psql','-U','postgres','-c',create_db_command])
# except:
#     print('Database already exists!')

# time.sleep(5)

# proc = subprocess.Popen(['docker','exec','-i',POSTGREST_CONTAINER,'psql',"-U",'postgres','-d','estay'],
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE)
# out, err = proc.communicate(open(schema_path,'rb').read())
