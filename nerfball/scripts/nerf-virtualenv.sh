#!/bin/bash

venv_python=""
if [[ "${1}" == "" ]]; then
    echo "Please provide a path to the virtualenv python binary like: <venv path>/bin/python"
    exit 1
else
    venv_python="${1}"
fi

if [[ ! -e ${venv_python} ]]; then
    echo ""
    echo "Please provide a path to the virtualenv python binary like: <venv path>/bin/python"
    echo ""
    exit 1
fi

lib_base_dir=$(echo ${venv_python} | sed -e "s|/bin/python|/lib|g")
python_version=$(ls $(echo "${lib_base_dir}") | grep python)
path_to_python_dir="${lib_base_dir}/${python_version}"

echo ""
echo "-----------------------------------------"
echo "Python lib dir: ${lib_base_dir}"
echo "Python version: ${python_version}"
echo "Install path:   ${path_to_python_dir}"
echo "-----------------------------------------"
echo ""

importlib_src=$(echo "${path_to_python_dir}/importlib")
if [[ -h ${importlib_src} ]]; then
    mkdir -p -m 777 /tmp/backup_importlib >> /dev/null
    cp -r ${importlib_src}/* /tmp/backup_importlib/
    echo "Removing importlib"
    rm -f ${importlib_src}
    cp -r /tmp/backup_importlib ${importlib_src}
fi

files="imp.py os.py subprocess.py importlib/machinery.py"
echo ""
echo ""
echo "Installing"
for i in $files; do

    delete_sym=1
    src=./nerfball/${i}
    dst=$(echo ${path_to_python_dir})
    file_count=$(ls -l ${dst} | grep ${i} | wc -l)
    
    if [[ "${i}" == "importlib/machinery.py" ]]; then
        dst=$(echo "${path_to_python_dir}/importlib/")
    elif [[ "${i}" == "os.py" ]]; then
        if [[ "${python_version}" == "python3.6" ]]; then
            src=./nerfball/nerfed_3_6_os.py
            dst=$(echo "${path_to_python_dir}/os.py")
            echo "  remove  sym=${dst}"
            echo "          pre=$(ls -lrt ${dst})"
            rm ${dst}
        elif [[ "${python_version}" == "python3.5" ]]; then
            src=./nerfball/os.py
            dst=$(echo "${path_to_python_dir}/os.py")
            echo "  remove  sym=${dst}"
            echo "          pre=$(ls -lrt ${dst})"
            rm ${dst}
        else
            src=./nerfball/os.py
        fi
    else
        if [[ "${file_count}" == "1" ]]; then
            echo ""
            echo "=${dst}="
            echo ""
            echo ""
            echo ""
            echo "  remove  sym=${dst}"
            echo "          pre=$(ls -lrt ${dst})"
            rm ${dst}/${i}
            dst=$(echo "${path_to_python_dir}/")
        fi
    fi

    echo "  install src=${src}"
    echo "          dst=${dst}"
    cp ${src} ${dst} 
    if [[ "$?" != "0" ]]; then
        echo ""
        echo "Failed to install new file=${i} to dst=${dst}"
        exit 2
    fi
    echo "          post=$(ls -lrt ${dst})"
done

echo ""

exit 0
