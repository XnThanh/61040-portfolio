<concept_spec>

concept Database

purpose 
    generate sentences tailored to a User's level

principle 
    Characters and their ZhuyinRep are added and assigned to one or more Levels (by admin, not user);
    User action can generate a random sentence with Chinese characters suitable to their level using LLM;

state
    a set of Levels with  
        a set of Characters

    a set of Characters with  
        a ZhuyinRep

    invariants
        every Character has a unique ZhuyinRep
        every level has a unique Character set

    note (to self, and to grader)
        in uncommon instances, a single Chinese Character may have more than one ZhuyinRep. 
        These are known as polyphonic characters. The scope of this project will assume one ZhuyinRep per Character.

actions  
    register (Character, ZhuyinRep)  
        requires Character doesn't already exist  
        effect add Character and associate with that ZhuyinRep

    addCharacter (Character, Level)  
        requires Character not already in Level, Character exists and has a ZhuyinRep  
        effect associate Character to Level

    removeCharacter (Character, Level)  
        requires Character in Level  
        effect remove Character from Level

    generateSentence (Level, topic: String): (sentence: String)  
        effect Get Characters in Level; Use LLM to generate a sentence on given topic using only characters in that Level. Return sentence.

    getAnswer (Character): (ZhuyinRep)  
        effect returns the ZhuyinRep associated with the Character

</concept_spec>