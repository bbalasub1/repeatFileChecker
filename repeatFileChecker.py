"""
### DESCRIPTION:

Cross-platform function to delete repeated files that occur below a given directory. 

This code traverses through a directory and its subdirectories, identifies 
repeat files by matching their MD5 checksums and deletes the repeats after
prompting the user. 

Files can be filtered based on file name extensions. If filtering is used,
only files belonging to an input list of extensions are checked for repeats.

As always, use with prudence as the deleted files cannot be recovered 
later in some OS!

One typical use is for removing duplicate photos from your archive. 

### TYPICAL USE-CASES: 

Delete repeated/replicate photos

Remove multiple backup archives

Remove reduntant copies of log files

Streamline document archives

Manage code bases

### INPUT:

    rootDir : full directory to start the scan (use unix forward slash format)
               <string>
               
    extList : Provide a list of string extensions for filtering files to process.
                use ["*.*"] to look for all files (default). See examples below.
                
    caseIndependentMatch: <boolean> When set to True, file extension filtering
               is done independently. Default is False.

### OUTPUT:

    tuple of (result_df, summary_df, resultFlag)
    
    result_df  : complete scan results of all files <pandas dataframe>
    
    summary_df : scanned results agg by checksum <pandas dataframe>
    
    resultFlag : 1 if all delete operations were completed, 0 if no deletes 
                  were requested, -1 if deletes were done partially
                  if -1 is returned, some of the deletes were not done <int>

### USAGE:

    import repeatFileChecker as rf
    
    # search for repeats without filtering on file extensions
    result_df, summary_df, resultFlag = rf.repeatFileChecker('./testimages', extList = ["*.*"], caseIndependentMatch=True)
    
    # search for repeats only on .jpg files. case independent extension filtering
    #  is performned. I.e. .jpg, .JPG, .JpG etc files are all searched. 
    result_df, summary_df, resultFlag = rf.repeatFileChecker('./testimages', extList = [".jpg"], caseIndependentMatch=True)

    # search for repeats only on .jpg files. case dependent search is performed
    #  i.e. only .jpg files are searched. .JPG files are ignored 
    result_df, summary_df, resultFlag = rf.repeatFileChecker('./testimages', extList = [".jpg"], caseIndependentMatch=False)
    
### TESTING:

    Use the photos in the testimages directory for testing this function.

### CAVEATS:

    If you select to delete the files at the prompt, make sure the files
    are not read-only. Otherwise, the code throws an exception and exits.
    The catch-try has been omitted by design.
    
Please notify author if you encounter an error on your OS (see caveats above before emailing).

@author: Balakumar B J, 2018
"""

import os
import hashlib
import pandas

def repeatFileChecker(rootDir = 'C:/Users/xyz/Desktop/MainPhotoFolder/', \
                      extList = [".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".img", ".png"], \
                      caseIndependentMatch = False):
        
    #############################################################
    # set parameters
    #############################################################
    rootDir = os.path.abspath(rootDir)  # make it os-independent

    if not isinstance(extList, (list,)):
        raise TypeError("extList must be a list. See documentation.")

    # convert input extList to lower if caseIndependentMatch is turned on
    if caseIndependentMatch:   
        extList = [x.lower() for x in extList]
    extList = tuple(extList)  # extList must be a tuple for comparison    
    
    print('Searching for files with the following extensions:')
    print(extList)
    print('\n')
    
    #############################################################
    # checksum function 
    #############################################################
    def md5Checksum(filePath):
        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
 
    #############################################################
    # check if filename contains the extension in the extList
    #############################################################       
    def checkFileExtension(fname, extList):
        processFile = False
        if extList == tuple(["*.*"]):
            processFile = True
        else:
            if caseIndependentMatch:
                if fname.lower().endswith(extList):
                    processFile = True
            else:
                if fname.endswith(extList):
                    processFile = True
        return(processFile)

    
    #############################################################
    # crawl through directory and compute checksums for all files
    #############################################################        
    # first do a quick crawl to compute total number of files with matching extensions
    n = 0
    for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                # check if file has the extensions specified in the input
                if checkFileExtension(fname, extList):
                    n = n + 1    
                    
    # now do the checksum crawl            
    i = 0   
    mList = []
    fList = []
    for dirName, subdirList, fileList in os.walk(rootDir):    
        #print('Found directory: %s' % dirName)
        for fname in fileList:
            # if file has matching extensions, checksum it and compare
            if checkFileExtension(fname, extList):
                fullFileName = os.path.join(dirName, fname)
                #print('\t%s' % fullFileName)
                mdc = md5Checksum(fullFileName)
                #print('\t%s' % mdc)
                i = i + 1
                mList.append(mdc)
                fList.append(fullFileName)
                print('completed %d of %d files' % (i, n))
        
    #############################################################
    # figure out which files are repeat files
    #############################################################
    # create a pandas dataframe of chksum and filenames    
    pd = pandas.DataFrame({'fname':fList, 'chksum':mList})        
    
    # filter to keep only unique images based on chksum
    pdunq = pd.drop_duplicates(subset = 'chksum').copy()
    pdunq['keep'] = 1
    # do a left join and add a keep column that specifies whether the images
    # are repeats or not   
    pd = pd.merge(pdunq, how = 'left', on = ['chksum', 'fname'])
    pd.keep = pd.keep.fillna(0)
    pd = pd.sort_values(['chksum']).reset_index(drop = True)
    
    #############################################################
    # display info on repeat files
    #############################################################
    q = pd.groupby(['chksum'], as_index = False).agg(['count']).reset_index()
    q.columns = q.columns.droplevel(1)
    print('Found %d repeat files (out of %d)' % (len(pd) - sum(pd.keep), len(pd)))
    print("")
    print('Printing table with counts of repeated files:')
    print(q)
    
    #############################################################
    # delete repeated files from drive
    #############################################################
    resultFlag = 0
    if (len(pd) - sum(pd.keep) > 0):    
        print("")
        print("**************************************")
        print("WARNING! %d repeated files ready for delete" % (len(pd) - sum(pd.keep)))
        checkDelete = input("Delete all repeat files [Y/N]? ")
        if (checkDelete == "Y"):
            print("**************************************")
            print(" WARNING! You are about to permanently delete files from your drive")
            print(" WARNING!  Make sure you have backups")
            print(" WARNING!  This operation cannot be reversed")
            finalCheckDelete = input("Are you sure you want to delete all repeat files [Yes/No]? ")
            if (finalCheckDelete == "Yes"):
                resultFlag = -1
                for i in range(0, len(pd)):
                    if (pd.keep[i] == 0.0):
                        print('deleting %s (chksum = %s)' % (pd.fname[i], pd.chksum[i]))
                        os.remove(pd.fname[i])
                resultFlag = 1
            else:
                print("Not deleting repeat files. Exiting program.")        
        else:
            print("Not deleting repeat files. Exiting program.")
    else:
        print("No repeat files found for delete. Exiting program.")
    
    
    # return
    return (pd, q, resultFlag)

