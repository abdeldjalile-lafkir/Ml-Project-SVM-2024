import random
import mysql.connector
import numpy as np
import mysql.connector
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd
from colorama import init , Fore , Style


Connection_Key = mysql.connector.connect(host="localhost", user="root", password="",database="PROJECTAIdatabase")
SQL = Connection_Key.cursor()

text = (" Lorem Ipsum has $ been the 0000000000 industry's standard dummy text ever since "
        " the 1500s, ! when ¤ an unknown GARANTED printer took %¤ a galley of & PRIZE type and scrambled 0000000000 it "
        " to 000-000-00-00-00 make https://www.kaggle.com/  a type CONGRATULATION  specimen ¤ book. It has CLICK % survived not only  @ ¤ ERROR https://jetbrains.com/ five centuries,"
        " but  FREE also / URGENT the leap into  ) DONT MISS OUT  electronic ½ typesetting,WINNER remaining essentially "
        " containing IPHONE Lorem _ - Ipsum 0000000000 passages, HERE and _  more recently with desktop publishing "
        " GIFT 0000000000 software £ DOLLAR like Aldus £ PageMaker ( including $ versions of https://github.com/ Lorem Ipsum. ")


# REPROSSESING DATA : # Replace all periods and commas ann whitespaces and regularwords with an empty string
def PREPROCESSING_DATA( MESSAGE ):
    pattern01 = r'\d{1,}'
    pattern02 = r'[^a-zA-Z0-9$.,€£\s]'
    pattern03 = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
    pattern04 = r'\s+'
    pattern05 = r'(?:\$|€|£|¥|₹|﷼|₽)\s*'

    CLEANED_MESSAGE = MESSAGE.lower()
    CLEANED_MESSAGE = re.sub(pattern01, '', CLEANED_MESSAGE)
    CLEANED_MESSAGE = re.sub(pattern02, '', CLEANED_MESSAGE)
    CLEANED_MESSAGE = re.sub(pattern03, '', CLEANED_MESSAGE)
    CLEANED_MESSAGE = re.sub(pattern04, ' ', CLEANED_MESSAGE)
    CLEANED_MESSAGE = re.sub(pattern05, '', CLEANED_MESSAGE)
    return CLEANED_MESSAGE


def ACCURCY_TEST( MODEL_CLASSIFIVATION_LIST , VALIDATION_LABELES_LIST ):

    CORRECTCLASSIFICATIONCOUNTER = 0
    for i in range(2000) :
        if(  VALIDATION_LABELES_LIST[i] == MODEL_CLASSIFIVATION_LIST[i]):
            CORRECTCLASSIFICATIONCOUNTER += 1

    return (CORRECTCLASSIFICATIONCOUNTER / 2000) * 100




# SPLIT DATA INTO TRAIN VALIDATION AND TEST
TRAINING_LABELES_LIST = []
TRAINING_FEATURES_LIST = []

VALIDATION_LABELES_LIST = []
VALIDATION_FEATURES_LIST = []

TESTING_LABELES_LIST = []
TESTING_FEATURES_LIST = []

SQL.execute(f" SELECT * From FINALEDATASETTABLE WHERE LABEL = 'ham'")
SQL_DATASET = SQL.fetchall()
i = 0
for row in SQL_DATASET:

    CLEANED_ROW = PREPROCESSING_DATA(row[1])

    if (i < 2500):  #2500 SAMPLE OF TRAINING DATA
        TRAINING_LABELES_LIST.append(0)
        TRAINING_FEATURES_LIST.append(CLEANED_ROW)
        i += 1
    elif (2500 <= i < 3500):  # 1000 SAMPLE OF VALIDATION DATA
        VALIDATION_LABELES_LIST.append(0)
        VALIDATION_FEATURES_LIST.append(CLEANED_ROW)
        i += 1
    elif (3500<= i < 3600):  # 100 SAMPLE OF VALIDATION DATA
        TESTING_LABELES_LIST.append(0)
        TESTING_FEATURES_LIST.append(CLEANED_ROW)
        i += 1



SQL.execute(f" SELECT * From FINALEDATASETTABLE WHERE LABEL = 'spam'")
SQL_DATASET = SQL.fetchall()
i = 0
for row in SQL_DATASET:

    CLEANED_ROW  =PREPROCESSING_DATA(row[1])

    if (i < 2500):  #2500 SAMPLE OF TRAINING DATA
        TRAINING_LABELES_LIST.append(1)
        TRAINING_FEATURES_LIST.append(CLEANED_ROW)
        i += 1
    elif (2500 <= i < 3500):  # 1000 SAMPLE OF VALIDATION DATA
        VALIDATION_LABELES_LIST.append(1)
        VALIDATION_FEATURES_LIST.append(CLEANED_ROW)
        i += 1
    elif (3500<= i < 3600):  # 100 SAMPLE OF VALIDATION DATA
        TESTING_LABELES_LIST.append(1)
        TESTING_FEATURES_LIST.append(CLEANED_ROW)
        i += 1

'''
print("training")
print(len(TRAINING_LABELES_LIST))
print(len(TRAINING_FEATURES_LIST))
print("validation")
print(len(VALIDATION_LABELES_LIST))
print(len(VALIDATION_FEATURES_LIST))
print("test")
print(len(TESTING_LABELES_LIST))
print(len(TESTING_FEATURES_LIST))
'''

# MODEL FOR EXTRACT FEATURES :
''''''
COUNT_VECTORISER_MODEL = CountVectorizer()
TRAINING_FEATURES_ARRAY = COUNT_VECTORISER_MODEL.fit_transform(np.array(TRAINING_FEATURES_LIST))
TRAINING_LABELES_ARRAY = np.array(TRAINING_LABELES_LIST).reshape(-1)

