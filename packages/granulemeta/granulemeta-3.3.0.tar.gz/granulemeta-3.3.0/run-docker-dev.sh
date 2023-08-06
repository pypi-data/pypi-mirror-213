#!/bin/bash

# Put command line args into sensibly named variables.
inpath=${1-.}
outpath=`pwd`

# Set some environment variables from command line args.
export INPUT_PATH=inpath
export OUTPUT_PATH=outpath
export OUTPUT_NAME=""

# Build docker container for granulemeta dev use.
docker-compose build v3_gm_dev > /dev/null

# Run v3_gm_dev docker container.
echo "Executing v3_gm_dev"
docker run -a stdin -a stdout -it \
           --user $(id -u):$(id -g) \
           --name v3_gm_dev_container \
           --volume $inpath:/data \
           --volume $outpath:/code \
           v3_gm_dev

# Remove the container and anonymous volumes asociated with it.
docker rm --volumes v3_gm_dev_container > /dev/null