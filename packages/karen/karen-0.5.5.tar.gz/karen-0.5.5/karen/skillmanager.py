import os, logging, random
from padatious import IntentContainer
from .shared import dayPart

class SkillManager:
    """
    Translates text commands into skill results.
    """
    
    def __init__(self, brain_obj=None, skill_folder=None):
        """
        Skill Manager Initialization
        
        Args:
            brain_obj (object): The brain object for which to process skills.
            skill_folder (str):  The path to the folder containing the skill modules.  (optional)
        """
        self.logger = logging.getLogger("SKILLMANAGER")
        self.skill_folder = skill_folder
        self.brain = brain_obj
        
        self.skills = []

    def initialize(self):
        """
        Loads all skills into memory for referencing as required.
        """
        
        self.logger.debug("Initalizing")
        
        self.intentParser = IntentContainer('/tmp/intent_cache')

        if self.skill_folder is None:
            self.skill_folder = os.path.join(os.path.dirname(__file__), "skills")
            
        skillModules = [os.path.join(self.skill_folder, o) for o in os.listdir(self.skill_folder) 
                    if os.path.isdir(os.path.join(self.skill_folder,o))]
        
        for f in skillModules:
            mySkillName = os.path.basename(f)
            self.logger.debug("Loading " + mySkillName) 
            mySkillModule = __import__(mySkillName)
            mySkillClass = mySkillModule.create_skill()
            mySkillClass.brain = self.brain
            mySkillClass.initialize()
            
        #print(self.skills)
        self.logger.debug("Skills load is complete.")
        
        self.intentParser.train(False) # False = be quiet and don't print messages to stdout

        self.logger.debug("Training completed.")

        self.logger.debug("Initialization completed.")

        
    def parseInput(self, text):
        """
        Parses inbound text leveraging skills and fallbacks to produce a response if possible.
        
        Args:
            text (str):  Input text to process for intent.
            
        Returns:
            (bool):  True on success and False on failure.
        """

        def audioFallback(in_text):
            
            if "thanks" in in_text or "thank you" in in_text:
                if self.brain is not None:
                    res = self.brain.say("You're welcome.")
                    if res:
                        return True
                
            # Some simple responses to important questions
            elif "who are you" in in_text or "who are u" in in_text:
                res = self.brain.say("I am a synthetic human.  You may call me Karen.")
                if res:
                    return True
            elif "how are you" in in_text:
                res = self.brain.say("I am online and functioning properly.")
                if res:
                    return True
            elif "you real" in in_text and len(in_text) <= 15:
                res = self.brain.say("What is real?  If you define real as electrical impulses flowing through your brain then yes, I am real.")
                if res:
                    return True
            elif "you human" in in_text and len(in_text) <= 17:
                res = self.brain.say("More or less.  My maker says that I am a synthetic human.")
                if res:
                    return True
            elif ("is your maker" in in_text or "is your father" in in_text) and len(in_text) <= 20:
                res = self.brain.say("I was designed by lnx user  one in 2020 during the Covid 19 lockdown.")
                if res:
                    return True
                                        
            self.logger.debug("fallback: " + in_text)
            return False

        try:
            intent = self.intentParser.calc_intent(text)
            #print(intent)
            # I need to be at least 60% likely to be correct before I try to process the request.
            if intent.conf >= 0.6:
                for s in self.skills:
                    if intent.name == s["intent_file"]:
                        #TODO: What happens if we get an incorrect intent determination?
                        ret_val = s["callback"](intent)
                        try:
                            if ret_val["error"] == True:
                                return audioFallback(text)
                            else:
                                return True
                        except:
                            # Should we just assume it completed successfully?
                            return True
            else:
                return audioFallback(text)
        except Exception as e:
            self.logger.debug(str(e))
            return False

        return False
    
    def stop(self):
        """
        Calls the stop method of all opened skills to close any daemon processes opened.
        
        Returns:
            (bool): True on success else raises an exception.
        """
        
        if (self.skills is not None and len(self.skills) > 0):
            for s in self.skills:
                try:
                    s["object"].stop()
                except:
                    pass

        return True
    
