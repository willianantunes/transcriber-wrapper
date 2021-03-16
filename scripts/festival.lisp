; This is not LISP literally, but actually Festival's Scheme Programming Language!
; Know more about it looking at: http://www.festvox.org/bsv/c3927.html
;; First we create a variable which will store the value of env variable WORD
(set! word_to_be_transcribed (getenv "WORD"))
;; Now we create an utterance object
;; http://www.festvox.org/docs/manual-1.4.2/festival_14.html#SEC51
(set! utterance (eval (list 'Utterance 'Text word_to_be_transcribed)))
;; http://www.festvox.org/docs/manual-1.4.2/festival_34.html#SEC143
;; The main synthesis function. 
;; Given UTT it will apply the functions specified for UTT's type, as defined with deffUttType and then those demanded by the voice. 
;; After modules have been applied synth_hooks are applied to allow extra manipulation.
(utt.synth utterance)
;; http://www.festvox.org/docs/manual-1.4.2/festival_14.html#SEC53
;; A Lisp tree presentation of the items RELATIONNAME in UTT. The Lisp bracketing reflects the tree structure in the relation.
;; We use the relation SylStructure, which is a list of trees. This links the Word, Syllable and Segment relations. Each Word is the root of a tree whose immediate daughters are its syllables and their daughters in turn as its segments.
;; Know more relations here: http://www.festvox.org/docs/manual-1.4.2/festival_14.html#SEC49
(print (utt.relation_tree utterance "SylStructure"))
