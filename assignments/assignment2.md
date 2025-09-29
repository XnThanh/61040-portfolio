# Assignment 2: Functional Design

## Problem Statement

### Problem Domain

**Learning Mandarin**  
I am very intrigued by foreign languages and have studied Mandarin for around 6 years, with multiple trips abroad to pursue advance language studies.

### Problem

Many Mandarin learners are taught using the Pinyin romanization system (official phonetic system used in China). However, other Mandarin-speaking countries, such as Taiwan, uses a different phonetic system (i.e. Zhuyin). Many Mandarin learners who started learning Mandarin outside of Taiwan, and later come to Taiwan to study, become interested in switching to Zhuyin system for typing Chinese characters. However, to be able to type at a reasonable speed in Zhuyin requires a lot of typing practice (similar to how we learned to type on QWERTY keyboard in adolecence), along with dictionary lookups to learn the correct Zhuyin input (because Pinyin to Zhuyin is not a 1-to-1 conversion).

### Stakeholders

- Taiwanese children: elementary and middle school-aged children in Taiwan who are learning to type.

- Foreign learners: Mandarin learners (foreigners or non-advanced heritage speakers) who want to learn Zhuyin for typing Chinese. They often have issues with remembering tones.

- Heritage learners: native or advanced heritage Chinese speakers who are learning Zhuyin, either because they grew up knowing another input system such as Pinyin, or never learned to write/type. They don't have problems with remembering tones.

- Teachers: teachers of the above three stakeholders

- Taiwanese: native Taiwanese or those of Taiwanese heritage

Taiwanese children, foreign learners, heritage learners all suffer from lack of Zhuyin typing practice. Teachers may have interest in providing resources that can help their students learn and practice in their own time. Taiwanese may have interest in spreading their culture and language as Zhuyin is used solely in Taiwan and by Taiwanese outside Taiwan; besides writing traditional characters, Zhuyin plays a role in Taiwanese pop culture, as many slangs, puns, and trends, along with some references to Taiwanese Hokkien (another language spoken in Taiwan) has a basis in Zhuyin.

### Evidence and Comparables