# SVM MODEL FOR TESTING THE IMPLEMENTATION SYSTEM
'''
MODEL01 = SVC(kernel='linear' )
MODEL01.fit( TRAINING_FEATURES_ARRAY  ,   np.array(TRAINING_LABELES_LIST).reshape(-1))
print(TESTING_FEATURES_LIST[1])
TEST_FEATURE = COUNT_VECTORISER_MODEL.transform(np.array(TESTING_FEATURES_LIST[1]).reshape(-1))
TEST_LABEL = MODEL01.predict(TEST_FEATURE)
print(f"resultssss :  {TEST_LABEL}")
'''




# CREATE A MODEL AND TRAIN IT :

MODEL02 = SVC(kernel='linear' , C=0.1)
MODEL02.fit( TRAINING_FEATURES_ARRAY , TRAINING_LABELES_ARRAY )


#TUNE HYPERPARAMETERS SYSTEM WITH VALIDATION DATA
'''
FEATURS_EXTRUCTION_METHOD = 'COUNTVECTORIZEREXTRACTION'  # MANUAL OR COUNTVECTORISER
MARGINSSSSS = 'SOFT'  # DEFULTS , HARD inf   OR SOFT 0.1
KERNALLLLLL = 'LINEAR'   #LINEAR POLYNOMINALE(degree,coffes) RBF(gamma=defults,auto)
TRAININGDATASIZE = 5000  # for each label

MODEL_CLASSIFIVATION_LIST = []
for validationsample in VALIDATION_FEATURES_LIST:
    VALIDATION_MESSAGE_FEATURES = COUNT_VECTORISER_MODEL.transform(np.array(validationsample).reshape(-1))
    VALIDATION_LABEL = MODEL02.predict(VALIDATION_MESSAGE_FEATURES)
    MODEL_CLASSIFIVATION_LIST.append(VALIDATION_LABEL)


MODEL_RATE = ACCURCY_TEST(MODEL_CLASSIFIVATION_LIST , VALIDATION_LABELES_LIST)
print(f"THE ACCURACY OF NEW MODEL : {round(MODEL_RATE,2)}")
'''


#SQL.execute(f"INSERT INTO PROJRCTAI_MODELSSPECIFICATION (FEARTURES, MARGINS, THEKARNEL, TRAININGDATA, ACCURACY) VALUES ( '{FEATURS_EXTRUCTION_METHOD}','{MARGINSSSSS}', '{KERNALLLLLL}', '{TRAININGDATASIZE}', '{MODEL_RATE}' )")
#Connection_Key.commit()


print("------------------------------------------------------------------------------------------>")


def SYSTEM_RECOGNITION_HEADER( MESSAGE ):

    #PREPROCESSING_DATA(MESSAGE)
    TESTSAMPLE_HELPER = COUNT_VECTORISER_MODEL.transform(np.array(PREPROCESSING_DATA(MESSAGE)).reshape(-1))
    return TESTSAMPLE_HELPER


def LABEL_TRANSFER( NUMBER ):
    SHARSLABEL = " "
    if (NUMBER == 0):
        SHARSLABEL = " HAM "
    elif (NUMBER == 1):
        SHARSLABEL = " SPAM "

    return SHARSLABEL


print("     WELCOM HERO ! \n "
      " THIS IS ABDELJALIL's SYSTME RECOGNITION PROJECT FOR CLASSIFING EMAILS EITHERS HAM EMAILS OR SPAMS !"
      " ALL CODE EXPLANITION IN README FILE "
      " HOPE ENJOY TO USE IT : \n\n")


init()
USERCHOICE = 1
while (USERCHOICE == 1 ):

    START_KEY = input("\n DO YOU WANT A RANDOM MESSEGE FOR TEST THE SYSTEM ? TYPE 'YES'/'yes'! : ")
    if (START_KEY == 'YES' or START_KEY == 'yes') :
        RANDOM_TESTING_MESSAGE = random.randint(0, 199)
        print(f" message : {TESTING_FEATURES_LIST[RANDOM_TESTING_MESSAGE]}")



    CLIENT_EMAIL_MESSAGE = input("\n ENTER OR PAST YOUR EMAIL BODY HEROOOOOOOO : ")
    TESTSAMPLE = SYSTEM_RECOGNITION_HEADER( CLIENT_EMAIL_MESSAGE )
    TESTLABEL = MODEL02.predict(TESTSAMPLE)


    if TESTLABEL == 0 : print(Fore.BLUE + f"THIS MESSAGE IS A {LABEL_TRANSFER(TESTLABEL)} EMAIL \n " + Style.RESET_ALL)
    else : print(Fore.RED + f"THIS MESSAGE IS A {LABEL_TRANSFER(TESTLABEL)} EMAIL \n " + Style.RESET_ALL)

    if (START_KEY == 'YES' or START_KEY == 'yes'):
        RghitClass = input("\n DO YOU WNAT TO SEE RGHIT CLASS OF THIS MESSAGE ? TYPE 'YES'/'yes'! : ")
        if (RghitClass == 'YES' or RghitClass == 'yes') : print(f"THE CORRECT LABEL OF THIS EMAIL : {TESTING_LABELES_LIST[RANDOM_TESTING_MESSAGE]}")


    CLOSEINGKEY = input("\n ANOTHER TRY ? TYPE 'ENTER' FOR CONTENUE | TYPE EXIT/exit  FOR EXIT THE SYSTEM INTERFACE : ")
    if CLOSEINGKEY == 'EXIT' or CLOSEINGKEY == 'exit' : break


print("\n\n SEEYEA BROTHER | TAKE CARE OF UR SELF !!! ")

