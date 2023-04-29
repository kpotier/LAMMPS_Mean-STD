import numpy as np
import time
import os
import sys

outputSummaryLastHeader = []

def process(outputGlobal, outputSummary, output, path, sections, convergedLine):
    log = open(path, "r")

    header = []
    headerFound = False

    for headerLine, content in enumerate(log): # Find the header
        values = content.split()
        if len(values) != len(header) or len(values) == 0:
            header = values
        else:
            notValue = False
            for val in values:
                try:
                    float(val)
                except ValueError:
                    notValue = True
                    break
            if notValue == True:
                header = values
            else:
                headerLine -= 1
                headerFound = True
                break
    
    if headerFound == False:
        print("Could not find the header")
        return

    log.seek(0) # Reset position
    for valuesLine, content in enumerate(log): # How many lines
        if valuesLine <= headerLine:
            continue

        values = content.split()

        if len(values) != len(header):
            valuesLine -= 1
            break

        notValue = False
        for val in values:
            try:
                float(val)
            except ValueError:
                notValue = True
                break
        if notValue == True:
            valuesLine -= 1
            break

    if convergedLine > 0: # We count the converged line.
        convergedLine -= 1

    totalLines = valuesLine - headerLine - convergedLine
    linesPerSection = totalLines // sections

    printAwrite([output, outputGlobal], "Number of lines: " + str(totalLines))
    printAwrite([output, outputGlobal], "Number of lines per section: " + str(linesPerSection))

    assert(linesPerSection > 0), "Too many sections for this number of lines"

    log.seek(0) # Reset position
    
    results = list()
    for i in range(0, sections):
        results.append(list())
        for _ in range(0, len(header)):
            results[i].append(list())

    sectionsCurrent = 0
    for valuesConvergedLine, content in enumerate(log): # Append only converged lines
        if valuesConvergedLine > valuesLine:
            break

        line = valuesConvergedLine - headerLine - convergedLine
        if valuesConvergedLine <= headerLine or line <= 0:
            continue

        line = valuesConvergedLine - headerLine - convergedLine
        sys.stdout.write("\rProcessing line " + str(line) + "/" + str(totalLines) + " in section " + str(sectionsCurrent + 1))
        sys.stdout.flush()

        values = content.split()
        
        i = 0
        for val in values:
            results[sectionsCurrent][i].append(float(val))
            i += 1

        if line % linesPerSection == 0:
            sectionsCurrent += 1
            if sectionsCurrent >= sections:
                break
    
    sys.stdout.write("\n") # New line
    if line != totalLines:
        print("Could not process the last " + str(totalLines - line) + " line(s) (out of window)")

    printAwrite([output, outputGlobal], "Type " + " ".join(header))
    sectionsCurrent = 0
    resultsGlobal = list()
    for i in range(0, len(header)):
        resultsGlobal.append(list())

    for arr in results:
        i = 0
        string = ""
        for val in arr:
            resultsGlobal[i].append(np.mean(val))
            string += formatTable(resultsGlobal[i][-1])
            i += 1
        printAwrite([output, outputGlobal], "{:8d}".format(sectionsCurrent + 1) + string)
        sectionsCurrent += 1

    stringMean = ""
    stringSTD = ""
    for arr in resultsGlobal:
        stringMean += formatTable(np.mean(arr))
        stringSTD += formatTable(np.std(arr))
    
    printAwrite([output, outputGlobal], " "*4 + "Mean" + stringMean)
    printAwrite([output, outputGlobal], " "*5 + "Std" + stringSTD)

    global outputSummaryLastHeader
    if outputSummaryLastHeader != header:
        outputSummaryLastHeader = header
        outputSummary.write("Path " + " ".join(header) + " " + "-STD ".join(header) + "-STD\n")
    outputSummary.write(os.path.relpath(path) + stringMean + stringSTD + "\n")

# formatTable formats and beautify a number that is meant to be written in a file.
def formatTable(number):
    return " "*4 + ("%f" % number).rstrip("0").rstrip(".")

# printAwrite prints and writes a text into some files.
def printAwrite(files, text):
    print(text)
    for file in files:
        file.write(text + "\n")

# beforeProcess prints some text before and after the calculations.
def beforeProcess(output, outputSummary, outputDir, dir, sections, line):
    printAwrite([output], "BEGIN "+ dir + "/log.lammps:")
    process(output, outputSummary, outputDir, dir + "/log.lammps", sections, line)
    printAwrite([output], "END "+ dir + "/log.lammps")

def main():
    timeNow = str(int(time.time())) # fix time
    output = open("./meanstd_results_" + timeNow, "w+")
    outputSummary = open("./meanstd_results_summary_" + timeNow, "w+")
    length = len(sys.argv[1:])
    if length < 2 or length % 3 != 0 and length > 2:
        print("Not enough arguments")
        print("First argument: number of sections (int)")
        print("Second argument: line where the converged part starts (do not count the lines before the beginning of the table)")
        print("Optional: Third argument: path of the file")
        print("Optional: Repeat from the first arg to add multiple files")
        return
    
    if length == 2:
        for dirPath, _ , files in os.walk(os.path.abspath(os.curdir)):
            for file in files:
                if file == "log.lammps":
                    beforeProcess(output, outputSummary, open(dirPath + "/meanstd_" + timeNow, "w+"), dirPath, int(sys.argv[1]), int(sys.argv[2]))
                    break
    else:
        for k, arg in enumerate(sys.argv[1:]):
            if k % 3 != 0: # Not a multiple of 3
                continue
            beforeProcess(output, outputSummary, open(sys.argv[k+3] + "/meanstd_" + timeNow, "w+"), sys.argv[k+3], int(arg), int(sys.argv[k+2]))
main()
