REMOTE=${pi}
echo PI addrees is "${REMOTE}"
REMOTE_DIR=/home/pi/karel-pupper-api/StanfordQuadruped

scp -r $(pwd)/StanfordQuadruped/programs pi@${REMOTE}:${REMOTE_DIR}
