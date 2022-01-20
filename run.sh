/bin/bash ./reset.sh
/bin/bash ./deploy.sh
REMOTE=${pi}
echo PI addrees is "${REMOTE}"
REMOTE_DIR=/home/pi/karelPupper
DEFAULT_PROGRAM=karel-pupper-test.py
if [ "$#" -ne 1 ]; then
    echo "Running default file"
    ssh -t pi@${REMOTE} 'cd karel-pupper-api/StanfordQuadruped/programs && python3 '${DEFAULT_PROGRAM}''
else
  ssh -t pi@${REMOTE} 'cd karel-pupper-api/StanfordQuadruped/programs && python3 '$1''

fi
