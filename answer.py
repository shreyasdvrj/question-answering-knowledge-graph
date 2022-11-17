import qp
import json 
import spacy 
import re
import inflect

nlp = spacy.load('en_core_web_sm')
def findanswer(question):
        p = qp.question_pairs(question)
        if p == [] or p is None:
            return "Not Applicable", "Not Applicable"

        pair = p[0]

        f = open("./content/database.json","r", encoding="utf8")

        
        listData = f.readlines()
        
        pos=0
        relQ = []
        
        loaded = json.loads(listData[0])
        relationQ = nlp(pair[1])


        for i in relationQ:
            relationQ = i.lemma_
            relQ.append(relationQ)

        objectQ = pair[3]
        subList = []
        sentenceList = [] # append sentences 
        timeQ = str(pair[4]).lower()
        placeQ = str(pair[5]).lower()

        relationQ = " ".join(relQ)
#-------------------------------------------------WHO-----------------------------------------
        if pair[0] in ('who'):

            

            for i in loaded:
                relationS = [relation for relation in nlp(loaded[str(i)]["relation"])]
                relationSSS = " ".join([relation.lemma_ for relation in nlp(loaded[str(i)]["relation"])])

                relationS = [i.lemma_ for i in relationS]
                relationS = relationS[0]

                if (relationS == relationQ) or (relationS in relationQ) or (relationQ in relationS):
                    objectS = loaded[str(i)]["target"]
                    objectS = re.sub('-', ' ', objectS)
                    objectQ = re.sub('-', ' ', objectQ)

                    if inflect.engine().singular_noun(objectS):
                        objectS = inflect.engine().singular_noun(objectS)
                    if inflect.engine().singular_noun(objectQ):
                        objectQ = inflect.engine().singular_noun(objectQ)

                    if (objectS == objectQ) or (objectQ in objectS) or (objectS in objectQ):
                        if str(pair[4]) != "":
                            timeS = [str(loaded[str(i)]["time"]).lower()]
                            if timeQ in timeS:
                                answer_subj = loaded[str(i)]["source"]
                                target = loaded[str(i)]["target"]
                                subList.append(answer_subj)
                                
                                answer_sent = loaded[str(i)]["sentence"]
                                
                                if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)

                            else:
                                answer_subj = loaded[str(i)]["source"]
                                target = loaded[str(i)]["target"]
                                subList.append(answer_subj)
                                
                                answer_sent = loaded[str(i)]["sentence"]


                                if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)

                        else:
                            answer_subj = loaded[str(i)]["source"]
                            target2 = loaded[str(i)]["target"]
                            subList.append(answer_subj)
                            answer_sent = loaded[str(i)]["sentence"]

                            if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)

                    elif (loaded[str(i)]["source"])==objectQ or objectQ in loaded[str(i)]["source"]:
                            answer_subj = loaded[str(i)]["source"]
                            subList.append(answer_subj)
                            answer_sent = loaded[str(i)]["sentence"]


                            if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)

                    

                elif str(relationSSS) == str(relationQ) or (relationSSS in relationQ) or (relationQ in relationSSS):
                    objectS = loaded[str(i)]["target"]
                    objectS = re.sub('-', ' ', objectS)

                    if objectS == objectQ:
                        if str(pair[4]) != "":
                            timeS = [str(loaded[str(i)]["time"]).lower()]
                            if timeQ in timeS:
                                answer_subj = loaded[str(i)]["source"]
                                subList.append(answer_subj)
                                answer_sent = loaded[str(i)]["sentence"]


                                if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)
                        else:
                            answer_subj = loaded[str(i)]["source"]
                            subList.append(answer_subj)
                            answer_sent = loaded[str(i)]["sentence"]


                            if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)

            
            finalSentenceList=[]

            for j in sentenceList :
              if j != None:
                finalSentenceList.append(j)


            answer_subj = ",".join(subList)
            answer_sent = " ".join(finalSentenceList)

            
            if answer_subj == "":
                return "None", "Sorry. Model couldn't fetch the answer. Please rephrase or ask a different question."

            return answer_subj, answer_sent
