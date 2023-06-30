echo Running Installer
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
pip install pwinput

mkdir -p Keybird/src
echo "python3 ./src/main.py" > Keybird/src/start.sh

cd Keybird
rm "get-pip.py"
python3 ./src/main.py
