import random
import renpy.store as store
import renpy.exports as renpy
from mer_person import Person 
import inspect



class MetaPerson(Person):#all metapersons should inherit from this
    meta_code = ""
    def __init__(self):
        super(MetaPerson, self).__init__()


class UniqueMetaPerson(MetaPerson):#all unique metapersons should inherit from this
    not_used = True
    def __init__(self):
        super(MetaPerson, self).__init__()



class GenPerson(Person):#all character generators should inherit from this
    def __init__(self):
        super(GenPerson, self).__init__()
        self.avatar = self.get_avatar()#path to metaperson's avatar
        if not self.avatar or len(self.avatar.split("/")) != 9:#we wait that path starts with "characters/generic or unique/morphology/gender/age/color"
            self.avatar = "characters/none.jpg"
            return
        self.meta_path = self.get_meta_path()#path to a folder containing this metaperson
        self.meta_code = self.get_script()#name of this metaperson's script file     
        self.meta_person = self.call_script()
        self.color = self.meta_path.split('/')[5]
        if self.meta_path.split('/')[4] in ("child", "young", "adult", "elder"):
            self.age = self.meta_path.split('/')[4]
        if self.meta_path.split('/')[3] in ("male", "female", "shemale", "sexless"):
            self.gender = self.meta_path.split('/')[3]
        self.species = self.meta_path.split('/')[2]
        if self.meta_person:
            for key in self.meta_person.__dict__:
                self.__dict__[key] = self.meta_person.__dict__[key]
            self.meta_person = None






    def get_metapersons(self): #creates list of available metapersons
        files = [f for f in renpy.list_files() if f.startswith("characters/generic") and "avatar" in f]
        return files

    def get_avatar(self):
        available = self.get_metapersons()
        if len(available) > 0:
            return random.choice(available)
        return None

    def get_meta_path(self):#get path to a metaperson
        meta_holder = self.avatar.split('/')
        meta_holder.pop()
        meta_holder.remove('avatar')
        meta_path = ""
        for name in meta_holder:
            meta_path += "%s/"%(name)
        return meta_path

    def get_script(self):
        for f in renpy.list_files():
            if f.startswith("%sscript"%(self.meta_path)):
                script = f.split('/').pop()
                return script
        return None

    def call_script(self):
        if self.meta_code:
            sub_list = []
            for sub in MetaPerson.__subclasses__():
                if sub.meta_code in self.meta_code:
                    sub_list.append(sub)
            if len(sub_list) > 0:
                return random.choice(sub_list)()
        else:
            return None

class GenPersonByGender(GenPerson):
    def __init__(self, gender):
        self.search_gender = gender
        super(GenPersonByGender, self).__init__()
    def get_metapersons(self):
        files = [f for f in renpy.list_files() if f.startswith("characters/generic") and "avatar" in f and self.search_gender in f.split('/')]
        return files



class GenUnique(GenPerson):
    def __init__(self):
        super(GenUnique, self).__init__()
    def get_metapersons(self):
        files = [f for f in renpy.list_files() if f.startswith("characters/unique") and "avatar" in f]
        return files
    def call_script(self):
        if self.meta_code:
            sub_list = []
            for sub in UniqueMetaPerson.__subclasses__():
                if sub.meta_code in self.meta_code and sub.not_used:
                    sub.not_used = False
                    sub_list.append(sub)
            if len(sub_list) > 0:
                return random.choice(sub_list)()
        else:
            return None
class GenUniqueById(GenUnique):
    def __init__(self, uniqueid="None"):
        self.uniqueid = uniqueid
        super(GenUniqueById, self).__init__()
    def get_metapersons(self):
        files = [f for f in renpy.list_files() if f.startswith("characters/unique") and "avatar" in f and self.uniqueid in f]
        return files
