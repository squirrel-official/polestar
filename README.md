use ubuntu 32 bit only

python -m venv polestar-env

source polestar-env/bin/activate

sudo apt install -y python3-libcamera

sudo apt-get install libcap-dev

sudo apt-get install libopenblas-dev

sudo apt-get install gfortran

pip install -r requirements.txt


