.. _predefined_handshapes:

***************
Predefined Handshapes
***************

1. Selecting a predefined handshape
`````````````````
To select a predefined handshape click on the hand icon on the top left menu bar. A new window will open. The predefined handshapes are organized vertically by
base handshape and horizontally by modification type. For example, if you are searching for 'clawed-F', you can find the 'F' row and the 'clawed' column.

The configuration and hand you are selecting the handshape for can be changed on the top bar. For example, if you want to select a predefined handshape for
Configuration 1 of Hand 2, select the option 'Config1 Hand2'.

Once you have selected a predefined handshape, the slots will be filled in for the appropriate configuration and hand on the 'handshape transcription' window of the SLPAA. The name of the selected handshape will appear to the right of the slots. To clear this selection, click on the 'clear' button to the right of the predefined handshape name. To change the selection, you can simply select another predefined handshape to replace it (while the configuration you are trying to change is still selected).


.. _fill_slot:

2. Making specific changes
`````````````````
Once a predefined handshape has been selected, you can change individual slots of the predefined handshape transcription. Once changes are made, the name of the predefined handshape will no longer appear to the right of the transcription. 
(For more detailed axplanation of the transcription process, see 'transcription_process.rtf'?)


.. _flag_slot:

3. Searches for handshapes
`````````````````
TO DO: include info about components that can be ignored in searches


.. _copy_and_paste:

4. Copying and Pasting
`````````````````
Using the Copy and Paste functions, you can copy your transcription for one Config and paste it to to 
another Config within the same sign.

To copy your transcription, click on the "Copy" button at the top right corner or go to "Edit" in the menu bar and 
select "Copy a transcription...". A new window "Copy transcription" will appear. Select a Config that you would like to copy, 
and click "OK".

Similarly, to paste the transcription, click on the "Paste" button at the top right corner or go to "Edit" in the menu bar and 
select "Paste a transcription...". A new window "Paste transcription" will appear. Make sure that the intended trasnscription 
has been copied, and select a Config to which you would like to paste that transcription. If you would like to paste 
only the symbols and not the flags, then uncheck the option "Paste in highlighting for uncertain and estimated slots". 
Click "OK". 
Note that any existing symbols in the Config will be overwritten.

   For example, let's say you would like to copy your transcription for Config 1 of Hand 1 and paste it to Config 1 of Hand 2.
   
   
   First, click on the Copy button. In the new window, select Config 1, Hand 1, and click OK.
   
   .. image:: static/copy.png
      :width: 90%
      :align: center

  
   Second, click on the Paste button. In the new window, you can see the copied transcription in the first line, 
   introduced by    "The currently copied transcription is". Make sure that it is the correct one. 
   Then select "Config 1, Hand 2", and click "OK".
      
   .. image:: static/paste.png
      :width: 90%
      :align: center
   
   
   This function may be particularly useful for transcribing symmetrical signs or assymmetrical signs in which
   only the dominant hand changes its handshape.
   
   .. image:: static/paste_result.png
      :width: 90%
      :align: center
      

.. _check_global_handshape:

5. Checking Global handshape options
`````````````````
Global handshape options (see :ref:`global_handshape_options`) can be checked by simply cliking the box next to a description.
The options "Estimated" and "Uncertain" can be thought of as a global counterpart of the slot options "Flag as estimate" 
and "Flag as uncertain," respectively (see :ref:`flag_slot`).
In other words, it may be useful, for example, to check these Global handshape options when estimation or uncertainty applies
to a whole sign or a whole field(s) rather than individual slots.


.. _other_parameters:

6. Transcribing other parameters
`````````````````
To transcribe parameters other than handshapes, click on "View Parameters" button at the top right corner. A new window will
appear, and you can select relevant values. To transcribe handshapes and parameters at the same time, see :ref:`options`.

.. image:: static/.png
      :width: 90%
      :align: center


.. _add_sign_notes:

7. Adding Sign and Corpus notes
`````````````````
To add a note to a sign that you are transcribing, go to "Notes" in the menu bar and click on "Edit sign notes..." A new 
window will appear, and you can type in your comments. 

.. image:: static/sign_notes.png
      :width: 90%
      :align: center
        
Sign notes are automatically saved when the signs are saved, and you can go back and edit them by following the above step.
It may be useful, for example, to use this sign notes to describe reasons for checking the Global handshape options.    

Similarly, "Notes" > "Edit corpus notes..." will allow you to add a note to the entire corpus.


.. _check_transcription:

8. Checking transcription
`````````````````
To check your transcription against your selected constraints (see :ref:`constraints`), click on "Check transcription" button.


.. _visualize_transcription:

9. Visualizing transcription
`````````````````
To see a graphic image of transcribed handshapes, click on "Visualize transcription" button. A new window titled 
"Handshape visualization" appears. Select a combination of Config and Hand you would like to visualize, and click "OK".

.. image:: static/visualization.png
      :width: 90%
      :align: center


.. _save_sign:

10. Saving a sign to a corpus
`````````````````
Note that each sign should be saved before a next sign can be transcribed. To save a sign, either click on "Save word to
corpus" button or go to "File" in the menu bar and select "Save current word". You will get a message 
"Corpus successfully updated!" if "Show save alert" is selected in your setting (see :ref:`options`).


If you do not have a corpus loaded beforehand, you will get a warning message: "You must have a corpus loaded before you can
save words. What woule you like to do?". You can either "Create a new corpus" or "Add this word to an existing corpus".

.. image:: static/corpus_warning.png
      :width: 90%
      :align: center


If you have a sign with the same gloss already saved in the same corpus and "Warn about duplicate glosses" is selected in your
setting (see :ref:`options`), you will get a warning message: "A word with the gloss XXX already exists in your corpus. What do you want to do?".
You can either "Go back and edit the gloss" or "Overwrite existing word".

.. image:: static/duplicate_warning.png
      :width: 90%
      :align: center


Finally, if you click on "New gloss" (see :ref:`next_sign`) without saving the current sign, you will get a warning message: 
"The current gloss has unsaved changes. what would you like to do?" It gives you options to either "Go back" to the current 
sign or to "Continue without saving". 
If this is the first time the sign is transcribed in the corpus, the latter option will delete a sign.


.. _next_sign:

11. Transcribing the next sign
`````````````````
Once a sign has been saved, if you would like to continue on transcribing a next sign, you can either click on 
the "New gloss" button or go to "File" and select "New gloss".

You can repeat the transcribing process from :ref:`enter_gloss`.
