#!/bin/bash
unset LD_LIBRARY_PATH
declare -x PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:"${ASCENDPATH}""
readonly TRUE=1
readonly FALSE=0
readonly BASE_DIR=$(cd "$(dirname $0)" > /dev/null 2>&1; pwd -P)
readonly LOG_SIZE_THRESHOLD=$((20*1024*1024))
readonly LOG_COUNT_THRESHOLD=5

function operation_log_info()
{
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >> ${BASE_DIR}/downloader_operation.log
}

function log_info()
{
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[INFO] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >> ${BASE_DIR}/downloader.log
}

function log_error()
{
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[ERROR] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [ERROR] $*" >> ${BASE_DIR}/downloader.log
}

function rotate_log()
{
    local log_list=$(ls $1* | sort -r)
    for item in $log_list; do
        local suffix=${item##*.}
        local prefix=${item%.*}
        if [[ ${suffix} != "log" ]]; then
            if [[ ${suffix} -lt ${LOG_COUNT_THRESHOLD} ]];then
                suffix=$(($suffix+1))
                mv -f $item $prefix.$suffix
            fi
        else
            mv -f ${item} ${item}.1
            cat /dev/null > ${item}
        fi
    done
}

function check_log()
{
    if [[ ! -e $1 ]];then
        touch $1
    fi
    local log_size=$(ls -l $1 | awk '{ print $5 }')
    if [[ ${log_size} -ge ${LOG_SIZE_THRESHOLD} ]];then
        rotate_log $1
    fi
}

function set_permission()
{
    chmod 750 ${BASE_DIR}
    chmod 550 $0
    chmod 600 ${BASE_DIR}/downloader.log ${BASE_DIR}/downloader_operation.log 2>/dev/null
    chmod 400 ${BASE_DIR}/downloader.log.? ${BASE_DIR}/downloader_operation.log.? 2>/dev/null
}

function get_python3()
{
    # try this first
    py36="/usr/bin/python3"
    if [ -f ${py36} ];then
        echo ${py36}
        return 0
    fi

    # centos 8.2
    platform_python="/usr/libexec/platform-python3.6"
    if [ -f ${platform_python} ];then
        echo ${platform_python}
        return 0
    fi

    # this python3 maybe replace by user and have no lzma or other module
    have_python3=$(command -v python3 | wc -l)
    if [ ${have_python3} -eq 1 ];then
        echo python3
        return 0
    fi

    return 1
}

function main()
{
    check_log ${BASE_DIR}/downloader.log
    check_log ${BASE_DIR}/downloader_operation.log
    set_permission

    get_python3 >/dev/null 2>&1
    if [[ $? == 0 ]];then
        local pycmd=$(get_python3)
    else
        log_error "python3 is not available, install it first by running 'apt install -y python3' or 'yum install -y python3' with root permission and available repo accessing"
        return 1
    fi

    log_info "${pycmd} $(basename ${BASE_DIR})/ascend_download.py $@"
    ${pycmd} ${BASE_DIR}/ascend_download.py $@
}

main $*
main_status=$?
if [[ ${main_status} != 0 ]] && [[ ${main_status} != 2 ]];then
    operation_log_info "parameter error,run failed"
else
    operation_log_info "$0 $*: Success"
fi
exit ${main_status}
