#! /bin/sh
ansible_version=`ansible-playbook --version | grep -v '^ ' |cut -d ' ' -f 2`
ansible_dir=`ansible-playbook --version |grep 'ansible python module location' |cut -d '=' -f 2 |tr -d ' '`
fmgr_plugin_file=$ansible_dir"/plugins/httpapi/fortimanager.py"

#$1: the file to be patched
#$2: the patch file
patch_file() {
    echo "patching "$1
    if ! patch -R --dry-run -s -f  $1 < $2; then
        patch $1 < $2 > /dev/zero;
    fi
}

case $ansible_version in 
2.9.0)
    patch_file $fmgr_plugin_file ansible.2.9.x.patch
    ;;
2.9.1)
    patch_file $fmgr_plugin_file ansible.2.9.x.patch
    ;;
2.9.2)
    patch_file $fmgr_plugin_file ansible.2.9.x.patch
    ;;
*)
    echo "No need to patch ansible "$ansible_version
    ;;
esac


