from tests.fdstest import FunctionalDependencySetTest
from functional_dependencies.fdsbase import Notation, RelSchema, Set,FD
from functional_dependencies.BCNF import FunctionalDependencySet
import functional_dependencies.fds as fd
import logging

class Test_UB7(FunctionalDependencySetTest):
    '''
    test examples for dbis-ub 7
    '''
    def setUp(self):
        debug=True
        profile=True
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        FunctionalDependencySetTest.setUp(self, debug=debug, profile=profile)
        
    def getNonBCNF(self,fdsset):
        for fds in fdsset:
            for fd in fds:
                if not fds.isFDinBCNF(fd):
                    return fds,fd
        return None,None
    
    def decompose(self,rs,verbose:bool=False):
        '''
        decomposition algorithm according to DBIS-VL
        Source: https://dbis.rwth-aachen.de/dbis-vl/RelDesign#page=82
        and https://stackoverflow.com/a/18399094/1497139
        '''
        # Initialize S = {R} 
        # Starte mit Z= { R,F}
        # need to refactor later currently attributes are in fds
        S={rs.fds}
        # While S has a relation R' that is not in BCNF do:  
        # Solange es noch ein Schema ℛ  ∈ 𝑍 gibt, das nicht in BCNF ist:
        fdsxy,fdxy=self.getNonBCNF(S)
        count=0
        while fdxy is not None: 
            # Pick a FD: X->Y that holds in R' and violates BCNF
            newFds=FunctionalDependencySet()
            left,right=fdxy
            for attr_name in left | right:
                attr=fdsxy.get_attribute(attr_name)
                newFds.add_an_attribute(attr)
            S.update(newFds)
            #    Add the relation XY to S
            #    Update R' = R'-Y
            # @FIXME - needs to be implemented here
            fdsxy,fdxy=self.getNonBCNF(S)
            count+=1
            if count>1000:
                raise Exception("endless loop in decompose")
        
        # Return S
        self.isdecompose=True
        return S
        
    def getExample71(self):
        '''
        test Aufgabe 7.1
        '''
        fds=FunctionalDependencySet()
        fds.add_attribute("A","country","Land")
        fds.add_attribute("B","altitude","Meereshöhe")
        fds.add_attribute("C","givenName","Vorname")
        fds.add_attribute("D","surname","Nachname")
        fds.add_attribute("E","occupation","Beruf")
        fds.add_attribute("F","runway","Startbahn")
        fds.add_attribute("G","length","Länge")        
        fds.add_dependency("CDE","AB")
        fds.add_dependency("CD","E")
        fds.add_dependency("CDE","F")
        fds.add_dependency("F","G")
        rs=RelSchema(fds.attributes,fds,notation=Notation.math)
       

        fd1 = fd.FD({"C","D","E",}, {"A","B"}) # Airport
        fd2 = fd.FD({"CD"}, {"E"}) # Person named after - occupation
        fd3 = fd.FD({"CDE"}, {"F"}) # runway
        fd4 = fd.FD({"F"}, {"G"}) # runway length
        
        fdsm=fd.FDSet({fd1,fd2,fd3,fd4})
        return rs,fdsm
    
    def showRs(self,rs):
        print(rs)
        for attribute in rs.fds.attribute_map.values():
            print(f"{attribute.var_name}≡{attribute.english_name}≡{attribute.german_name}")
     
    def test7_1AttributeClosure(self):
        rs,fdsm=self.getExample71()
        for attribute in rs.fds.attribute_map.values():
            cl=rs.fds.get_attr_closure(attribute.var_name)
            print(cl)
        
    def test7_1a(self):
        '''
        test Excercise 7.1
        '''
        rs,fdsm=self.getExample71()
        self.showRs(rs)
        print(rs.fds.as_graphviz())
        # candidate keys - BCNF
        print(f"-------------------------------------------- Candidate keys BCNF")

        ckset=rs.fds.find_candidate_keys()
        print('ckeys:',Set.stringify_set(ckset,notation=Notation.short))

        # candidate keys - Münster
        print(f"-------------------------------------------- Candidate keys Münster")

        rs7_1=fd.RelSchema(fdsm.attributes(),fdsm)
        keyset=rs7_1.key()
        print("ckeys", Set.stringify_set(keyset,notation=Notation.short))

    def test71b(self):
        rs,fdsm=self.getExample71()
        # attribute closures - BCNF
        print(f"-------------------------------------------- Attribute closures BCNF")
        attrsets=["ACF","CD","AD","F"]
        for attrset in attrsets:
            clos = rs.fds.get_attr_closure(attrset)
            print(f"attr closure of {attrset}:",Set.stringify_set(clos,notation=Notation.short))
            closOer = fdsm.closure(attrset)
            print(f"attr closure of {attrset}:",Set.stringify_set(closOer,notation=Notation.short))
            
    
            
    def test72a(self):
        rs,fdsm=self.getExample71()
        print (f"2NF: {rs.fds.is2NF()}")
        print (f"3NF: {rs.fds.is3NF()}")
                
    def test72b(self):
        '''
        Übung 7.2 b
        '''
        rs,fdsm=self.getExample71()
        # synthesis - BCNF
        print(f"-------------------------------------------- Synthese BCNF")

        synth =rs.fds.synthesize(verbose=True)
        print('synthesis:',Set.stringify_set(synth,notation=Notation.short))

        # synthesis - Münster
        print(f"-------------------------------------------- Synthese Münster")

        rs7_2=fd.RelSchema(fdsm.attributes(),fdsm)
        synth=rs7_2.synthesize()
        print("synthesis:", Set.stringify_set(synth,notation=Notation.short))
        
    def test72bLeftAndRightReduction(self):
        '''
        '''
        rs,fdsm=self.getExample71()
        verbose=True
        _keys = rs.fds.find_candidate_keys(verbose=verbose)
        rs.fds.left_reduction(verbose=verbose)
        rs.fds.right_reduction(verbose=verbose)
        
    def test72canonicalCover(self):
        '''
        '''
        rs,fdsm=self.getExample71()
        rs.fds.canonical_cover()
        print(rs.fds)
        
    def test7_1_2022_16_15(self):
        '''
        test Aufgabe 7.1
        '''

        fds=FunctionalDependencySet("ABCDEG")
        fds.add_dependency("AB", "CG")
        fds.add_dependency("G","AE")
        fds.add_dependency("C","AG")
        fds.add_dependency("EG","D")

        fd1 = fd.FD({"A","B"}, {"G","C"})
        fd2 = fd.FD({"G"}, {"A", "E"})
        fd3 = fd.FD({"C"}, {"G", "A"})
        fd4 = fd.FD({"E","G"}, {"D"})
        fdsm=fd.FDSet({fd1,fd2,fd3,fd4})

        # candidate keys - BCNF
        print(f"-------------------------------------------- Candidate keys BCNF")

        ckset=fds.find_candidate_keys()
        print('ckeys:',Set.stringify_set(ckset,notation=Notation.short))

        # candidate keys - Münster
        print(f"-------------------------------------------- Candidate keys Münster")

        rs7_1=fd.RelSchema(fdsm.attributes(),fdsm)
        keyset=rs7_1.key()
        print("ckeys", Set.stringify_set(keyset,notation=Notation.short))

        # attribute closures - BCNF
        print(f"-------------------------------------------- Attribute closures BCNF")

        clos = fds.get_attr_closure("ABC")
        print("attr closure of ABC:",Set.stringify_set(clos,notation=Notation.short))
        clos = fds.get_attr_closure("AC")
        print("attr closure of AC:",Set.stringify_set(clos,notation=Notation.short))
        clos = fds.get_attr_closure("G")
        print("attr closure of G:",Set.stringify_set(clos,notation=Notation.short))
        clos = fds.get_attr_closure("EC")
        print("attr closure of EC:",Set.stringify_set(clos,notation=Notation.short))

        # attribute closures - Münster
        print(f"-------------------------------------------- Attribute closures Münster")

        clos = fdsm.closure("ABC")
        print("attr closure of ABC:",Set.stringify_set(clos,notation=Notation.short))
        clos = fdsm.closure("AC")
        print("attr closure of AC:",Set.stringify_set(clos,notation=Notation.short))
        clos = fdsm.closure("G")
        print("attr closure of G:",Set.stringify_set(clos,notation=Notation.short))
        clos = fdsm.closure("EC")
        print("attr closure of EC:",Set.stringify_set(clos,notation=Notation.short))

    def getExample72SynthesisOld(self):
        '''
        get the UB-7.2 Synthesis Example
        '''
        fds=FunctionalDependencySet("ABCDEF")
        fds.add_dependency("B", "CD")
        fds.add_dependency("AB","CE")
        fds.add_dependency("F","ACD")
        fds.add_dependency("EF","BD")
        fds.add_dependency("BF","C")
   

        fd1 = fd.FD({"B"}, {"C","D"})
        fd2 = fd.FD({"AB"}, {"CE"})
        fd3 = fd.FD({"F"}, {"A","C","D"})
        fd4 = fd.FD({"E","F"}, {"B","D"})
        fd5 = fd.FD({"B","F"}, {"C"})
        fdsm=fd.FDSet({fd1,fd2,fd3,fd4,fd5})
        rs=RelSchema(fds.attributes,fds,notation=Notation.math)
        return rs,fdsm
    
    def getRunwaysExample(self):
        '''
        get the airport with runway Example
        '''
        fds=FunctionalDependencySet()
        fds.add_attribute("A","airport","Flughafen")
        fds.add_attribute("B","iataCode","IATA Code")
        fds.add_attribute("C","altitude","Meereshöhe")
        fds.add_attribute("D","country","Land")
        fds.add_attribute("E","isoCode","ISO Code")
        fds.add_attribute("F","namedFor","Namensgeber")
        fds.add_attribute("G","givenName","Vorname")
        fds.add_attribute("H","surname","Nachname")
        fds.add_attribute("I","occupation","Beruf")
        fds.add_attribute("J","runway","Startbahn")
        fds.add_attribute("K","length","Länge") 
        # dependencies       
        fds.add_dependency("A","BCFJ")
        fds.add_dependency("B","A")
        fds.add_dependency("D","E")
        fds.add_dependency("E","D")
        fds.add_dependency("F","GHI")
        fds.add_dependency("J","K")
        rs=RelSchema(fds.attributes,fds,notation=Notation.math)
       

        fd1 = fd.FD({"A"}, {"B","C","F","J"}) # Airport
        fd2 = fd.FD({"B"}, {"A"}) # bijection 
        fd3 = fd.FD({"D"}, {"E"}) # country
        fd4 = fd.FD({"E"}, {"D"}) # 2nd bijection
        fd5 = fd.FD({"F"}, {"G","H","I"}) # Person named after - occupation
        fd6 = fd.FD({"J"}, {"K"}) # runway length
        
        fdsm=fd.FDSet({fd1,fd2,fd3,fd4,fd5,fd6})
        return rs,fdsm
    
    def getExample72Decompose(self):
        '''
        get the UB-7 Example
        '''
        fds=FunctionalDependencySet()
        fds.add_attribute("A","airport","Flughafen")
        fds.add_attribute("B","iataCode","IATA Code")
        fds.add_attribute("C","altitude","Meereshöhe")
        fds.add_attribute("D","country","Land")
        fds.add_attribute("E","isoCode","ISO Code")
        # dependencies       
        fds.add_dependency("A","BCD")
        fds.add_dependency("B","A")
        fds.add_dependency("D","E")
        fds.add_dependency("E","D")
        rs=RelSchema(fds.attributes,fds,notation=Notation.math)
       

        fd1 = fd.FD({"A"}, {"B","C","D"}) # Airport
        fd2 = fd.FD({"B"}, {"A"}) # bijection 
        fd3 = fd.FD({"D"}, {"E"}) # country
        fd4 = fd.FD({"E"}, {"D"}) # 2nd bijection
      
        fdsm=fd.FDSet({fd1,fd2,fd3,fd4})
        return rs,fdsm
    
    def getExample72Synthesis(self):
        return self.getExample71()
        
    def test7_2Synthesis(self):
        '''
        test Aufgabe 7.2
        '''
        rs,fdsm=self.getExample72Synthesis()
        print(rs)

        # candidate keys - BCNF
        print(f"-------------------------------------------- Candidate keys BCNF")

        ckset=rs.fds.find_candidate_keys()
        print('ckeys:',Set.stringify_set(ckset,notation=Notation.short))

        # candidate keys - Münster
        print(f"-------------------------------------------- Candidate keys Münster")

        rs7_2=fd.RelSchema(fdsm.attributes(),fdsm)
        keyset=rs7_2.key()
        print("ckeys", Set.stringify_set(keyset,notation=Notation.short))
        
        # synthesis - BCNF
        print(f"-------------------------------------------- Synthese BCNF")

        synth = rs.fds.synthesize()
        print('synthesis:',Set.stringify_set(synth,notation=Notation.short))

        # synthesis - Münster
        print(f"-------------------------------------------- Synthese Münster")

        rs7_2=fd.RelSchema(fdsm.attributes(),fdsm)
        synth=rs7_2.synthesize()
        print("synthesis:", Set.stringify_set(synth,notation=Notation.short))
        
    def test72SynthesisParts(self):
        # synthesis parts
        print(f"-------------------------------------------- Synthese Parts BCNF")

        rs,fdsm=self.getExample72Synthesis()
        fdsParts = rs.fds
        ckset=rs.fds.find_candidate_keys()

        fdsParts.left_reduction(True)
        print('After left reduction',fdsParts)
        fdsParts.right_reduction(True)
        print('After right reduction',fdsParts)
        fdsParts.remove_empty_fds(True)
        fdsParts.combine_fds(True)
        print('canonical cover',fdsParts)

        newsets = fdsParts.create_new_fdsets(True)
        print('new fdsets:',Set.stringify_set(newsets,notation=Notation.short))
        fdsets_with_key = fdsParts.create_optional_key_scheme(ckset, newsets, True)
        print('new fdsets with keyset:',Set.stringify_set(fdsets_with_key,notation=Notation.short))
        synth = fdsParts.remove_subset_relations(fdsets_with_key, True)
        print('result of remove subset relations:',Set.stringify_set(synth,notation=Notation.short))

        
    def test72Decompose(self):
        '''
        test decompose algorithm
        '''
        rs,fdsm=self.getExample72Decompose()
        self.showRs(rs)
        result=rs.fds.decompose(verbose=True)
        print(result)
        
    def test72Decompose2(self):
        '''
        test the decompose 2 algorithm
        '''
        rs,fdsm=self.getExample72Decompose()
        self.showRs(rs)
        print(rs.fds.as_graphviz())
        for fd in rs.fds:
            left,right=fd
            fdp=FD(left,right)
            fdp.notation=Notation.math
            print(f"{fdp}:{rs.fds.isFDinBCNF(fd)}")
        fdsets=rs.fds.decompose2(verbose=True)
        for fdset in fdsets:
            print(fdset)
        print (f"islossy: {rs.fds.is_lossy()}")
              
    def test72Decompose3(self):
        '''
        test the decompose 2 algorithm
        '''
        # @FixMe - implement the test and decompose
        return
        rs,fdsm=self.getExample72Decompose()
        dcRsets=self.decompose(rs,verbose=True)
        for dcrs in dcRsets:
            print(dcrs)

    
    def test7_3(self):
        '''
        test Aufgabe 7.3
        '''

        # candidate keys
        print(f"-------------------------------------------- Candidate keys BCNF")

        fds=FunctionalDependencySet("ABCDEG")
        fds.add_dependency("B", "CD")
        fds.add_dependency("AB", "CE")
        fds.add_dependency("G", "ACD")
        fds.add_dependency("EG", "BD")
        fds.add_dependency("BG", "C")
        ckset=fds.find_candidate_keys()
        print('ckeys:',Set.stringify_set(ckset,notation=Notation.short))

        # isBCNF
        print(f"-------------------------------------------- isBCNF BCNF")

        print("isBCNF:", fds.isBCNF())

        # decomposition
        print(f"-------------------------------------------- Dekompalgo BCNF")

        decomp = fds.decompose2(True)
        print('decomposition:',Set.stringify_set(decomp,notation=Notation.short))
        
        
    def getLectureExample(self): 
        fds=FunctionalDependencySet()
        fds.add_attribute("A", "", "PersNr")
        fds.add_attribute("B", "", "Name")
        fds.add_attribute("C", "", "Rang")
        fds.add_attribute("D", "", "Raum")
        fds.add_attribute("E", "", "Ort")
        fds.add_attribute("F", "", "Straße")
        fds.add_attribute("G", "", "Hausnr")
        fds.add_attribute("H", "", "PLZ")
        fds.add_attribute("I", "", "Vorwahl")
        fds.add_attribute("J", "", "Bland")
        fds.add_dependency("A","BCDEFGJ")
        fds.add_dependency("D","A")
        fds.add_dependency("A","D")
        fds.add_dependency("EFGJ","H")
        fds.add_dependency("EJ","I")
        fds.add_dependency("HE","J")
        rs=RelSchema(fds.attributes,fds,notation=Notation.math)
        return rs
    
    def testLecture(self):
        rs=self.getLectureExample()
        print(rs)
        ckset=rs.fds.find_candidate_keys()
        print(ckset)
        rs.fds.canonical_cover()
        print(rs.fds)
        
    def testLectureSynthesize(self):
        rs=self.getLectureExample()
        fdsSet=rs.fds.synthesize()
        for fds in fdsSet:
            print (fds)
            
    def testLectureDecompose(self):
        rs=self.getLectureExample()
        dcres=rs.fds.decompose()
        print(dcres)
    
    