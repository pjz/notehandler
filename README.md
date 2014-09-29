
NoteHandler - Commandline Evernote
==================================

An Evernote CLI in python.  

State (including your dev key) is stored in the file pointed at
by the NHRC environment variable, or ~/.nhrc if no value is set.

'nh' is the command:

`nh add [[:<tag1>] [:\<tag2>] ...]
       [+<notebook>] 
       <title> 
       [resource1] [resource2] ..
       < <content>`
    - add a new note 
       with the specified tags (or none if unspecified)
       in the specified notebook (or your current notebook if unspecified)
       with the specified title (required)
       adding the specified files as resources to that note (or none if unspecified)
       and content from stdin
       
`nh login` - Log in to Evernote; you'll be prompted for username and password

`nh logout` - Nuke your persistent Evernote credentials.

`nh notebook [+<notebook>]` - if notebook is specified, set the current notebook,
    creating it if necessary. Otherwise, just show the current notebook.

`nh notebooks` - List existing notebooks.
    The (evernote) default notebook is marked with a 'D'.
    The (local-only) current notebook is marked with a '+'

`nh notes [+notebook] [:tag1 [:tag2] ...] [--offset=X] [--count=Y]` -
    list notes in the specified notebook, or the current one if not specified.


