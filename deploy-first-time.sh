REMOTE=${pi}
echo PI addrees is "${REMOTE}"
REMOTE_DIR=/home/pi/

scp -r $(pwd) pi@${REMOTE}:${REMOTE_DIR}