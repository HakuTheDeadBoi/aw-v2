from os.path import join

from lxml import etree

from aw.query import Query
from aw.constraint import Constraint
from aw.constraintgroup import ConstraintGroup

class QueryParser:
    ROOT = "queries"

    def __init__(self):
        self.etree = etree
        self.file = ""
        self.xmlTree = None
        self.root = None
        self.lastQueryId = 0
        self.filePath = ""
    
    def loadFile(self, path):
        with open(path, "r") as FILE:
            self.xmlTree = self.etree.parse(FILE)
            self.root = self.xmlTree.getroot()
            lastQuery = self.root.xpath("//query[last()]")

            if lastQuery is not None:
                self.lastQueryId = int(lastQuery[0].attrib["id"])
            else:
                self.lastQueryId = 0

    def newFile(self):
        self.root = self.etree.Element(QueryParser.ROOT)
        self.xmlTree = self.etree.ElementTree(self.root)
        self.lastQueryId = 0
    
    def initFile(self, rootPath, destDir, fileName):
        self.filePath = join(rootPath, destDir, fileName)

        try:
            self.loadFile(self.filePath)
        except (FileNotFoundError, IOError) as e:
            self.newFile()
    
    def addQuery(self, query):
        # <query>
        newQuery = self.etree.SubElement(self.root, "query")
        newQuery.set("id", self.lastQueryId + 1)
        self.lastQueryId += 1

        # <query><q>
        newQ = self.etree.SubElement(newQuery, "q")
        newQ.text = query.q

        for group in query.groups:
            # <query><constraint-group>
            newGroup = self.etree.SubElement(newQuery, "constraint-group")
            newGroup.set("bool-relation", group.boolRelation)

            for constraint in group.constraints:
                # <query><constraint-group><constraint>
                newConstraint = self.etree.SubElement(newGroup, "constraint")
                newConstraint.set("type", constraint.type)
                newConstraint.set("relation", constraint.relation)
                newConstraint.text = "f{constraint.key}:{constraint.value}"

    def deleteQuery(self, queryId):
        query = self.root.find(f".//*[@id='{str(queryId)}']")
        if query is not None:
            self.root.remove(query)
    

    def saveFile(self):
        self.etree.write(self.filePath, encoding="utf-8", xml_declaration=False, pretty_print=True)

    def getQueryList(self):
        queryList = []
        for xmlQuery in self.root.findall('query'):
            newQuery = Query()
            # get query text
            newQuery.q = xmlQuery.find('q').text

            for group in xmlQuery.findall('constraint-group'):
                newGroup = ConstraintGroup()
                newGroup.boolRelation = group.get("bool-relation")

                for constraint in group.findall('constraint'):
                    newConstraint = Constraint()
                    newConstraint.type = constraint.get("type")
                    newConstraint.relation = constraint.get("relation")
                    newConstraint.preventDecap = constraint.get("prevent-decap")
                    newConstraint.key, newConstraint.value = constraint.text.split(":")

                    newGroup.constraints.append(newConstraint)
                
                newQuery.groups.append(newGroup)
            
            queryList.append(newQuery)

        return queryList

            



        
