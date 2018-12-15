echo "Welcom to Wayfair E-commerce"
echo "Group 6"

echo "Want to open notebook? y/n"
read input
if [ $input == "y" ] || [ $input == "Y" ]; then
    jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --notebook-dir='/WayfairFinal'
fi

echo "Want to open web application? y/n"
read input1
if [ $input == "y" ] || [ $input == "Y" ]; then
    python3 WayfairFinal/flask/app.py
fi

cd WayfairFinal
ls