class Skill:
    """
    Class for inheriting to generate new skills.  Includes basic functionality for generic skills.
    """
        
    def __init__(self):
        """
        Skill Initialization
        """
        
        self._name = "Learned Skill"
        self.brain = None 
    
    def ask(self, in_text, in_callback, timeout=0):
        """
        Encapsulates the frequently used function of "ask" in order to make it easier for new skill development.  Makes self.ask() method available.
        
        Args:
            in_text (str): The text to speak to start the question/answer phase.
            in_callback (function):  The function to call when the subject responds.
            timeout (int):  The length of time to wait for a response before giving up.  A value of zero will wait forever.
            
        Returns:
            (bool): True on success and False on failure.
        """

        if self.brain is not None:
            return self.brain.ask(in_text, in_callback, timeout=timeout)
        else:
            self.logger.debug("BRAIN not referenced")

        return False
    
    def getMessageFromDialog(self, dialog_file, **args):
        """
        Retrieves a randomized line from the specified dialog file beneath the vocab/locale folder.
        
        Args:
            dialog_file (str):  Filename of the dialog for the skill from which to pull a response.
            
        Returns:
            (str): Randomized string response from the specified dialog file.
        """
        
        text = ""
        df = os.path.join(self.brain.skill_manager.skill_folder, self.__class__.__name__, "vocab", "en_us", dialog_file)
        
        if os.path.exists(df):
            with open(df,"r") as s:
                m=s.readlines()
                l=[]
                for i in range(0,len(m)-1):
                    x=m[i]
                    z=len(x)
                    a=x[:z-1]
                    l.append(a)
                l.append(m[i+1])
                text=random.choice(l)
                    
            if ("*dayPart*" in text):
                text = text.replace("*dayPart*", dayPart())
            
            return text
        else:
            return ""
        
    def getContentsFromVocabFile(self, filename):
        """
        Retrieves all text in the specified file beneath the vocab/locale folder.
        
        Args:
            filename (str):  Filename for the skill from which to read data.
            
        Returns:
            (str): Full text of the specified file.
        """
        filename = os.path.join(self.brain.skill_manager.skill_folder, self.__class__.__name__, "vocab", "en_us", filename)
        if os.path.exists(filename):
            with open(filename, "r") as f:
                text = f.read()
                
            return text
        else:
            return ""

    def initialize(self):
        """
        Function to be overridden in child classes.  This function is where intents can be registered for the padatious runtime.
        
        Returns:
            (bool):  True on success or False on failure.
        """
        return True
        
    def register_intent_file(self, filename, callback):
        """
        Registers an intent file with the Padatious neural network engine.
        
        Args:
            filename (str): The file in the vocab/local folder whose contents should be registered.
            callback (function): The function to call when the determined intent matches this data set.
            
        Returns:
            (bool):  True on success and False on failure.
        """
        
        fldr = os.path.join(self.brain.skill_manager.skill_folder, self.__class__.__name__)
        if os.path.exists(fldr):
            if os.path.exists(fldr):
                if self.brain is not None:
                    self.brain.skill_manager.intentParser.load_file(filename, os.path.join(fldr,"vocab","en_us",filename), reload_cache=True)
                    self.brain.skill_manager.skills.append({ "intent_file": filename, "callback": callback, "object": self })
                else:
                    self.logger.debug("BRAIN not referenced")
            else:
                self.logger.debug("Error registering intent file")
        else:
            self.logger.debug("Intent file not found")
            return False
        
        return True
    
    def say(self, in_text):
        """
        Encapsulates the frequently used function of "say" in order to make it easier for new skill development.  Makes self.say() method available.
        
        Args:
            in_text (str): The text to speak to start the question/answer phase.
            
        Returns:
            (bool): True on success and False on failure.
        """

        if self.brain is not None:
            return self.brain.say(in_text)
        else:
            self.logger.debug("BRAIN not referenced")

        return False

    def stop(self):
        """
        Method to stop any daemons created during startup/initialization for this skill.
        
        Returns:
            (bool):  True on success and False on failure
        """
        return True