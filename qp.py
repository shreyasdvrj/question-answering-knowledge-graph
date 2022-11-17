import spacy
nlp = spacy.load('en_core_web_sm')

import extract

def question_pairs(question__):
        
        questionNLPed = nlp(question__) #convert string(question__) into spacy token (questionNLPed)
        


        maybe_object = ([i for i in questionNLPed if i.dep_ in ('obj', 'pobj', 'dobj')])
        

        if len(maybe_object)==0:
          maybe_object = ([i for i in questionNLPed if i.dep_ in ('pcomp')])
        
        runloop = 1
        maybe_place, maybe_time = [], []
        aux_relation = ""
        maybe_time, maybe_place = extract.get_time_place_from_sent(questionNLPed)
        object_list = []
        qobj=0

        for x in maybe_object:
          if str(x).lower() == 'what':
            qobj=1

        for obj in questionNLPed:
            objectNEW = obj

#---------------------------------------------------------------------------------Determine Object List----------------------------------------------------------------------------------
            
            if (obj.dep_ in ('obj', 'dobj', 'pobj', 'xcomp','attr','acomp','pcomp') and str(obj).lower() != "what" and qobj==0) or (obj.dep_ in ('ROOT') and obj.nbor(1).dep_ == 'punct' and qobj==0) :
                buffer_obj = obj
                
                if obj.dep_ in ('xcomp') and obj.nbor(-1).dep_ in ('aux') and obj.nbor(-2).dep_ in ('ROOT'):
                    continue

                if str(obj) in maybe_place and obj.nbor(-1).dep_ in ('prep') and str(obj.nbor(-1)) == "of":
                    pass
                else:
                    if str(obj) not in maybe_time and str(obj) not in maybe_place:

                        if (obj.nbor(1)):
                          if(obj.n_rights == 0):
                            runloop = 1

                          else:
                            runloop = obj.n_rights 

                        
                        for k in range(0,runloop):

                            child = obj.nbor(k+1)

                            if str(obj) == 'who' or str(obj)=='Who':
                              runloopval = 1
                              i=0
                              while i<runloopval:
                                temp=obj.nbor(i+1)
                                if temp.dep_ in ('subj','nsubj','nsubjpass'):
                                  object_list.append(str(temp))
                                  break
                                if temp.nbor(1):
                                  runloopval+=1
                                  i+=1
                                

                            elif (child.nbor(-1).dep_ in ('conj', 'dobj', 'pobj', 'obj','ROOT')):
                                
                                if [i for i in child.nbor(-1).lefts]: #checking if the object is a compound word, in which case you append it to the list
                                     
                                    if str(child.nbor(-2)).isdigit() :
                                      child = (str(child.nbor(-2)) + " " + str(child.nbor(-1)))
                                      object_list.append(str(child))

                                    elif str(child.nbor(-2)) in ('amod','dobj') :
                                      child = (str(child.nbor(-2)) + " " + str(child.nbor(-1)))
                                      object_list.append(str(child))

                                    elif child.nbor(-2).dep_ in ('punct') and child.nbor(-3).dep_ in ('compound'):
                                        #ice-cream
                                        child = str(child.nbor(-3)) + str(child.nbor(-2)) + str(child.nbor(-1))
                                        object_list.append(str(child))

                                    elif child.nbor(-2).dep_ in ('compound'):
                                        child_with_comp = ""
                                        for i in child.nbor(-1).subtree:
                                            if i.dep_ in ('compound', 'nummod','quantmod'):
                                                if child_with_comp == "":
                                                    child_with_comp = str(i)
                                                else:
                                                    child_with_comp = child_with_comp +" "+ str(i)
                                            elif i.dep_ in ('cc'):
                                                break
                                        child = child_with_comp + " " + str(child.nbor(-1))

                                        object_list.append(str(child))
                                    elif child.nbor(-1).dep_ in ('ROOT'):
                                        object_list.append(str(child.nbor(-1)))

                                    elif child.nbor(-2).dep_ in ('det'): #check if the previous word is like an article or something then don't append only this word to object list
                                        # The Taj Mahal
                                        object_list.append(str(child.nbor(-1)))

                                    else:
                                      object_list.append(str(child.nbor(-1)))


                                elif [i for i in child.nbor(-1).rights]:
                                    if str(child.nbor(-1).text) not in object_list:
                                        object_list.append(str(child.nbor(-1).text))

                                    for a in child.nbor(-1).children:
                                        if a.dep_ in ('conj'):
                                            if a.nbor(-1).dep_ in ('punct'):
                                                pass
                                            else:
                                                object_list.extend( [ str(a.text) ] )

                                else:
                                    # icecream
                                    if str(child.nbor(-1)) not in object_list:
                                      
                                        object_list.append(str(child.nbor(-1)))

                            elif obj.nbor(-1).dep_ in ('xcomp'): #open clausal complement type of sentence directly implies object
                                object_list.append(str(obj.nbor(-1)))
                            elif obj.nbor(-1).dep_ in ('det'):
                                object_list.append(str(obj))
                            elif obj.dep_ in ('acomp','attr','pcomp'):
                                object_list.append(str(obj))

                            else:
                              pass

                    elif str(obj) in maybe_place and str(obj.nbor(-1)) != "of":
                        object_list.append(str(obj))
                    else:
                        if str(obj) in maybe_time and object_list == []:
                            object_list.append(str(obj))
                
                if len(object_list) == 0:
                  
                    if str(nlp(maybe_object[0].nbor(-1))).isdigit() :
                                      child = (str(maybe_object.nbor(-1)) + " " + str(maybe_object))
                                      object_list.append(str(child))

                    elif (maybe_object[0].nbor(-2)) in ('amod') :
                                      child = (str(maybe_object.nbor(-1)) + " " + str(maybe_object))
                                      object_list.append(str(child))
                    else:
                      object_list.append(maybe_object)
                
                obj = object_list[-1]
                check=(obj)

                if len(nlp(check))==1:
                    count=0
                    for x in maybe_object:
                      if check==str(x):
                        count=1
                        break
                            
                    if count==0:
                      for x in maybe_object:
                        if (x).dep_ in ('dobj'):
                          obj=x
                          break
                        if (x).dep_ in ('pobj'):
                          obj=x
                          break
                        if (x).dep_ in ('obj'):
                          obj=x
                          break
                        if (x).dep_ in ('oprd'):
                          obj=x
                          break

