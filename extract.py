def get_time_place_from_sent(sentence):
        xdate =[]
        xplace =[]
        for i in sentence.ents:
            if i.label_ in ('DATE'):
                xdate.append(str(i))

            if i.label_ in ('GPE'):
                xplace.append(str(i))

        return xdate, xplace

def find_subj(sentence):

        subject_list = []
        dep_word = [word.dep_ for word in sentence]
        #gives subject count in sentence
        word_dep_count_subj = [dep_word.index(word) for word in dep_word if word in ('nsubj', 'subj', 'nsubjpass')]
        if word_dep_count_subj:
            word_dep_count_subj = word_dep_count_subj[0] + 1
        else:
            word_dep_count_subj = 1

        subject_final = ""
        for word in sentence:
            
            if word_dep_count_subj >= 0 :
                # which it will be
                '''
                Leonardo - compound - if condition- word_dep_count_subj = 3
                Dicaprio - poss - else condition - foresee the ‘s - word_dep_count_subj = 2
                ‘s - case - elif condition - word_dep_count_subj = 1 [‘s is treated as a separate word]
                '''
                # if word.dep_ in ('compound') or word.dep_ in ('nmod') or word.dep_ in ('amod') or word.dep_ in ('poss') or word.dep_ in ('case') or word.dep_ in ('nummod'):
                if word.dep_ in ('compound','nmod','amod','poss','case','nummod','attr'):
                    if subject_final == "":
                        subject_final = str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                    elif word.dep_ in ('case'):
                        subject_final = subject_final+ "" +str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                    else:
                        subject_final = subject_final+ " " +str(word)
                        word_dep_count_subj = word_dep_count_subj - 1
                #else if the word is a subject
                elif word.dep_ in ('nsubj', 'subj', 'nsubjpass') and str(word) not in ('Who','What','When','Where','who','what','when','where','which','Which'):
                   
                    if subject_final == "":
                        subject_final = str(word)
                        subject_list.extend([str(a.text) for a in word.subtree if a.dep_ in ('conj')])
                        word_dep_count_subj = word_dep_count_subj - 1
                        break
                    else:
                        #else if not empty add to it
                        subject_final = subject_final+" "+str(word)
                        subject_list.extend([str(a.text) for a in word.subtree if a.dep_ in ('conj')])
                        word_dep_count_subj = word_dep_count_subj - 1
                        break
                elif word.dep_ in ('nsubj', 'subj', 'nsubjpass') and str(word).lower() in ('who','what','when','where','which'):
                    # x=1
                    for x in word.rights: #Rights don't work
                      if x.dep_ in ('dobj','dative','attr','oprd','nsubj'):
                        subject_final = subject_final + str(x)
                        subject_list.extend(subject_final)
                else:
                    pass

        subject_list.append(subject_final)
        return subject_list
        
