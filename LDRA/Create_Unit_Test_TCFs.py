#-----------------------------------------------------------------------------------
# Create_Unit_Test_TCFs.py
#
# syntax: python.exe Create_Unit_Test_TCFs.py tcf_folder
#
# For each file in the set.tcf, create setname_file_name.tcf
# In set_file.tcf remove all files, except file
#
# Requires Python27 or above
#
# Author : M.W.Richardson   
# Date   : 19/11/2021
# 
# Copyright (C) 2021 Liverpool Data Research Associates
#-----------------------------------------------------------------------------------

import os
import sys
import datetime

# Create a log file
# -----------------
log = open('Create_Unit_Test_TCFs.log','a')

try:
  import shutil
except:
  log.write('*** Error: Missing shutil, it is recommended to install Python27 or above\n')
  sys.exit(1)


# ----------------------------------------------------------------------------------
# Function to create a tcf file
# ----------------------------------------------------------------------------------
def create_tcf(tcf_folder, set_name, source_file_name, source_file):

  # Create the file_tcf
  # -------------------
  with open(tcf_folder + '\\' + set_name + '_' + source_file_name + '.tcf','w') as file_tcf:
    with open(cwd + '\\' + set_name + '.tcf','r') as set_tcf:
      for line in set_tcf:
        if not line.startswith('$'):
          if 'SET_NAME' in line:
            line = '   SET_NAME = ' + set_name + '_' + source_file_name + '\n'
            file_tcf.write( line )
          else:
            if 'GENERATED_BY' in line:
              line = ' GENERATED_BY Create_Unit_Test_TCFs.bat\n'
              file_tcf.write( line )
            else:
              line = line.replace('/','\\')
              if not 'File = ' in line:
                if not (line == '    \n'):
                  file_tcf.write( line )
              else:
                if source_file in line:
                  line = line[:-1]
                  file_tcf.write( line )
                  file_tcf.write( '\n   ' )

      set_tcf.close()
    file_tcf.close()

  return
# ----------------------------------------------------------------------------------



# Get all the passed arguments
# ----------------------------
if not len(sys.argv) == 2:
  log.write('*** Error: Incorrect number of arguments! Usage: ' + sys.argv[0] + ' set_name\n' )
  sys.exit(1)
set_name = sys.argv[1]


# Check that the tcf exists
# -------------------------
cwd = os.getcwd()
if not os.path.isfile(cwd + '\\' + set_name + '.tcf'):
  log.write('*** Error: The file ' + cwd + '\\' + set_name + '.tcf does not exist\n')
  sys.exit(1)
log.write('set_name: ' + set_name + '\n')


# Read list of all source files
# -----------------------------
source_files=[]
bSearchSection = True
with open(set_name + '.tcf','r') as tcf:
  for line in tcf:
    if not line.startswith('$'):
      if ('File = ' in line):
        source_file = line.strip ('File = ')
        # Ensure that the path only has backward slashes
        # ----------------------------------------------
        source_file = source_file.replace('/','\\')
        source_files.append(source_file )
tcf.close()


# Print out list of files
# -----------------------
for source_file in source_files:
  # Find the name of the file
  # -------------------------
  beg_pos = source_file.rfind('\\')
  end_pos = source_file.rfind('.')
  if end_pos > beg_pos:
    source_file_name = source_file[beg_pos+1:end_pos]
  else:
    log.write('*** Error: problem with file ' + source_file + '\n')
    log.write('beg = ' + str(beg_pos) + '\n')
    log.write('end = ' + str(end_pos) + '\n')
    sys.exit(1)
  
  create_tcf('UnitTests', set_name, source_file_name, source_file)
  log.write('source_file: ' + source_file_name + '\n' )

