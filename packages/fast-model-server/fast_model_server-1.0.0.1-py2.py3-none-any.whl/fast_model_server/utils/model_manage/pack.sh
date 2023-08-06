#!/bin/bash
model_path_name=$1
model_path=$2
work_path=$3

cp -rf "${model_path}/${model_path_name}" "$work_path/"
cd "$work_path" || exit
tar -czf "$work_path/${model_path_name}.tar.gz" "${model_path_name}"

linux_md5_cmd=$(which md5sum)
mac_md5_cmd=$(which md5)
if [ -n "$linux_md5_cmd" ]
then
  md5_str=$(md5sum "${work_path}/${model_path_name}.tar.gz" | awk -F " " '{print $1}')
else
  if [ -n "$mac_md5_cmd" ]
  then
    md5_str=$(md5 "${work_path}/${model_path_name}.tar.gz" | awk -F " " '{print $NF}')
  else
    exit
  fi
fi

mv "${model_path_name}.tar.gz" "${work_path}/model_file_XXX_${md5_str}"

rm -rf "${work_path}/${model_path_name}"
