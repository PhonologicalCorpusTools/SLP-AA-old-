# SLP-Annotator

One of the barriers to conducting corpus-based phonetic and phonological research on signed languages is the lack of tools for 
streamlining phonetic annotation in a way that is then compatible with other corpus-analysis resources. SLP-Annotator is a free, open-
source software program that is designed to implement a (slightly modified) version of Johnson 
and Liddell’s anatomically based and phonetically detailed Sign Language Phonetic Annotation (SLPA) system (2010, 2011a, 2011b, 2012).
The software creates corpora that are compatible with the more general program Phonological CorpusTools (PCT; Hall et al. 2016) to 
allow relatively automated phonological analysis. 
  
SLPAnnotator follows the guidelines laid out in Tkachman et al. (2016) to modify SLPA. Specifically, each handshape annotation 
consists of exactly 34 slots, each of which can consist of a pre-determined list of annotations (see Fig. 1). Completely standardizing 
the input format of each transcription makes it possible to (a) facilitate the transcription process by providing the transcriber with 
both visual and written information about what can be entered into each slot; (b) provide automatic checks for inaccurate 
transcriptions (e.g., warning users when they enter anatomically or phonologically implausible configurations); (c) create automatically
rendered images of the transcribed handshape, facilitating readability and human-led accuracy checks; and (d) create 
corpora that are compatible with automated analysis. For example, after creating corpora using SLPAnnotator, one could import them into
PCT to test claims about sign language phonology and typology, such as the proposal in Johnson and Liddell (2011b: 21) that when the 
proximal joints are all extended, the fourth finger is always abducted. This can be done by searching for certain finger configurations
in a corpus, in a manner similar to how PCT allows searching for words with segments matching specific phonological features. PCT will
also makes it easy to run a variety of common analyses that have rarely, or never, been used with sign languages, such as calculations
of functional load or neighbourhood density.

[ _ ]1 [ _ _ _ _ ]2 [ _ _ ∅ / _ _ _ _ _ _ ]3 [1_ _ _ ]4 [ _ 2 _ _ _ ]5 [ _ 3 _ _ _ ]6 [ _ 4 _ _ _ ]7

Figure 1. The template for SLPA handshape annotation in SLPAnnotator: (1) forearm, (2) thumb configuration, (3) thumb-finger contact, (4) index finger, (5) middle finger, (6) ring finger, (7) little finger.

References:

Caselli, N., Sevcikova, Z., Cohen-Goldberg, A., Emmorey, K. (2016). ASL-Lex: A lexical database for ASL. Behavior Research Methods. doi:10.3758/s13428-016-0742-0.

Hall, Kathleen Currie, Blake Allen, Michael Fry, Scott Mackie, and Michael McAuliffe. (2016). Phonological CorpusTools, Version 1.2. [Computer program]. Available from https://github.com/PhonologicalCorpusTools/CorpusTools/releases.

Johnson, Robert E. & Scott K. Liddell. 2010. Toward a phonetic representation of signs: Sequentiality and contrast. Sign Language Studies 11.241-74.

Johnson, Robert E. & Scott K. Liddell. 2011a. A segmental framework for representing signs phonetically. Sign Language Studies 11.408-63.

Johnson, Robert E. & Scott K. Liddell. 2011b. Toward a Phonetic Representation of Hand Configuration: The fingers. Sign Language Studies 12.5-45.

Johnson, Robert E. & Scott K. Liddell. 2012. Toward a Phonetic Representation of Hand Configuration: The thumb. Sign Language Studies 12.316-33.

Tkachman, Oksana, Kathleen Currie Hall, André Xavier & Bryan Gick. 2016. Sign Language Phonetic Annotation meets Phonological CorpusTools: Towards a sign language toolset for phonetic notation and phonological analysis. Proceedings of the Annual Meeting of Phonology.
