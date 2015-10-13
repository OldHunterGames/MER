import random
import renpy.store as store
import renpy.exports as renpy
from mer_person import Person 


metapersonsdict = {'generic':{}, 'unique':{}}
def check_script(metaname):
    for f in renpy.list_files():
        if f.startswith("characters") and 'script' in f and metaname in f:
            holder = f.split('/')
            return holder[len(holder)-1]
    return None

def init_metapersons_dict():
    for f in renpy.list_files():
        if f.startswith("characters/generic") and "avatar" in f:
            key = f.split("/")[6]
            color = f.split("/")[5]
            age = f.split("/")[4]
            gender = f.split("/")[3]
            morphology = f.split("/")[2]
            script = check_script(key)
            if key in metapersonsdict['generic']:
                metapersonsdict['generic'][key]['avatars'].append(f)
            else:
                metapersonsdict['generic'][key] = {
                'morphology':morphology,
                'gender':gender, 
                'age':age, 
                'color':color,
                'avatars':[f], 
                'script':script
                }
        if f.startswith("characters/unique") and "avatar" in f:
            key = f.split("/")[6]
            color = f.split("/")[5]
            age = f.split("/")[4]
            gender = f.split("/")[3]
            morphology = f.split("/")[2]
            script = check_script(key)
            metapersonsdict['unique'][key] = {
                'morphology':morphology,
                'gender':gender, 
                'age':age, 
                'color':color,
                'avatars':[f], 
                'script':script,
                'allready_used': False
                }
    return


init_metapersons_dict()
class GenPerson(Person):
    def __init__(self, metaname=None, frequency="generic", *args, **kwargs):
        self.frequency = frequency
        self.metaname = metaname
        self.meta_person = self.get_metaperson()
        super(GenPerson, self).__init__()
        self.color = self.get_parameter('color')
        self.gender = self.get_parameter('gender')
        self.age = self.get_parameter('age')
        self.morphology = self.get_parameter('morphology')
        self.meta_code = self.get_parameter("script")
        self.avatar = self.get_parameter("avatars")
        if self.meta_code:
            self.metastats = self.call_script()
        else:
            self.metastats = None
        if self.metastats:
            for key in self.metastats.__dict__:
                self.__dict__[key] = self.metastats.__dict__[key]

    def get_metaperson(self):
        if self.metaname:
            return self.metaname
        return random.choice(metapersonsdict[self.frequency].keys())

    def get_parameter(self, param):
        if param == "avatars":
            return random.choice(metapersonsdict[self.frequency][self.meta_person][param])        
        return metapersonsdict[self.frequency][self.meta_person][param]
    def call_script(self):
        sub_list = []
        for sub in MetaPerson.__subclasses__():
            if sub.meta_code in self.meta_code:
                sub_list.append(sub)
            if len(sub_list) > 0:
                return random.choice(sub_list)()
            else:
                return None
class GenPersonByGender(GenPerson):
    def __init__(self, gender, *args, **kwargs):
        self.gender = gender
        super(GenPersonByGender, self).__init__()
    def get_metaperson(self):
        l = []
        for meta in metapersonsdict[self.frequency].keys():
            if metapersonsdict[self.frequency][meta]['gender'] == self.gender:
                l.append(meta)
        if len(l) > 0:
            return random.choice(l)
        raise Exception("No persons with such gender, %s"%(self.gender))


class GenUnique(GenPerson):
    def __init__(self, metaname=None, frequency="unique", *args, **kwargs):
        self.frequency = 'unique'
        super(GenUnique, self).__init__(metaname, frequency)
    def get_metaperson(self):
        uniques = metapersonsdict[self.frequency].keys()
        if self.metaname and not metapersonsdict[self.frequency][self.metaname]['allready_used']:
            return self.metaname
        l = []
        for meta in uniques:
            used = metapersonsdict[self.frequency][meta]['allready_used']
            if not used:
                l.append(meta)
                metapersonsdict[self.frequency][meta]['allready_used'] = True
        if len(l) > 0:
            return random.choice(l)
        self.frequency = 'generic'
        return random.choice(metapersonsdict['generic'].keys())
    def call_script(self):
        sub_list = []
        for sub in UniqueMetaPerson.__subclasses__():
            if sub.meta_code in self.meta_code:
                sub_list.append(sub)
            if len(sub_list) > 0:
                return random.choice(sub_list)()
            else:
                return None

class MetaPerson(Person):#all metapersons should inherit from this
    meta_code = "NotImplemented"
    def __init__(self):
        super(MetaPerson, self).__init__()


class UniqueMetaPerson(MetaPerson):#all unique metapersons should inherit from this
    def __init__(self):
        super(MetaPerson, self).__init__()


