User manual
***********

Choose video and subtitles
==========================

Before the training you should choose an educational material. It may be some
movie, or clip, or TV show, but there are two conditions for the selection of
the material:

* It has to be in the language you're learning. It may be the localization of the chosen movie for a foreign country if the original movie in your native language.
* You should find the correct subtitles in the same language. The quality of the training is highly dependent on the accuracy of the chosen subtitles.

When you'll have the video and subtitles, you can open them by pressing Ctrl+O
for the video and Ctrl+S for the subtitles or by selecting an appropriate item
in menu "File".

"Preview" mode
==============

This mode may be used to check the accuracy of the subtitles and to set a value
of the subtitles shift if it's not synchronized with the video. This value is
specified in milliseconds and is used in both modes. It may be negative.
Important to set the shift value as accurate as possible, because it influences
the calculation of boundaries of video segments.

In this mode you should to set a volume level in order to not be distracted to 
it during trainging. The volume level should be sufficient so that you could
hear every word, but not too high, because high loudness will tire your sense
of hearing quickly.

Next, you can select a location from which you wish to start the training and
change the mode to "Learning".

"Learning" mode
===============

This mode is used for the training.
Watching the movie, you should listen to speech in the foreign language and
type everything you hear. If you don't have time to type a phrase during
the playback, the application will pause the video and will continue to play
as soon as you will have typed the last word of the phrase. Steno checks
the correctness after the typing of each letter, it uses the subtitles
to assess. Errors are highlighted immediately after detection.

You can repeat the last segment of the video as many times as necessary. To do
this, use the hotkey Ctrl+R or the "Repeat" button. If you can't recognize one
or more words, you can use the hint by pressing Ctrl+H or by clicking
the "Hint" button. In this case, next word will be appended at once.

Steno translates an every typed word and whole phrase using Google Translate.

You can interrupt a lesson at any moment by pressing the "Stop" button or
by changing the mode of the application.

Settings
========

You can use the "Preferences" dialog to configure the application. It may be
opened by pressing Ctrl+P or by selecting of an appropriate item in menu
"Edit". This dialog allows to edit the following settings:

* Disable the translation, if you don't want to use it.
* Choose a foreign language which is a language of your educational material.
* Choose your native language which is a target language for the translation.
* Choose colors and fonts of the application window.
* Choose colors of the highlighting.
* Add, update, or remove filters for the subtitles content.

Filters for the subtitles
=========================

Sometimes the subtitles text contains different comments, except speech of
characters. For example, notes about an intonation or noise, designations on
who is speaking, etc. These comments have characteristic signs such as square
brackets or uppercase.

Steno uses filters in order to remove the extra information from the subtitles.
The application has the default collection of filters which is works in most
cases, but you can add your own filters using the "Preferences" dialog.

Every filter contains two values:

* Regular expression pattern that is used to spot an undesired text.
* Replacement data that are usually whitespace or empty.