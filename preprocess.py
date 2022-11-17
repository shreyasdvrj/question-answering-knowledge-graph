import spacy
nlp = spacy.load('en_core_web_sm')

'''
pronouns->nouns conversion, upper lower case handle 
'''
def resolved( text ):
        flag = True

        official_subject = "Unknown"

        sentences = []
        prev_subjs = []

        temp_text = text
        
        #pos_of_brackets = {pos:char for pos, char in enumerate(temp_text) if str(char) in ("(",")")}

        text = nlp(text) #spacy

        i=0
        for sent in text.sents:
            prev_subj, compound_is, last_word = "", "", ""

            dep_word = [word.dep_ for word in sent] # part of speech tagging - subj, prep, auxpass and so on 

            word_dep_count_subj = [dep_word.index(word) for word in dep_word if word in ('nsubj', 'subj', 'nsubjpass')] # give position of subject in sentence


            try:
                word_dep_count_subj = word_dep_count_subj[-1] + 1 # pick position of last subject 
            except IndexError:
                word_dep_count_subj = 1
            #list of dependencies that are subjects in each sentence
            more_subjs = [word for word in dep_word if word in ('nsubj', 'subj', 'nsubjpass')]

            for word in sent:
              
                if len(more_subjs) > 1: #outermost if
                    if word.dep_ in more_subjs: #one l
                        #list of more_subjs > 1 and has nsubjpass in it then break
                        if word.dep_ in ['nsubjpass']: #two l
                            break
                        #list of more_subjs > 1 and has nsubj and subj in it then 
                        elif word.dep_ in ('nsubj','subj'):  #two l
                            #if position is non negative and not first position
                            if word_dep_count_subj > 0: #three l
                                # """ IN prime minister it gives compound and then nmod """
                                if word.dep_ in ('compound') or word.dep_ in ('nmod', 'amod'): #four l
                                    if compound_is == "": #five l
                                        compound_is = str(word)
                                        word_dep_count_subj = word_dep_count_subj - 1
                                    else: #five l
                                        compound_is = compound_is+ " " +str(word)
                                        word_dep_count_subj = word_dep_count_subj - 1

                                elif word.dep_ in ('nsubj', 'subj', 'nsubjpass'): #four l
                                    pronoun = [i for i in word.subtree]

                                    if compound_is == "": #five l
                                        if str(word) not in ('him','he','HE', 'He','she','SHE', 'She','They','they','Them','them'): #six l
                                            prev_subj = str(word)
                                            if str(pronoun[0]) not in ('him','his','His', 'her','Her', 'its', 'Its','Their','their'): #seven l
                                                prev_subjs = [prev_subj]
                                                official_subject = prev_subjs[0]
                                                word_dep_count_subj = word_dep_count_subj - 1

                                    else: #five l
                                        if str('poss') in [str(i.dep_) for i in word.subtree]: #six l
                                            prev_subj = compound_is
                                            word_dep_count_subj = word_dep_count_subj - 1
                                            prev_subjs = [prev_subj]
                                            # official_subject = prev_subjs[0]
                                        else: #five l
                                            prev_subj = compound_is+" "+str(word)
                                            word_dep_count_subj = word_dep_count_subj - 1
                                            prev_subjs = [prev_subj]
                                            official_subject = prev_subjs[0]

                                  
                                    if str(word) in ('him','he','HE', 'He','she','SHE', 'She','They','they','Them','them'):
                                        
                                        new_word = prev_subjs[-1]
                                        
                                        sentences.append(str(sent).replace(str(word), str(new_word)))
                                        flag = False

                                    if pronoun:
                                        if len(pronoun) <= 2 and str(pronoun[0]) in ('him','his','His', 'her','Her', 'its', 'Its','Their','their'):                                           
                                            new_word = str(official_subject)+"\'s"
                                            sentences.append(str(sent).replace((str(pronoun[0])), str(new_word)))
                                            flag = False
                                        elif len(pronoun)>2 and str(pronoun[0]) in ('him','his','His', 'her','Her', 'its', 'Its','Their','their'):
                                            new_word = str(official_subject)+"\'s"
                                            sentences.append(str(sent).replace(str(pronoun[0]), str(new_word)))
                                            flag = False


                                elif word.dep_ in ('nsubj','subj','nsubjpass') and str(word) not in ('he','HE', 'He','she','SHE', 'She','They','they','Them','them'):
                                    last_word = word
                                else:
                                    pass
                else:
                    if word_dep_count_subj > 0:
                        # """ IN prime minister it gives compound and then nmod """
                        if word.dep_ in ('compound') or word.dep_ in ('nmod', 'amod'):
                            if compound_is == "":
                                compound_is = str(word)
                                word_dep_count_subj = word_dep_count_subj - 1
                            else:
                                compound_is = compound_is+ " " +str(word)
                                word_dep_count_subj = word_dep_count_subj - 1

                        elif word.dep_ in ('nsubj', 'subj', 'nsubjpass'):
                            pronoun = [i for i in word.subtree]

                            if compound_is == "":
                                if str(word) not in ('him','he','HE', 'He','she','SHE', 'She','They','they','Them','them'):
                                    prev_subj = str(word)
                                    if str(pronoun[0]) not in ('his','His', 'her','Her', 'its', 'Its','Their','their'):
                                        prev_subjs = [prev_subj]
                                        official_subject = prev_subjs[0]
                                        word_dep_count_subj = word_dep_count_subj - 1

                            else:
                                if str('poss') in [str(i.dep_) for i in word.subtree]:
                                    prev_subj = compound_is
                                    word_dep_count_subj = word_dep_count_subj - 1
                                    prev_subjs = [prev_subj]
                                    # official_subject = prev_subjs[0]
                                else:
                                    prev_subj = compound_is+" "+str(word)
                                    word_dep_count_subj = word_dep_count_subj - 1
                                    prev_subjs = [prev_subj]
                                    official_subject = prev_subjs[0]

                            # if str(word) in ('they'):
                                # subject_list.extend([str(a.text) for a in word.subtree if a.dep_ in ('conj')])
                            if str(word) in ('him','he','HE', 'He','she','SHE', 'She','They','they','Them','them'):
                                new_word = prev_subjs[-1]
                                sentences.append(str(sent).replace(str(word), str(new_word)))
                                flag = False

                            if pronoun:
                                if len(pronoun) <= 2 and str(pronoun[0]) in ('him','his','His', 'her','Her', 'its', 'Its','their','Their'):
                                    new_word = str(official_subject)+"\'s"
                                    sentences.append(str(sent).replace((str(pronoun[0])), str(new_word)))
                                    flag = False
                                elif len(pronoun)>2 and str(pronoun[0]) in ('him','his','His', 'her','Her', 'its', 'Its','Their','their'):
                                    new_word = str(official_subject)+"\'s"
                                    sentences.append(str(sent).replace(str(pronoun[0]), str(new_word)))
                                    flag = False


                        elif word.dep_ in ('nsubj','subj','nsubjpass') and str(word) not in ('he','HE', 'He','she','SHE', 'She','They','they','Them','them'):
                            last_word = word
                        else:
                            pass

            if flag:
                sentences.append(str(sent))
            else:
                flag = True

        resolved_text = " ".join(sentences)
        return resolved_text

def preprocess_text(input_file):
      text_strip = [text.strip() for text in input_file]
      preprocessed_text = [text for text in text_strip if text not in ('', ' ')]
      text = " ".join(preprocessed_text)
      input_data = text
      text = resolved(text)
      text = nlp(text)
      return input_data, text