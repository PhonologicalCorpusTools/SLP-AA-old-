.. _start_new_corpus:

***************
Starting a new corpus
***************

.. _transcribe_sign:

Transcribing a sign
------------------

.. _enter_gloss:

1. Entering a Gloss
`````````````````
To enter a gloss for a sign, simply click on the text box named "Gloss" and type in. This box is case-sensitive.

.. _fill_slot:

2. Filling in a slot
`````````````````
To fill in a slot, you can either click on a slot to select a symbol from the pull-down menu or type in 
a symbol yourself. For more infomation about slots and symbols, see :ref:`field_and_slot`

      Notes on typing in a symbol
      
      * Slots are generally case-insensitive. An exeption is Slot 11, which permits both "m" and "M".
      
      * In Slots 20, 25, and 30, use the key 'z' for "x-"; 'c' for "x+"; and 's' for "☒".
      
      * For Mac users, it may be helpful to use the Tab key to move to the next slot. To enable this, go to System Preferences > Keyboard > Shortcuts. At the bottom of the page under Full Keyboard Access, select "All controls."

.. _flag_slot:

3. Flagging a slot
`````````````````
You can optionally flag individual slots. "Flag as uncertain" will colour the slot, and 
"Flag as estimate" will mark the slot with a dotted line. 

To do this, control-click or rightclick a slot. A pull-down menu will appear, and you can select or unselect these options:

.. image:: static/flag.png
   :width: 90%
   :align: center

Alternatively, go to Transcription in the menu bar and select "Set transcription flags...". A new window will appear. You can expand and scroll through the window to flag any slot in any Config. Click OK.

.. image:: static/set_flag.png
   :width: 90%
   :align: center

"Flag as estimate" is intended to note that, because of obscurity, a symbol has been estimated in some way (based on
knowledge of hand anatomy, a preceeding hand configuration, the other hand in a two-handed symmetrical sign, etc.).
"Flag as uncertain" is intended to stand for the transcriber's subjective uncertainty about their choice of a sylbol.
Therefore, it is certainly possible to use these two options simultaneously when the transcriber is uncertain about their
estimation.

.. image:: static/use_both.png
   :width: 90%
   :align: center


.. _copy_and_paste:

4. Copying and Pasting
`````````````````
Using the Copy and Paste buttons at the top right corner, you can copy your transcription for one Config and paste it to to another Config within the same sign.

To copy your transcription, click on the Copy button at the top right corner. A new window "Copy transcription" will appear. Select a Config that you would like to copy, and click OK.

Similarly, to paste the transcription, click on the Past button at the top right corner. A new window "Paste transcription" will appear. Make sure that the intended trasnscription has been copied, and select a Config to which you would like to paste that transcription. Click OK. Note that any existing symbols in the Config will be overwritten.

   For example, let's say you would like to copy your transcription for Config 1 of Hand 1 and paste it to Config 1 of Hand 2.
   
   First, click on the Copy button. In the new window, select Config 1, Hand 1, and click OK.
   
   .. image:: static/copy.png
      :width: 90%
      :align: center

  
   Second, click on the Paste button. In the new window, you can see the copied transcription in the first line introduced by    "The currently copied transcription is". Make sure it is the correct one. Then select Config 1, Hand 2, and click OK.
      
   .. image:: static/paste.png
      :width: 90%
      :align: center
   
   This feature may be particularly useful for transcribing symmetrical signs.
   
   .. image:: static/paste_result.png
      :width: 90%
      :align: center
      

.. _check_global_handshape:

5. Checking Global handshape options
`````````````````
Global handshape options (see :ref:`global_handshape_options`) can be checked by simply cliking the box next to a description.
The options "This sign is partially obscured" and "The coding for this sign is uncertain" can be thought of as a global
counterpart of the slot options "Flag as estimate" and "Flag as uncertain," respectively (see :ref:`flag_slot`).
In other words, it may be useful, for example, to check these Global handshape options when estimation or uncertainty applies
to a whole sign or a whole finger(s) rather than individual slots.


.. _other_parameters:

6. Transcribing other parameters
`````````````````
To transcribe parameters other than handshapes, click on "View Parameters button at the top right corner. A new window will
appear, and you can select relevant values.

.. image:: static/.png
      :width: 90%
      :align: center

If you would like to have the parameters window open while transcribing handshapes, go to Options in the menu bar and select
"Keep parameters window on top."

.. _add_sign_notes:

7. Adding Sign and Corpus notes
`````````````````
To add a note to a sign that you are transcribing, go to Notes in the menu bar and click on "Edit sign notes..." A new window
will appear, and you can type in your comments. 

.. image:: static/sign_notes.png
      :width: 90%
      :align: center
        
Sign notes are automatically saved when the signs are saved, and you can go back and edit them by following the above step.
It may be useful, for example, to use this sign notes to describe reasons for checking the Global handshape options.    

Similarly, Notes>"Edit corpus notes..." will allow you to add a note to the entire corpus.


.. _check_transcription:

8. Checking transcription
`````````````````
To check your transcription against your selected constraints (see :ref:`constraints`), click on "check transcription" button.
