conda create --name dataprocess python "mamba>=0.22.1"
conda activate dataprocess
mamba install ipywidgets
pip install opencc
mamba install pymongo
pip install -e .
pip install twine

python setup.py sdist bdist_wheel

pip install wheel
