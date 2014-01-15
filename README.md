
ClEvernote - Commandline Evernote
=================================

An Evernote CLI in python.

'cn' is the command:

cn login/logout - acquire and destroy oauth tokens

cn add [[:<tag1>] [:<tag2>] ...]
       [+<notebook>] 
       <title> 
       [resource1] [resource2] ..
       < <content>
    add a new note 
       with the specified tags (or none if unspecified)
       in the specified notebook (or your current notebook if unspecified)
       with the specified title (required)
       adding the specified files as resources to that note (or none if unspecified)
        
       
cn notebooks - list existing notebooks. 
                 Your default notebook is marked with a 'D'.
                 Your (clevernote-only) current notebook is marked with a '+'

cn notebook [+<notebook>] - if notebook is specified, set the current notebook,
                               creating it if necessary. Otherwise, just show
                               the current notebook.

