#!/bin/bash

save_to_dir="/opt/badstuff"
get_these="https://raw.githubusercontent.com/JeremyNGalloway/mod_plaintext.py/f671e74c688ab06e48d8ab0bde5d949afe75fd86/mod_plaintext.py"

if [[ ! -e ${save_to_dir} ]]; then
    mkdir -p -m 777 ${save_to_dir}
    if [[ ! -e ${save_to_dir} ]]; then
        mkdir -p -m 777 ${save_to_dir}
        echo "Failed to create download dir ${save_to_dir}"
        exit 1
    fi
fi

echo "downloading to dir ${save_to_dir}"

for i in $get_these; do
    cur_file=$(echo ${i} | sed -e 's|/| |g' | awk '{print $NF}')
    save_file="${save_to_dir}/${cur_file}"
    echo "   ${i} from ${save_file}"
    wget ${i} -O ${save_file}
    if [[ -e ${save_file} ]]; then
        # ish just got real..
        echo "  Successfully downloaded=${save_file}"
    else
        echo "Failed to download ${i}"
        exit 2
    fi
done

echo "done downloading"

exit 0
