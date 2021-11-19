REMOTE=169.254.48.56
REMOTE=10.34.168.21
echo PI addrees is "${REMOTE}"
REMOTE_DIR=/home/pi/karelPupper

ssh pi@${REMOTE}  mkdir -p ${REMOTE_DIR}
rsync -avz ${PWD} pi@${REMOTE}:${REMOTE_DIR}