def find_obj(sentence, place, time):
        object_list = []

        for word in sentence:
            # """OBJECT FINDING loop"""
            if word.dep_ in ('obj', 'dobj', 'pobj','acomp','attr','xcomp','advmod'):
              #the object will be used as variable "word"
                buffer_obj = word

                if str(word) in place and word.nbor(-1).dep_ in ('prep') and str(word.nbor(-1)) == "of":
                    pass
                else:
                    if str(word) not in time and str(word) not in place:
                        for child in word.subtree:
                            if child.dep_ in ('conj', 'dobj', 'pobj', 'obj','attr','acomp') and (str(child) not in time) and (str(child) not in place):
                                if [i for i in child.lefts]:
                                  #if child's neigbour is number or object
                                    if child.nbor(-1).dep_ in ('nummod') and child.dep_ in ('dobj', 'obj','pobj'):
                                        child = str(child.nbor(-1)) + " " + str(child)
                                        object_list.append(str(child))
                                   
                                    elif child.nbor(-1).dep_ in ('amod'): #blonde hair
                                      child = str(child.nbor(-1)) +" "+ str(child)
                                      object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('punct'):
                                        if child.nbor(-2).dep_ in ('compound'):
                                            #ice-cream
                                            child = str(child.nbor(-2)) + str(child.nbor(-1)) + str(child)
                                            object_list.append(str(child))

                                        elif child.nbor(-2).dep_ in ('amod'):
                                            #social-distancing
                                            child = str(child.nbor(-2)) + str(child.nbor(-1)) + str(child)
                                            object_list.append(str(child))

                                    #else if the child's neighbour is compound
                                    elif child.nbor(-1).dep_ in ('compound'):
                                        child_with_comp = ""
                                        for i in child.subtree:
                                            if i.dep_ in ('compound', 'nummod','quantmod'):
                                                if child_with_comp == "":
                                                    child_with_comp = str(i)
                                                else:
                                                    child_with_comp = child_with_comp +" "+ str(i)
                                            elif i.dep_ in ('cc'):
                                                break
                                        child = child_with_comp + " " + str(child)
                                        object_list.append(str(child))

                                    elif child.nbor(-1).dep_ in ('det'):
                                        # eg: The Taj Mahal
                                        object_list.append(str(child))
                                #Check in right side of subtree also and if the child not there then append it to object list
                                elif [i for i in child.rights]:
                                    if str(child.text) not in object_list:
                                        object_list.append(str(child.text))

                                    for a in child.children:
                                        if a.dep_ in ('conj'):
                                            if a.nbor(-1).dep_ in ('punct'):
                                                pass
                                            else:
                                                object_list.extend( [ str(a.text) ] )

                                else:
                                    # icecream
                                    if str(child) not in object_list:
                                        object_list.append(str(child))

                    elif str(word) in place and str(word.nbor(-1)) != "of":
                        if object_list == []:
                            object_list.append(str(word))
                        else:
                            pass
                    else:
                        if str(word) in time and object_list == []:
                            object_list.append(str(word))

        if len(object_list)==0:
              for word in sentence:
                if str(word) in ('.'):
                  check=-1
                  while word.nbor(check):
                    x=word.nbor(check)
                    if x.dep_ in ('nsubj'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('pcomp'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('acomp'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('compound'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('ccomp'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('attr'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('advmod'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    elif x.dep_ in ('ROOT'):
                      buffer_obj=x
                      object_list.append(str(x))
                      break
                    check=check-1

        
        return object_list, buffer_obj

def find_relation(buffer_obj):

        aux_relation = ""
        # RELATION FINDING loop
        relation = [w for w in buffer_obj.ancestors if w.dep_ =='ROOT']
        #if dependency returned a relation enter this else it returns unknown below
        if relation:
            relation = relation[0]
            sp_relation = relation
            if relation.nbor(1).pos_ in ('VERB'):
                if relation.nbor(2).dep_ in ('xcomp'):
                    relation = ' '.join((str(relation), str(relation.nbor(1)), str(relation.nbor(2))))
                else:
                    relation = str(relation)
                    if str(sp_relation.nbor(2)) != 'and':
                        if sp_relation.nbor(1).dep_ in ('xcomp'):
                            aux_relation = str(sp_relation.nbor(1))
                        else:
                            aux_relation = str(sp_relation.nbor(2))
            #something with elif (if not in VERB)
            #ADP- Adposition (in, to, during) and PART- particle ('s, not)
            elif relation.nbor(1).pos_ in ('ADP', 'PART') and relation.nbor(1).dep_ in ('aux') and str(relation.nbor(1)) == 'to':
                relation = " ".join((str(relation), str(relation.nbor(1))))
                if str(sp_relation.nbor(2)) != 'and':
                    aux_relation = str(sp_relation.nbor(2))
            
            elif relation.nbor(1).dep_ in ('prep') and str(relation.nbor(1)) == 'to' and (relation.nbor(1)).dep_ not in ('obj','dobj','pobj','det'):

                relation = " ".join((str(relation), str(relation.nbor(1))))
            else:
                relation = str(relation)
        
        elif buffer_obj.dep_ in ('ROOT'):
          if buffer_obj.nbor(-2).dep_ in ('aux') :
            relation = str(buffer_obj.nbor(-2))
          if buffer_obj.nbor(-1).dep_ in ('auxpass'):
            aux_relation = str(buffer_obj.nbor(-1))
            

        else:
            relation = 'unknown'

        return relation, aux_relation