import json

#importing custom functions
import answer
import entity 
import graph
import qp 
import preprocess 

def build():
  input_file = open('./content/data.txt',"r+")
  input_data, refined_text = preprocess.preprocess_text(input_file)

  dataEntities, numberOfPairs = entity.get_entity(refined_text)
  if dataEntities:
      dataEntities[0].to_json('./content/database.json', orient='index')
  # graph.createGraph(dataEntities[0])
  return input_data

def build_graph():
  input_file = open('./content/data.txt',"r+")
  input_data, refined_text = preprocess.preprocess_text(input_file)

  dataEntities, numberOfPairs = entity.get_entity(refined_text)
  graph.createGraph(dataEntities[0])

def qna_system(ip_question):
  # ip_question=input("Enter your question. ")
  p = qp.question_pairs(ip_question)
  pair = p[0]

  Answer, Sentence = answer.findanswer(ip_question)

  outputAnswer = []
  [outputAnswer.append(x) for x in Answer.split(',') if x not in outputAnswer]


  outputSentence = Sentence.split('.')
  outputSentence.pop()

  # for eachAnswer in set(outputSentence):
  #   print(eachAnswer)
  
  final_ans = '. '.join(set(outputSentence))
  return final_ans
