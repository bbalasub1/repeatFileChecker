#%%

"""
Function to delete repeated files that occur below a root directory. It is 
written to be cross-platform. Please notify author if you encounter an error 
on your OS (see caveats below before emailing).

This code traverses through a directory and its subdirectories, identifies 
repeat files by matching their MD5 checksums and deletes the repeats after
prompting the user. 

As always, use with prudence as the deleted files cannot be recovered 
later in some OS!

One typical use is for removing duplicate photos from your archive. It can also
be used for deleting repeated archival files etc.

INPUT:
    rootDir : full directory to start the scan (use unix forward slash format)
               <string>

OUTPUT:
    tuple of (result_df, summary_df, resultFlag)
    
    result_df  : complete scan results of all files <pandas dataframe>
    summary_df : scanned results agg by checksum <pandas dataframe>
    resultFlag : 1 if all delete operations were completed, 0 if no deletes 
                  were requested, -1 if deletes were done partially
                  if -1 is returned, some of the deletes were not done <int>

CAVEATS:
    If you select to delete the files at the prompt, make sure the files
    are not read-only. Otherwise, the code throws an exception and exists.
    The catch-try has been omitted by design as attempting to delete
    read-only files is a serious problem and the user needs to reconsider.
    

@author: Balakumar B J, 2018
"""

import os
import hashlib
import pandas

def repeatFileChecker(rootDir = 'C:/Users/xyz/Desktop/MainPhotoFolder/'):
        
    #############################################################
    # set parameters
    #############################################################
    rootDir = os.path.abspath(rootDir)  # make it os-independent
    
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
    # crawl through directory and compute checksums for all files
    #############################################################        
    # first do a quick crawl to compute total number of files        
    n = 1
    for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                n = n + 1    
    # now do the checksum crawl            
    i = 1    
    mList = []
    fList = []
    for dirName, subdirList, fileList in os.walk(rootDir):    
        #print('Found directory: %s' % dirName)
        for fname in fileList:
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
    print("")
    print("**************************************")
    print("WARNING! %d repeated files ready for delete" % (len(pd) - sum(pd.keep)))
    checkDelete = input("Delete all repeat files [Y/N]?")
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
    
    
    # return
    return (pd, q, resultFlag)

