#! /bin/bash


    echo "=================================="
    echo "=   請按 Ctrl + c 關閉此程式     ="
    echo "=   press Ctrl + c to close      ="
    echo "=================================="

python facedetect_line.py & python motoion_160_120.py & python key_control.py

read -p "請按Enter鍵離開" a
