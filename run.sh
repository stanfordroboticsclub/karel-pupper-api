/bin/bash ./deploy.sh
REMOTE=10.34.168.21
echo PI addrees is "${REMOTE}"
REMOTE_DIR=/home/pi/karelPupper
DEFAULT_PROGRAM=karel-pupper-test.py
if [ "$#" -ne 1 ]; then
    echo "Running default file"
    ssh -t pi@${REMOTE} 'cd karelPupper/karel-pupper-api/StanfordQuadruped/programs && python3 '${DEFAULT_PROGRAM}''
else
  ssh -t pi@${REMOTE} 'cd
  karelPupper/karel-pupper-api/StanfordQuadruped/programs && python3 '$1''

fi
