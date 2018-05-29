DESCRIPTION:

Cross-platform function to delete repeated files that occur below a given directory. 

This code traverses through a directory and its subdirectories, identifies 
repeat files by matching their MD5 checksums and deletes the repeats after
prompting the user. 

Files can be filtered based on file name extensions. If this is used,
only files belonging to an input list of extensions are checked for repeats.

As always, use with prudence as the deleted files cannot be recovered 
later in some OS!

One typical use is for removing duplicate photos from your archive. 

TYPICAL USE-CASES: 

Delete repeated/replicate photos, remove multiple backup archives, 
remove reduntant copies of log files, streamline document archives/document stores,
remove multiple pdf's from reference management software, code management, bookmark management.

USAGE:

    result_df, summary_df, resultFlag = repeatFileChecker('../MainPhotoDirectory/')

INPUT:

    rootDir : full directory to start the scan (use unix forward slash format)
               <string>
               
    extList : Provide a list of string extensions for filtering files to process.
                use ["*.*"] to look for all files (default). See examples below.
                
    caseIndependentMatch: <boolean> When set to True, file extension filtering
               is done independently. Default is False.

OUTPUT:

    tuple of (result_df, summary_df, resultFlag)
    
    result_df  : complete scan results of all files <pandas dataframe>
    
    summary_df : scanned results agg by checksum <pandas dataframe>
    
    resultFlag : 1 if all delete operations were completed, 0 if no deletes 
                  were requested, -1 if deletes were done partially
                  if -1 is returned, some of the deletes were not done <int>

EXAMPLES:
    import repeatFileChecker as rf
    
    # search for repeats without filtering on file extensions
    rf.repeatFileChecker('./testimages', extList = ["*.*"], caseIndependentMatch=True)
    
    # search for repeats only on .jpg files. case independent extension filtering
    #  is performned. I.e. .jpg, .JPG, .JpG etc files are all searched. 
    rf.repeatFileChecker('./testimages', extList = [".jpg"], caseIndependentMatch=True)

    # search for repeats only on .jpg files. case dependent search is performed
    #  i.e. only .jpg files are searched. .JPG files are ignored 
    rf.repeatFileChecker('./testimages', extList = [".jpg"], caseIndependentMatch=False)
    
TESTING:

    Use the photos in the testimages directory for testing this function.

CAVEATS:

    If you select to delete the files at the prompt, make sure the files
    are not read-only. Otherwise, the code throws an exception and exists.
    The catch-try has been omitted by design as attempting to delete
    read-only files is a serious problem and the user needs to reconsider.
    
Please notify author if you encounter an error on your OS (see caveats above before emailing).

@author: Balakumar B J, 2018