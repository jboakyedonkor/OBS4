#!/bin/sh

cd OBS4
python main.py &
node_modules/bin/cypress run cypress/cypress/integration/sample.spec.js
exit