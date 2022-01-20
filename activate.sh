REMOTE=${pi}
ssh -t pi@${REMOTE} 'cd karel-pupper-api/StanfordQuadruped && python3 activate.py'
