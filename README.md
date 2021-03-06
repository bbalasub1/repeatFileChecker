### DESCRIPTION:

Cross-platform code to scan through an archive of documents (photos, codes, documents, etc.) and remove duplicates if any. 

This code traverses through a directory and its subdirectories, identifies repeat files by matching their MD5 checksums and deletes the repeats after prompting the user. 

Files can be filtered based on file name extensions. If filtering is used, only files belonging to an input list of extensions are checked for repeats.

As always, use with prudence as the deleted files cannot be recovered  later in some OS!

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