#--------------------------------------------------------------------------------WHO-------------------------------------------------------------------------------------
                
                relation = [w for w in objectNEW.ancestors if w.dep_ =='ROOT'] # relation will be the root word which is on the newly appended obj list
                
                if len(relation) == 0:
                  relation = [w for w in objectNEW.lefts if w.nbor(1).dep_ =='ROOT']

                
                if relation:
                    relation = relation[0]
                    sp_relation = relation
                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        if relation.nbor(2).dep_ in ('xcomp'):
                            aux_relation = str(relation.nbor(2))
                            relation = str(relation)+" "+str(relation.nbor(1))
                        else:
                            relation = str(relation)

                    subject = [a for a in sp_relation.lefts if a.dep_ in ('subj', 'nsubj','nsubjpass','attr')]  # identify subject nodes - which will be to the left of therelation
                    
                    
                    if subject:
                        subject = subject[0]

                    else:
                        # subject = 'unknown'
                        subject='who'
                else:
                    # relation = 'unknown'
                    relation.append('unknown')
               
                ent_pairs = []

                if maybe_time and maybe_place:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str(maybe_time[0]).lower(), str(maybe_place[0]).lower()])
                elif maybe_time:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str(maybe_time[0]).lower(), str("").lower()])
                elif maybe_place:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str("").lower(), str(maybe_place[0]).lower()])
                else:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str("").lower(), str("").lower()])

                return ent_pairs

