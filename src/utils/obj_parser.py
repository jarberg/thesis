from src.constants import *

class ObjParser:

    def __init__(self, filepath, method="r"):
        self.filepath = os.path.join(ROOT_DIR,filepath)
        self.file_obj = open(self.filepath, method)


    def __enter__(self):
        self.mtls = []
        self.objects = []
        self.vertices = []
        self.normals = []

        self._parse(self.file_obj)


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _parse(self, fileString, scale=1, reverse=False):
        lines = self.file_obj.read().split('\n')
        lines.append(None)

        index = 0
        currentObject = OBJObject("")
        self.objects.append(currentObject)
        currentMaterialName = ""

        line = lines[index]
        sp = StringParser()

        while line is not None:
            sp.set_string(line)
            sp.index = 0
            command = sp.getWord()

            if command == "#" or command == None:
                index += 1
                line = lines[index]
                continue
                
            elif command == "mtllib":
                path = self._parseMtlLib(sp, self.filepath)
                mat = MTL_object(path)
                self.mtls.append(mat)

            elif command == "o":
                pass
            elif command == "g":
                pass
            elif command == "v":
                pass
            elif command == "vn":
                pass
            elif command == "usemtl":
                pass
            elif command == "f":
                pass

            index += 1
            line = lines[index]

    def _parseObjectName(self, sp):
        pass

    def _parseVertex(self, sp, scale):
        pass

    def _parseNormal(self,sp):
        pass

    def _parseUsemtl(self,sp):
        pass

    def _parseMtlLib(self, sp, filepath):
        path = filepath.replace(r"\\\\", r"/")
        dirPath = filepath.rsplit("\\",1)
        ret = dirPath[0] +"\\"+ sp.getWord()
        return ret


class StringParser:

    def __init__(self):
        self.index = 0

    def set_string(self, string):
        self.string = string

    def getWord(self):
        self.skipDelimiters()
        n = self.get_word_length(self.string, self.index)
        if n == 0: return None
        word = self.string[self.index: self.index+n]
        self.index += (n+1)
        return word

    def skipDelimiters(self):
        for i in range(self.index ,len(self.string)):
            c = self.string[i]
            if c == "\t" or c == " " or c == "(" or c == ")" or c == '"':
                continue
            self.index = i
            break

    def get_word_length(self, string, start):
        n = 0
        for i in range(start, len(string)):
            n = i
            c = string[i]
            if c == "\t" or c == " " or c == "(" or c == ")" or c == '"' or c == None:
                break
            if i == len(string)-1:
                n+=1
        return n-start

    def getFloat(self):
        return float(self.getWord())

from utils.objects import Material


class MTL_object:
    def __init__(self, path):
        self.path = path
        self.complete = False
        self.materials = []
        self._onReadMTLFile()

    def _onReadMTLFile(self):
        with open(self.path) as f:
            lines = f.read().split('\n')
            lines.append(None)

            index = 0

            line = lines[index]
            sp = StringParser()
            name = ""
            while line is not None:
                sp.index = 0
                sp.set_string(line)
                command = sp.getWord()


                if command == "#" or command == None:
                    index += 1
                    line = lines[index]
                    continue

                elif command == "newmtl":
                    name = self._parseNewmtl(sp)

                elif command == "Kd":
                    if name == "":
                        continue   # Go to the next line because of Error
                    material = self._parseRGB(sp, name)
                    self.materials.append(material)
                    name = ""

                index += 1
                line = lines[index]

        self.complete = True

    def _parseRGB(self, sp, name):
        r = sp.getFloat()
        g = sp.getFloat()
        b = sp.getFloat()
        return Material(name, r, g, b, 1)

    def _parseNewmtl(self, sp):
        return sp.getWord()


class OBJObject:
    def __init__(self, _name):
        self.name = _name
        self.faces = []
        self.numIndices = 0

with ObjParser(r"res\models\charlie\charlie.obj") as parser:
    print("hello")