- [Learn Scripts Zhuyin](https://learn-scripts.github.io/zhuyin.html) Flashcard-style practice for recognizing what each Zhuyin symbols correspond to in Pinyin. Only relevant for learners who come from a Pinyin background. Useful for switching from Pinyin to Zhuyin, but does not help with actual Zhuyin typing.

- [JSZhuyin](https://jszhuyin.timdream.org/learn/) Introduction to typing Zhuyin on a qwerty keyboard. However, only teaches you to type the one phrase "Hello, world!".

- [What is Bopomofo Youtube Video](https://www.youtube.com/watch?v=AKH5IHhbUUA) Zhuyin usage explanation, mentions certain differences between Pinyin and Zhuyin conversion (because Pinyin to Zhuyin is not 1-to-1 conversion). Relevant for complete beginners (non-Taiwanese).

- [Zhuyin Practice App](https://play.google.com/store/apps/details?id=com.turtle8.banana01&hl=en_US) ([demo link](https://youtu.be/t4rZHKVTZpg)) Practice typing Zhuyin for different words. However, no long form typing (i.e. sentences), only single words. Has a couple other functionalities like audio pronounciation and Chinese character to Zhuyin conversion.

- [Chinese Typing Practice](https://readtypechinese.com/) Shows sentences and have users type them. Input-method agnostic, so tells users whether the characters typed are right or wrong, but no feedback on how to type it correctly (in term of which key strokes).

- [Taiwan Forum on Zhuyin Practicing Software](https://tw.forumosa.com/t/any-typing-software-website-to-practice-zhuyin-fuhao/69998/19) Discussion forum shows there are learners looking to practice Zhuyin, but no mainstream software exists. Also, word that some software exists in Taiwan but is passed down by word of mouth. (Excerpts:

  "Yes, there is, it exists, but I haven’t seen it years. I remember there was a copy floating around at MTC that the teachers were passing around."

  "Yes there is. Go to the nearest public grade school in your place with a friend and ask if they have Chinese Language class for foreign spouses. As part of the language class curriculum, there is one class for typing chinese language. They have a small adobe flash program that can improve how you type zhuyin fuhao.")

- [typing.tw](https://typing.tw/) Typing test website that tells you your typing speed. Made for traditional Chinese characters. Input agnostic. Has time limit. Good for users to practice speed after they learn how to type correctly. However, no Zhuyin-specific feedback.

- [Another typing contest site](https://contest.hlc.edu.tw/typing/content_bpmf.asp?lang=1) Has a preset list of phrases for typing practice, and shows the Zhuyin symbols for each word. Site all in Chinese, hard for foreign learners to navigate.

# Application Pitch

**Name**: ZHYN  
(the word "Zhuyin" but without vowels, would still be read as "Zhuyin")

**Motivation**: Provides a platform for learners to practice typing Chinese characters via Zhuyin input system, and provides Zhuyin-specific feedback.

**Key Features**:

**Level Selection** - User can select levels (beginner, intermediate, advanced), so that the characters presented to users during typing practice can more closely match their language level and ability. Users will be learners of different level and ability, and this feature allows the app to be usuable for all learner levels (ex: a beginner Mandarin learner will only know the most basic Chinese characters, displaying advanced characters will be testing their knowledge of Chinese language rather than ability to type in Zhuyin.) Stakeholders benefit because users are more likely to stay engaged and progress effectively.

**Statistics** - After each typing session, display key statistics to users, such as their accuracy rate and typing speed. Additionally, display the correct Zhuyin symbols for characters that user typed incorrectly, providing targeted feedback for learning.

**Adaptive Immersion** - Users can switch the app interface between English and Chinese, allowing beginners to gradually increase language exposure while maintaining comprehension. This reduces frustration, supports comprehension, and caters to both foreign learners and native speakers.

# Concept Design

## Concept Specifications

**concept** Database  
**purpose** generate sentences tailored to a User's level  
**principle** each generate creates a random sentence with Chinese characters suitable to User level  
**state**  
a set of Levels with  
&emsp; a set of Characters

a set of Characters with  
&emsp; a ZhuyinRep

**actions**  
register (Character, ZhuyinRep)  
&emsp; **requires** Character doesn't already exist  
&emsp; **effect** add Character and associate with that ZhuyinRep

addCharacter (Character, Level)  
&emsp; **requires** Character not already in Level, Character exists and has a ZhuyinRep  
&emsp; **effect** associate Character to Level

removeCharacter (Character, Level)  
&emsp; **requires** Character in Level  
&emsp; **effect** remove Character from Level

generateSentence (Level, topic: String): (sentence: String)  
&emsp; **effect** Use LLM to generate a sentence on given topic using only characters in that Level. Return sentence.

getAnswer (Character): (ZhuyinRep)  
&emsp; **effects** returns the ZhuyinRep associated with the Character

---

**concept** Quiz [Character, ZhuyinRep]  
**purpose** track User's Zhuyin typing ability  
**principle** track the speed and accuracy for each Character that user typed  
**state**  
a set of Questions with  
&emsp; a Character  
&emsp; a ZhuyinRep  
&emsp; a speed Number  
&emsp; a correct Flag

**actions**  
register (Character, ZhuyinRep)  
&emsp; **effect** create a new Question with associated Character and ZhuyinRep

logStats (Question, speed: Number, correct: Boolean)  
&emsp; **requires** Question exists, speed is positive, Question doesn't already have speed , Question correct Flag not set  
&emsp; **effect** update Question with speed and correct Flag

getSpeed (Question): (speed: Number)  
&emsp; **requires** Question exists and stats logged  
&emsp; **effect** return speed associated with Question

getAccuracy (Question): (correct: Flag)  
&emsp; **requires** Question exists and stats logged  
&emsp; **effect** return correct Flag associated with Question

---

**concept** DisplayLanguage [DefaultLanguage]  
**purpose** Allows users to have an adaptive language immersion experience  
**principle** After a display language is complete, user will be able to view application in that language  
**state**  
a set of DisplayLanguages with  
&emsp; a DisplaySet  
&emsp; a complete Flag

a set of DisplaySets with  
&emsp; a set of TranslationEntries

a set of TranslationEntries with  
&emsp; a Section  
&emsp; a translation String

a set of Sections with  
&emsp; a sectionContent String (this string is in DefaultLanguage)  
&emsp; a ready Flag

**actions**  
register (DisplayLanguage)  
&emsp; **requires** DisplayLanguage doesn't already exist, DisplayLanguage is not Default Language  
&emsp; **effect** create a DisplayLanguage with a new, empty DisplaySet, and complete Flag set to False

addTranslation (DisplayLanguage, Section, translation: String)  
&emsp; **requires** DisplayLanguage exists, Section exists, translation assumed valid (correct translation for that section)  
&emsp; **effect** create new TranslationEntry with associated Section and translation, add new TranslationEntry to DisplaySet associated with DisplayLanguage

completeLanguage (DisplayLanguage)  
&emsp; **requires** DisplayLanguage must have a translation for all Sections marked ready  
&emsp; **effect** marks DisplayLanguage as complete

addSection (sectionContent: String)  
&emsp; **requires** Section doesn't already exist  
&emsp; **effect** creates a new Section with sectionContent and ready Flag as False

readySection (Section)  
&emsp; **requires** Section has a TranslationEntry for all DisplayLanguages marked complete  
&emsp; **effect** marks Section as ready

## Syncs

**sync** register  
**when** Database.generateSentence (Level, topic): (sentence: String)  
**then**  
for every Character in sentence:  
&emsp; Database.getAnswer(Character): (ZhuyinRep)  
&emsp; Quiz.register(Character, ZhuyinRep)
