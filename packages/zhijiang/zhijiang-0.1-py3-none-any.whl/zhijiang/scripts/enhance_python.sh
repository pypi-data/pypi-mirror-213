# add usefule python function to builtins, so they can be call directly
# these functions will be prefixed with zhijxu to avoid name conflict
sitepy_path=`python -c "import site; print(site.__file__)"`
backup=`dirname $sitepy_path`/site.py_bk
if [ -f $backup ]
then
  ## restore site.py
  cp $backup $sitepy_path
else
  ## site.py is unchanged, so backup it
  cp $sitepy_path $backup
fi

pkg_script_path=`dirname $BASH_SOURCE`
cat $pkg_script_path/useful_func.py >> $sitepy_path