#---------------------------------------------------------------------------------WHAT----------------------------------------------------------------------------------
            elif str(obj).lower() == "what" or str(obj).lower() == "which" :
   
                relation = [w for w in objectNEW.ancestors if w.dep_ =='ROOT']
                if relation:
                    relation = relation[0]
                    sp_relation = relation

                    if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                        if relation.nbor(2).dep_ in ('xcomp'):
                            aux_relation = str(relation.nbor(2))
                            relation = str(relation)+" "+str(relation.nbor(1))
                        else:
                            relation = str(relation)

                    subject = extract.find_subj(questionNLPed)
                    subject = subject[-1]

                    if len(subject)== 0 or subject=='' or subject==' ':
                      subject=maybe_object[0]

                else:
                    relation = 'unknown'

                ent_pairs = []
      
                if maybe_time and maybe_place:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str(maybe_time[0]).lower(), str(maybe_place[0]).lower()])
                elif maybe_time:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str(maybe_time[0]).lower(), str("").lower()])
                elif maybe_place:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str("").lower(), str(maybe_place[0]).lower()])
                else:
                    ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(obj).lower(), str("").lower(), str("").lower()])

                return ent_pairs

#---------------------------------------------------------------------------------WHERE----------------------------------------------------------------------------------
            elif obj.dep_ in ('advmod'):
                if str(obj).lower() == 'where':
                    relation = [w for w in obj.ancestors if w.dep_ =='ROOT']
                    if (len(relation) >0):
                        relation = relation[0]
                        sp_relation = relation
                        if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                          # ADP is preposition and to, during
                          if relation.nbor(2).dep_ in ('xcomp'):
                                aux_relation = str(relation.nbor(2))
                                relation = str(relation)+" "+str(relation.nbor(1))
                          else:
                                relation = str(relation)
                                
                        subject = extract.find_subj(questionNLPed)
                        subject = subject[-1]

                    else:
                        relation = 'unknown'

                    ent_pairs = []
                    
                    
                    if maybe_object:
                        if maybe_time and maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_time:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("").lower(), str("where").lower()])
                        else:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("").lower(), str("where").lower()])
                    else:
                        if maybe_time and maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_time:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str(maybe_time[0]).lower(), str("where").lower()])
                        elif maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("").lower(), str("where").lower()])
                        else:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("").lower(), str("where").lower()])


                    return ent_pairs

#---------------------------------------------------------------------------------WHEN----------------------------------------------------------------------------------

                elif str(obj).lower() == 'when':

                    relation = [w for w in obj.ancestors if w.dep_ =='ROOT']
                 
                    if relation:
                        relation = relation[0]
                        sp_relation = relation
                        if relation.nbor(1).pos_ in ('ADP', 'PART', 'VERB'):
                            if relation.nbor(2).dep_ in ('xcomp'):
                                relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                            else:
                                relation = ' '.join((str(relation), str(relation.nbor(1))))
                                

                        for left_word in sp_relation.lefts:
                            if left_word.dep_ in ('subj', 'nsubj','nsubjpass'):
                                if [i for i in left_word.lefts]:
                                    for left_of_left_word in left_word.lefts:
                                        subject = str(left_of_left_word) + " " + str(left_word)
                                else:
                                    subject = str(left_word)
                       
                    else:
                        relation = 'unknown'

                    ent_pairs = []
                    
                    if maybe_object:
                        if maybe_time and maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        elif maybe_time:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str("").lower()])
                        elif maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        else:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str(maybe_object[-1]).lower(), str("when").lower(), str("").lower()])
                    else:
                        if maybe_time and maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        elif maybe_time:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str("").lower()])
                        elif maybe_place:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str(maybe_place[0]).lower()])
                        else:
                            ent_pairs.append([str(subject).lower(), str(relation).lower(),str(aux_relation).lower(), str("").lower(), str("when").lower(), str("").lower()])

                    
                    return ent_pairs