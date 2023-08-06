'''Simple program that reads a template file and creates the folder structure and files based on the template.
The inverse can also be done, it can read a folder structure and create a template file based on it.
'''

__version__ = '0.1'

import os
import argparse
import re
import shutil

def main():
    parse=argparse.ArgumentParser(prog="Templater", description='Simple program that reads a template file and creates the folder structure and files based on the template. The inverse can also be done, it can read a folder structure and create a template file based on it.')
    parse.add_argument('-i', '--input', help='Input file or folder', required=True)
    parse.add_argument('-t', '--type', help='Type of operation. Can be template (generate template from directory) or create (generate directory from template file)', required=True) # template(generate template file from directory) or create(generate directory from template file)
    parse.add_argument('-o', '--output', help='Output file or folder')

    # Meta inputs
    parse.add_argument('-v', '--variables', help='Variables to be used in the template file metadata', nargs='*')

    args=parse.parse_args()

    type = args.type
    input = args.input
    output = args.output
    inputsList = args.variables

    metaInputs = {}

    if(inputsList != None):
        for field in inputsList:
            if '=' not in field:
                print('Invalid meta input.')
                return
            
            field = field.split('=')
            metaInputs[field[0]] = field[1]

    if type == 'template':
        template(input, output, metaInputs)
            
    elif type == 'create':
        create(input, output, metaInputs)

    else:
        print('Invalid operation type. Should be template (generate template from directory) or create (generate directory from template file).')


######################################################################################################
###################### Create template file based on folder structure and files ######################
######################################################################################################

def folderStructure(folder):
    dic = {}
    #list of files and folders
    files = os.listdir(folder)
    for f in files:
        #if it is a folder
        if os.path.isdir(folder + "/" + f):
            new_folder = folder + "/" + f
            dic[f] = folderStructure(new_folder)
        else:
            #if it is a file
            dic[f] = "file"
    return dic

def makeTreeTemplate(folder, counter):
    if counter == 0:
        tree = '''=== tree\n'''
    else:
        tree = ""

    file_content = ""

    c = counter

    dic = folderStructure(folder)

    for key in dic:
        if dic[key] == "file":
            if counter == 0:
                tree += key + "\n"
                pathname = folder + "/" + key
                file_content += makeContentTemplate(pathname)+"\n\n"
            else:
                pathname = folder + "/" + key
                tree += "\t"*c + "- " + key + "\n"
                file_content += makeContentTemplate(pathname)+"\n\n"
        else:
            if counter == 0:
                tree += key + "/\n"
                new_folder = folder + "/" + key
                treeRes, contentRes = makeTreeTemplate(new_folder, c+1)
                tree += treeRes
                file_content += contentRes
            else:
                tree += "\t"*c + "- " + key + "/\n"
                new_folder = folder + "/" + key
                treeRes, contentRes = makeTreeTemplate(new_folder, c+1)
                tree += treeRes
                file_content += contentRes
            
    return tree, file_content

def makeMetaTemplate(meta):
    metaString = "=== meta\n\n"
    for key in meta.keys():
        metaString += key + ": " + meta[key] + "\n"
    return metaString

def makeContentTemplate(file):
    #take only the name of the file
    content = "=== " + file + "\n"

    with open(file, "r") as f:
        content += f.read()

    return content

def template(input, output, metaInputs={}):
    output = "template.txt" if output == None else output
    tree, file_content = makeTreeTemplate(input, 0)
    meta = makeMetaTemplate(metaInputs)

    with open(output, "w") as f:
        f.write(meta +"\n" + tree +"\n" + file_content)

######################################################################################################
###################### Create folder structure and files based on template file ######################
######################################################################################################

def create(input, output, metaInputs={}):
    output = "/dist" if output == None else output
    if (output[0]!='/'):
        output='/'+output

    with open(input, 'r') as f:
        text = f.read()
        splittedText = re.split(r'=== (\S+)', text)
        splittedText=splittedText[1:]


        if(splittedText[0]=='meta'):
            meta = getMeta(splittedText[1], metaInputs)
        else:
            print('Invalid template file.')
            return
        if(splittedText[2]=='tree'):
            fileDict= parseTree(meta, output, splittedText[3])
        else:
            print('Invalid template file.')
            return
        
        fileAndContent = splittedText[4:]
        files=[]
        for i in range(0, len(fileAndContent), 2):
            files.append((applyMeta(meta, fileAndContent[i]),applyMeta(meta, fileAndContent[i+1])))

        for file in files:
            with open(fileDict[file[0]], 'w') as f:
                f.write(file[1])

def getMeta(metaString, metaInputs):
    matches = re.finditer(r'(\w+?):\s*(\w*)', metaString)

    meta = metaInputs
    for match in matches:
        if(match.group(1) not in metaInputs):
            if(match.group(2) == ''):
                value=input(match.group(1)+': ')
            else:
                value=match.group(2)
            meta[match.group(1)] = value

    return meta

def applyMeta(meta, string):
    for key in meta:
        string = string.replace('{{'+key+'}}', meta[key]).strip()
    return string

def parseTree(meta, output, treeString):
    treeString=applyMeta(meta, treeString).strip()

    files = {} # key: file name, value: file path

    parentDir = os.getcwd()+output
    try:
        os.mkdir(parentDir)
        os.chdir(parentDir)
    except FileExistsError:
        shutil.rmtree(parentDir)
        os.mkdir(parentDir)
        os.chdir(parentDir)

    
    result = {}
    lines = treeString.strip().split('\n')

    most_recent_parentAtDepth = {0: result}

    parentCycle=result

    for index in range(len(lines)):
        parentCycle = process_line(lines, index, parentCycle, most_recent_parentAtDepth, result)

    createFolderStructure(result, parentDir+"/", files, "")

    return files

def createFolderStructure(parent, parentDir, files, fileDir):
    for key in parent:
        if parent[key] == "file":
            files[fileDir+key] = parentDir + key
            open(key, 'w').close()
        else:
            os.mkdir(key)
            os.chdir(key)
            createFolderStructure(parent[key], parentDir + key, files, fileDir + key)
            os.chdir("..")

def process_line(lines, index, parent, most_recent_parentAtDepth, result):
    line=lines[index]
    depth = (len(line) - len(line.lstrip()))/4
    name = line.strip()

    if depth == 0:
        parent = result

    if index + 1 < len(lines): # if not out of bounds
        next_line = lines[index + 1]
        next_depth = (len(next_line) - len(next_line.lstrip()))/4

        if next_depth > depth: # if next line is a child
            if name not in parent:
                if name.endswith('/'):
                    parent[name] = {}
                else:
                    parent[name] = "file"
            most_recent_parentAtDepth[next_depth] = parent[name]
            return parent[name]

        elif next_depth == depth: # if next line is a sibling
            if name not in parent:
                if name.endswith('/'):
                    parent[name] = {}
                else:
                    parent[name] = "file"
            return parent

        else: # if next line is a parent or grandparent...
            if name not in parent:
                if name.endswith('/'):
                    parent[name] = {}
                else:
                    parent[name] = "file"
            return most_recent_parentAtDepth[next_depth]
    else:
        if name not in parent:
            if name.endswith('/'):
                    parent[name] = {}
            else:
                parent[name] = "file"
        return parent


if __name__ == '__main__':
    main()

