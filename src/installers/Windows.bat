#install wsl, pip, pwinput
echo Running Installer
wsl --install
python -m ensurepip --upgrade 
pip install pwinput

python3 ./src/main.py
