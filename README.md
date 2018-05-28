TYPICAL USES: Delete repeated/replicate photos, remove multiple archives, 
remove copies of log files, streamline document archives and document stores

DESCRIPTION:

Function to delete repeated files that occur below a root directory. It is 
written to be cross-platform. Please notify author if you encounter an error 
on your OS (see caveats below before emailing).

This code traverses through a directory and its subdirectories, identifies 
repeat files by matching their MD5 checksums and deletes the repeats after
prompting the user. 

As always, use with prudence as the deleted files cannot be recovered 
later in some OS!

One typical use is for removing duplicate photos from your archive. 

USAGE:

    result_df, summary_df, resultFlag = repeatFileChecker('../MainPhotoDirectory/')

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

TESTING:

    Use the photos in the phototest directory for testing this function.

CAVEATS:

    If you select to delete the files at the prompt, make sure the files
    are not read-only. Otherwise, the code throws an exception and exists.
    The catch-try has been omitted by design as attempting to delete
    read-only files is a serious problem and the user needs to reconsider.
    

@author: Balakumar B J, 2018