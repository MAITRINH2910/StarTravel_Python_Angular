import subprocess
import json
import os
cwd = os.getcwd() + '/'

try:
    subprocess.check_call(["docker", "stop", "hotelrecommendservice"])
    subprocess.check_call(["docker", "rm", "hotelrecommendservice"])
except:
    pass
subprocess.check_call(["docker", "build", "--tag=hotelrecommendservice:v0.0.1", "."])
subprocess.check_call(["docker", "run", "--mount","type=bind,source="+cwd+",target=/app", "-d", "-it","--restart", "unless-stopped", "--name", "hotelrecommendservice", "-p", "9999:9999","hotelrecommendservice:v0.0.1"])
# subprocess.check_call(["docker", "run", "-d", "-it","--restart", "unless-stopped", "--name", "hotelrecommendservice", "-p", "9999:9999", "hotelrecommendservice:v0.0.1"])



# subprocess.check_call(["docker", "run", "-v","audio-data:/app", "-d","--restart", "unless-stopped", "--name", "hotelrecommendservice", "-p", "9999:9999", "--env", "configs="+configs, "hotelrecommendservice:v0.0.1"])
# subprocess.check_call(["docker", "run", "-d", "--restart", "unless-stopped", "--name", "hotelrecommendservice", "-p", "9999:9999", "hotelrecommendservice:v0.0.1"])
# subprocess.check_call(["docker", "run", "-d", "--restart", "unless-stopped", "--name", "hotelrecommendservice", "-p", "9999:9999", "--env", "configs="+configs, "hotelrecommendservice:v0.0.1"])
