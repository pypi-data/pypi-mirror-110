  Fcomp - short for file/folder comparison
  
  Function receives the path and analyzes the directory it represents in order to find the files/directories of maximum and minimum sizes that the initial folder contains.
  Then returns paths to those files.
  Necessary info can be taken from returned dictionary with the use of keys "maxs","mins" and "eq"(if somehow all contents of a directory have equal size). 
  In case of a path to an empty directory inputted as argument None is returned.
  
  !!!
  Usage of backslash in paths should be avoided due to it causing the function to fail (SyntaxError).
  Either double backslash or slash should be used instead. Alternatively, the path can be initially inputted as raw, e.g. fcomp(r'C:\Users')