#-------------------------------------------------WHAT-----------------------------------------

        elif (pair[3] in ['what']) or (pair[3] in ['which']):
            
            subjectQ = pair[0]
            subList = []
            for i in loaded:

                
                subjectS = loaded[str(i)]["source"]
                objectS = loaded[str(i)]["target"]

                if (subjectQ == subjectS) or ( subjectQ in subjectS ) or (subjectS in subjectQ) or (subjectQ == objectS) or (subjectQ in objectS) or (objectS in subjectQ):
                    
                    relationS = [relation for relation in nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    if len(relationS) > 1:
                        relationS = " ".join(relationS)
                    else:
                        relationS = relationS[0]
                    

                    if (relationQ == relationS) or (relationS in relationQ) or (relationQ in relationS):
                        if str(pair[5]) != "":
                            placeS = [str(place).lower() for place in nlp(loaded[str(i)]["place"])]
                            if placeQ in placeS:
                                if str(pair[4]) != "":
                                    timeS = [str(time).lower() for time in nlp(loaded[str(i)]["time"])]
                                    if timeQ in timeS:
                                        answer_subj = loaded[str(i)]["target"]
                                        subList.append(answer_subj)
                                        answer_sent = loaded[str(i)]["sentence"]
                                        
                                        if answer_sent.startswith(('This','this','That','that')):
                                          answer_sent = loaded[str(int(i)-1)]["sentence"] + loaded[str(i)]["sentence"]

                                      
                                        if answer_sent not in sentenceList:
                                          sentenceList.append(answer_sent)
                                else:
                                    answer_subj = loaded[str(i)]["target"]
                                    subList.append(answer_subj)
                                    answer_sent = loaded[str(i)]["sentence"]

                                    if answer_sent.startswith(('This','this','That','that')):
                                      answer_sent = loaded[str(int(i)-1)]["sentence"] + loaded[str(i)]["sentence"]

                                    # sentenceList.append(answer_sent)
                                    if answer_sent not in sentenceList:
                                      sentenceList.append(answer_sent)
                        else:
                            if str(pair[4]) != "":
                                timeS = [str(time).lower() for time in nlp(loaded[str(i)]["time"])]
                                if timeQ in timeS:
                                    answer_subj = loaded[str(i)]["target"]
                                    
                                    if answer_subj not in subList:
                                      subList.append(answer_subj)
                                    answer_sent = loaded[str(i)]["sentence"]
                                    if answer_sent.startswith(('This','this','That','that')):
                                      answer_sent = loaded[str(int(i)-1)]["sentence"] + loaded[str(i)]["sentence"]
                                    
                                    if answer_sent not in sentenceList:
                                      sentenceList.append(answer_sent)
                            else:
                                answer_subj = loaded[str(i)]["target"]
                                if answer_subj not in subList:
                                  subList.append(answer_subj)
                                answer_sent = loaded[str(i)]["sentence"]
                                if answer_sent.startswith(('This','this','That','that')):
                                  answer_sent = loaded[str(int(i)-1)]["sentence"] + loaded[str(i)]["sentence"]
                                if answer_sent not in sentenceList:
                                  sentenceList.append(answer_sent)
                    
                    elif subjectQ in loaded[str(i)]["sentence"] or (objectQ in loaded[str(i)]["sentence"]):
                    
                          answer_subj = loaded[str(i)]["target"]
                          subList.append(answer_subj)
                          answer_sent = loaded[str(i)]["sentence"]
                          if answer_sent not in sentenceList:
                            sentenceList.append(answer_sent)
                        

                if ( int(i) < int(len(loaded)-1)):
                  pass

          
            finalSentenceList=[]

            for j in sentenceList :
              if j != None:
                finalSentenceList.append(j)


            answer_obj = ",".join(subList)
            answer_sent = " ".join(finalSentenceList)

            if answer_obj == "":
                return "None", "Sorry. Model couldn't fetch the answer. Please rephrase or ask a different question."


            return answer_obj, answer_sent
#-------------------------------------------------WHEN-----------------------------------------
        elif pair[4] in ['when']:
            subjectQ = pair[0]

            for i in loaded:
                subjectS = loaded[str(i)]["source"]
                if (subjectQ == subjectS) or (subjectQ in subjectS) or (subjectS in subjectQ) :
                    
                    relationS = [relation for relation in nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relBuffer = relationS

                    if len(relBuffer) < 2:
                        relationS = relBuffer[0]
                    else:
                        if str(relBuffer[1]).lower() == 'to':
                            relationS = " ".join(relationS)
                        else:
                            relationS = relationS[0]
                            extraIN = relBuffer[1].lower()

                    if relationQ == relationS or (relationS in relationQ) or (relationQ in relationS):
                        if str(pair[5]) != "":
                            placeS = [str(place).lower() for place in nlp(loaded[str(i)]["place"])]
                            
                            if placeQ in placeS:
                                if loaded[str(i)]["time"] != '':
                                    answer_obj = loaded[str(i)]["time"]
                                # elif extraIN == "in" or extraIN == "on":
                                    # answer_obj = loaded[str(i)]["target"]
                                    return answer_obj, loaded[str(i)]['sentence']
                                elif ( int(i) < int(len(loaded)-1)):
                                  #more lines present in json to read
                                  pass
                                else:
                                  return None, "Sorry. Model couldn't fetch the answer. Please rephrase or ask a different question."
                        else:
                            if loaded[str(i)]["time"] != '':
                                answer_obj = loaded[str(i)]["time"]
                                return answer_obj, loaded[str(i)]['sentence']
                            elif ( int(i) < int(len(loaded)-1)):
                                  #more lines present in json to read
                                  pass
                            else: 
                              return None, "Sorry. Model couldn't fetch the answer. Please rephrase or ask a different question."

#-------------------------------------------------WHERE-----------------------------------------

        elif pair[5] in ['where'] or pair[3] in ['where']:
            subjectQ = pair[0]
            temp=''
            temp_sent=''
            answer_obj=''
            for i in loaded:

                subjectS = loaded[str(i)]["source"]

                if (subjectQ == subjectS) or (subjectQ in subjectS) or (subjectS in subjectQ): #or (subjectQ == objectS) or (subjectQ in objectS) or (objectS in subjectQ):
                    
                    relationS = [relation for relation in nlp(loaded[str(i)]["relation"])]
                    relationS = [i.lemma_ for i in relationS]
                    relationS = relationS[0]

                    if relationQ == relationS or (relationS in relationQ) or (relationQ in relationS):
                        if (str(pair[5])=='where') or (str(pair[3])=='where'):

                          if len(loaded[str(i)]["place"])==0:
                            temp = loaded[str(i)]["target"]
                            temp_sent = loaded[str(i)]["sentence"]
                          
                          answer_obj = loaded[str(i)]["place"]
                          
                          if len(answer_obj)!=0:
                            return answer_obj, loaded[str(i)]['sentence']

                          if ( int(i) < int(len(loaded)-1)):
                                pass
                          else:
                            return answer_obj, loaded[str(i)]['sentence']

            if len(answer_obj)==0:
                      return temp, temp_sent