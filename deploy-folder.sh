REMOTE=10.34.168.21
echo PI addrees is "${REMOTE}"
REMOTE_DIR=/home/pi/karelPupper/

# scp -r $(pwd)/StanfordQuadruped/programs pi@${REMOTE}:${REMOTE_DIR}
scp -r $(pwd) pi@${REMOTE}:${REMOTE_DIR}

#rsync -avz ${PWD} pi@${REMOTE}:${REMOTE_DIR}
