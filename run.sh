nvidia-smi
echo $CUDA_VISIBLE_DEVICES
echo $HOSTNAME
which python
python -m pip list

#python ./test.py
python ./stable-dreamfusion/main.py --text "a hamburger" --workspace trial -O
