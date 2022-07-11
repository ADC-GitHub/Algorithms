#-----------------------------------------------------------------------------------
# Program to read a set and automatically create unit test tcf files
#
# Pre-requisites : Requires Python 2.7 or above
#
# Author : M.W.Richardson   
# Date   : 19/11/2021
# 
# Copyright (C) 2021 Liverpool Data Research Associates
#-----------------------------------------------------------------------------------

import os
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

#-----------------------------------------------------------------------------------------------------------------------
  
# Create a log file
# -----------------
log = open('Create_Unit_Test_TCFs.log','a')


# Get all the passed arguments
# ----------------------------
if not len(sys.argv) == 4:
  log.write('Error: Incorrect number of arguments! Usage: ' + sys.argv[0] + ' project name, xml file, tcf folder\n' )
  sys.exit(1)

proj_name  = sys.argv[1]
xml_file   = sys.argv[2]
tcf_folder = sys.argv[3]

log.write('Project Name: ' + proj_name + '\n')
log.write('XML File    : ' + xml_file + '\n')

# Check that the tcf folder exists
# --------------------------------
if not os.path.isdir(tcf_folder):
  log.write('Error: The folder ' + tcf_folder + ' does not exist\n')
  sys.exit(1)


# Find all the functions in the xml file
# --------------------------------------
tree = ET.parse(xml_file)
root = tree.getroot()
files = []
functions = 0
updated_tcfs = 0
existing_tcfs = 0
created_tcfs = 0

for file in root.findall('file'):
  files.append( file.get('name') )

for file in root.findall('file'):
  file_name = file.get('name')
  pos = file_name.rfind('.')
  filename= file_name[:pos]
  log.write('\nFile: ' + file_name + '\n')
  for elem in file.iter():
    if (elem.tag == 'functions'):
      for func in elem.findall('function'):
        func_name = func.get('name')
        if not (func_name == 'main'):
          functions = functions + 1
          log.write('  Function: ' + '{:<32}'.format(func_name))
          tcf_file = 'ut_' + filename + '_' + func_name + '.tcf'
          # if the tcf_file doesn't exist 
          # or if it does exist, but contains 'GENERATED_BY = Create_Unit_Test_TCFs.bat'
          # Then create the file, else do nothing
          bExists = False
          bUpdate = False
          if os.path.isfile(tcf_folder + '\\' + tcf_file):
            bExists = True
            with open(tcf_folder + '\\' + tcf_file,'r') as tcf:
              for line in tcf:
                if 'GENERATED_BY = Create_Unit_Test_TCFs.bat' in line:
                  bExists = False
                  bUpdate = True
                  break
            tcf.close
          
          if bExists == True:
            log.write('Exists  ' + tcf_file + '\n')
            existing_tcfs = existing_tcfs + 1
          else:
            if bUpdate == True:
              log.write('Updated ' + tcf_file + '\n')
              updated_tcfs = updated_tcfs + 1
            else:
              log.write('Created ' + tcf_file + '\n')
              created_tcfs = created_tcfs + 1
              
            tcf = open(tcf_folder + '\\' + tcf_file,'w')
            tcf.write( '# Begin Testbed Set\n' )
            tcf.write( '  SET_TYPE = SYSTEM\n' )
            tcf.write( '  SET_NAME = ' + proj_name + '\n' )
            tcf.write( '  GENERATED_BY = Create_Unit_Test_TCFs.bat\n' )
            tcf.write( '  # Begin Source Files\n' )
            for f in files:
              tcf.write( '    RelativeFile = .\\' + f + '\n' )
            tcf.write( '  # End Source Files\n' )
            tcf.write( '# End Testbed Set\n\n' )
            
            tcf.write( '# Begin Text\n' )
            tcf.write( 'This sequence tests the function ' + func_name + '\n' )
            tcf.write( '# End Text\n\n' )

            tcf.write( '# Begin Attributes\n' )
            tcf.write( '  Sequence Name = ut_' + filename + "_" + func_name + '\n' )
            tcf.write( '  Language Code = 2\n' )
            tcf.write( '# End Attributes\n\n' )

            tcf.write( '# Begin Properties\n' )
            tcf.write( '  IBox = Light Grey\n' )
            tcf.write( '# End Properties\n\n' )

            tcf.write( '# Begin Isolated Procedure\n' )
            tcf.write( '  File = .\\' + file_name + '\n' )
            tcf.write( '  Procedure = ' + func_name + '\n' )
            tcf.write( '# End Isolated Procedure\n\n' )

            tcf.write( '# Begin Selected Files from Set\n' )
            tcf.write( '  .\\' + file_name + '\n' )
            tcf.write( '# End Selected Files from Set\n\n' )

            tcf.write( '# Begin Excluded Files\n' )
            for f in files:
              if not (file_name == f):
                tcf.write( '  .\\' + f + '\n' )
            tcf.write( '# End Excluded Files\n\n' )

            tcf.write( '# Begin White Files\n' )
            tcf.write( '  .\\' + file_name + '\n' )
            tcf.write( '# End White Files\n\n' )
            tcf.close

log.write('\n\nTotal number of functions: ' + str(functions) + '\n')
log.write('Existing TCFs: ' + '{:>3}'.format(str(existing_tcfs)) + '\n')
log.write('Updated TCFs:  ' + '{:>3}'.format(str(updated_tcfs)) + '\n')
log.write('Created TCFs:  ' + '{:>3}'.format(str(created_tcfs)) + '\n')
