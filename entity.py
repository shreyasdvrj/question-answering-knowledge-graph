import spacy
import pandas as pd
import extract

nlp = spacy.load('en_core_web_sm')

def normal_sent(sentence):

        time, place = extract.get_time_place_from_sent(sentence)

        subject_list, object_list = [], []

        aux_relation, child_with_comp = "", ""

        subject_list = extract.find_subj(sentence)
        object_list, buffer_obj = extract.find_obj(sentence, place, time)
        relation, aux_relation = extract.find_relation(buffer_obj)

        ent_pairs = []

        if time:
            time = time[0]
        else:
            time = ""

        if place:
            place = place[0]
        else:
            place = ""

        pa, pb=[], []
        for m in subject_list:
            pa.append([m])

        for n in object_list:
            pb.append([n])

        if len(object_list)==0:
          pb.append([buffer_obj])

       

        for m in range(0, len(pa)):
            for n in range(0, len(pb)):
                ent_pairs.append([str(pa[m][0]).lower(), str(relation).lower(),str(aux_relation).lower(), str(pb[n][0]).lower(), str(time), str(place)])

        return ent_pairs

def get_entity(text):

        
        ent_pairs, final_entity_pairs = [],[]
        sentences = [one_sentence.text.strip() for one_sentence in text.sents]


        for one_sentence in sentences:
            final_entity_pairs = []
            one_sentence = nlp(one_sentence)
            dep = [token.dep_ for token in one_sentence]

            normal_sent_ = normal_sent(one_sentence)

            if normal_sent_:
              
                normal_sent_[0].append(str(one_sentence))
                
                for pair in normal_sent_:
                    ent_pairs.append(pair)

                    if len(pair)==6 :
                      pair.append(str(one_sentence))
                      ent_pairs.append(pair)


                pairs = pd.DataFrame(ent_pairs, columns=['source', 'relation', 'aux_relation', 'target', 'time', 'place', 'sentence'])
               
                number_of_ent_pairs = str(len(ent_pairs))

                final_entity_pairs.append(pairs)

        if final_entity_pairs:
            return final_entity_pairs, number_of_ent_pairs    

        return None, None