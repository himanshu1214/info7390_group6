# download original dataset
echo "Download data file? y/n"
read input
if [ $input == "y" ] || [ $input == "Y" ]; then
    python3 /midterm-case/Part1-Download.py
fi

# open notebook
echo "Want to open notebook? y/n"
read input1
if [ $input1 == "y" ] || [ $input1 == "Y" ]; then
    jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --notebook-dir='/midterm-case'
fi

# open terminal and come to midterm-case
/bin/bash
cd midterm-case

