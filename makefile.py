import os
import sys
import shutil
import subprocess

OUTPUT_FOLDER_CLEANUP = "output_cleanup/"

def recursive_load(MAP, directory, base_dir):
    files = os.scandir(directory)
    for file in files:
        if file.is_file():
            MAP[directory].append(file.name)
            shutil.move(directory+file.name, base_dir)
        elif file.is_dir():
            foldername = directory+file.name+"/"
            MAP[foldername] = []
            recursive_load(MAP, foldername, base_dir)
    return MAP


def load_files(base_dir, to_load):
    MAP = {}
    MAP[to_load] = []
    return recursive_load(MAP, to_load, base_dir)


def put_back_files(files):
    for d in files:
        for f in files[d]:
            shutil.move(f, d)


def cleanup(base_dir, texfile):
    filename = texfile[:-4]
    base_name = os.path.basename(filename)
    ext = [".aux", ".nav", ".out", ".snm", ".toc"]
    if not os.path.exists(base_dir+OUTPUT_FOLDER_CLEANUP):
        os.mkdir(base_dir+OUTPUT_FOLDER_CLEANUP)
    for e in ext:
        destination = base_dir+OUTPUT_FOLDER_CLEANUP+base_name+e
        if os.path.isfile(filename+e):
            if os.path.isfile(destination):
                os.remove(destination)
            shutil.move(filename+e, destination)


if __name__ == "__main__":

    texfile = None

    # First argument is the name of the file
    if len(sys.argv) > 1:
        texfile = sys.argv[1]
    # Else ask the user
    else:
        texfile = input("Please select a .tex file : ")

    # Clean the input
    texfile = texfile.strip()
    if not texfile.endswith(".tex"):
        texfile += ".tex"

    # Put every files from the ./theme folder at the root
    files = load_files("./", "./theme/")

    try:
        # Call PDFLaTeX to generate the .pdf
        subprocess.call('pdflatex.exe -draftmode -interaction=nonstopmode '+texfile, shell=True)
        subprocess.call('pdflatex.exe -synctex=1 -interaction=nonstopmode '+texfile, shell=True)
    except:
        print("Error while generating the files !")

    # Put back the files where they were
    put_back_files(files)
    cleanup("./", texfile)
    
