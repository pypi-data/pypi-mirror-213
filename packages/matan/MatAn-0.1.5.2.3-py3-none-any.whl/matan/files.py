import glob,os
import re
class files:
    def __init__(self,path, extension:str,methods=None, mods=None):
        """This class can manage the files as well as it's parameters

        This class helps managing he files, find their names/paths, extract the method of manufacturing or other
        parameters

        TODO: add automatically finding the method placement in names, by putting them in the method definition
        Parameters
        ----------
        path : str
            This variable is used to put path to your files
        extension : str
            Extention is the extention of your files. If your file is .csv put csv in there, be aware and do not put the dot before your extention
        methods : str
            Descripe the technique of manufacturing there, or find it using find_method in that class

        Examples
        --------
        FIXME: Add docs.

        """

        methods = [method.upper() for method in methods]
        if extension.startswith("."):
            extension=extension[1:]
        
        files=glob.glob(os.path.join(path, f"*.{extension}"))
        
        try:
            self.files=[file for file in files if any(method in file for method in methods)] 
            splitted = [os.path.split(file)[1] for file in self.files if any(method in file for method in methods)] #split to extract names
            self.paths = [file for file in self.files if any(method in file for method in methods)]
        except TypeError:
            self.files=[file for file in self.files if any(method in file for method in methods)] 
            splitted = [os.path.split(file)[1] for file in self.files if any(method in file for method in methods)]
            self.paths = [file for file in self.files]
        self.names = [name.split(".")[0] for name  in splitted]
        numbers = [name.split("_")[1] for name  in splitted]
        self.numbers=[os.path.splitext(number)[0] for number in numbers]
        self.comments= [self.find_comments(name)[0] for name in self.names]
        self.clean_names=[self.find_comments(name)[1] for name in self.names]
        if methods is not None:
            self.methods = [self.find_method(name, methods) for name in self.names ] #thats for
        if mods is not None:
            self.modifications = [self.find_modification(name, mods) for name in self.names]
        self.composition=[self.find_composition(name.split("_")[0]) for name in self.names]
    def find_method(self,name:str,
                    methods:list,
                    delimiter:str='-', ):
        """Find the technique how the material was created

        Find the method how the material was created, what methods were used to modify it, etc. To do so it is using
        first letters of filename, so for extruded parts you can use EXT, for annealed extruded parts you can use aEXT
        etc.

        Parameters
        ----------
        path : str
            path for your file
        delimiter : str
            what sign you wanna use to finish your method string. By default it is -

        Examples
        --------
        FIXME: Add docs.

        """
        name=name.split(delimiter)[0]
        for method in methods:
            if method in name:
                return method

    
    def find_modification(self, name, mods:list, place=0):
        if not  isinstance(mods, list):
            raise ValueError("Put list of modifications!")
        for mod in mods:
            letter = mod[0]
            if name[place]==letter:
                return mod
            else:
                continue
        return None
    
    def find_composition(self, name,delimiter: str='-', percent_sign="p"):
        """
        TODODO baby shark
        method to obtain material ingridiens from name, as I usually name files extracted from machine with code allowing me to get that information from filename
        """
        splitted=name.split(delimiter)
        comp={}
        for name in splitted[1:]:
            comp.update(extract_info(name))
        return comp




    def find_comments(self,s):

        pattern = r'\[.*?\]'  # a regular expression pattern to match text between square brackets
        matches = re.findall(pattern, s)  # find all matches of the pattern in the string
        comments = ''.join(matches)  # concatenate all the matches into a single string
        cleaned_text = re.sub(pattern, '', s)  # remove all the matches from the original string
        comments = re.sub(r'[\[\]]', '', comments)  # remove square brackets from the removed text
        return comments, cleaned_text

def extract_info(s):
    pattern = r'(\d+)p(.+)'
    match = re.match(pattern, s)
    result = {}
    if match:
        result[match.group(2)] = [int(match.group(1))]
    return result    
