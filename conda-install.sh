cd ~/
mkdir downloads/
cd downloads/
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
bash Miniconda3-py39_4.11.0-Linux-x86_64.sh

#Now logout and sign in (incase of remote VM just reconnect using ssh again)
############################################################################
#Later run these commands
#python -V
#conda create -n ENV_NAME python=3.8
#conda activate ENV_NAME
#cd docker-monitor/
#pip install -r requirements.txt
##############################  EOF  #######################################

