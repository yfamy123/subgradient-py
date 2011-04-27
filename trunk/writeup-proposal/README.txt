these are some simple examples that you can use for your project.

the directories matlab/ and figures/ contain ALL source required
to build the document.  the matlab files generate the .eps files that are
included in the latex document.

to compile pdf files (say) on any reasonable (ie, unix like or based)
operating system, the commands are

% latex stoch_subgrad_notes.tex
% dvipdf stoch_subgrad_notes.dvi

(for the notes)

to include the bibliography, you need to run

% bibtex stoch_subgrad_notes

and then latex a few times so the references get caught up.  then dvips 
(to create ps) and ps2pdf14 (to create pdf).
