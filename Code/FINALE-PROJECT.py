import os
import re
import numpy as np
import mysql.connector
from sklearn.svm import SVC
from colorama import init , Fore , Style


Connection_Key = mysql.connector.connect(host="localhost",user="root",password="",database="PROJECTAIdatabase")
SQL = Connection_Key.cursor()


def GET_LABELES():

    TRAINING_LABELS = []
    SQL.execute(f" SELECT LABEL From PROJRCTAI_TRAININGDATATABLE where LABEL = 0")
    SQL_TRAININGDATA = SQL.fetchall()
    i = 0
    for trainingsample in SQL_TRAININGDATA:
        TRAINING_LABELS.append(trainingsample[0])
        i += 1
        if i > 2500: break

    SQL.execute(f" SELECT LABEL From PROJRCTAI_TRAININGDATATABLE where LABEL = 1")
    SQL_TRAININGDATA = SQL.fetchall()
    i = 0
    for trainingsample in SQL_TRAININGDATA:
        TRAINING_LABELS.append(trainingsample[0])
        i += 1
        if i > 2500: break


    LABELS_HELPER = np.array(TRAINING_LABELS).reshape(-1)
    return LABELS_HELPER


def GET_FEATURES():

    TRAINING_FEATURES = []
    SQL.execute(f" SELECT PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE From PROJRCTAI_TRAININGDATATABLE where LABEL = 0 ")
    SQL_TRAININGDATA = SQL.fetchall()
    i = 0
    for trainingsample in SQL_TRAININGDATA:
        TRAINING_FEATURES.append(trainingsample)
        i += 1
        if i > 2500: break

    SQL.execute(f" SELECT PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE From PROJRCTAI_TRAININGDATATABLE where LABEL = 1 ")
    SQL_TRAININGDATA = SQL.fetchall()
    i = 0
    for trainingsample in SQL_TRAININGDATA:
        TRAINING_FEATURES.append(trainingsample)
        i += 1
        if i > 2500: break



    FEATURES_HELPER = np.array(TRAINING_FEATURES)
    return FEATURES_HELPER


def MODEL_GENERATOR(FEATURS, LABELS):

    MODEL = SVC(kernel='linear')
    MODEL.fit(FEATURS, LABELS)

    return MODEL



def PREPROCESSING_DATA( MESSAGE ):
    pattern = r'\b(?:and|or|a|an|the|is|are|was|were|be|been|being|has|have|had|do|does|did|will|would|shall|should|can|could|may|might|must|of|in|on|at|to|from|with|by|as|for|but|not|so|than|yet|either|neither|nor|although|because|if|unless|while|whereas|whether|though|since|until|before|after|during|over|under|between|among|through|above|below|beside|against|off|up|down|out|into|throughout|around|away|upon|along|across|into|onto|from|toward|underneath|within|beneath|[,])\b'
    CLEANED_DATA = re.sub(pattern, '', MESSAGE)
    CLEANED_DATA = re.sub(r'\s+', ' ', CLEANED_DATA)
    return CLEANED_DATA

def IS_THERE_PHONE_NUMBERS( MESSAGE ):
    NUMBERS_COUNT = 0
    WORDS = MESSAGE.split()
    patterns = [r'\d{3}-\d{3}-\d{2}-\d{2}-\d{2}' ,  r'\d{3}-\d{3}-\d{4}' ,  r'\d{5,}' ]
    for word in WORDS:
        for pattern in patterns:
            if re.findall(pattern, word):
                NUMBERS_COUNT += 1

    return  NUMBERS_COUNT

def IS_THERE_LINKS( MESSAGE ):
    LINKS_COUNT = 0
    WORDS = MESSAGE.split()
    pattern1 = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
    for word in WORDS:
        if re.fullmatch(pattern1, word):
            LINKS_COUNT += 1

    pattern2 = ['HTTP', 'HTTPS', 'http', 'https', 'www', 'com']
    for word in WORDS:
        for pattern in pattern2:
            if re.search(pattern, word):
                LINKS_COUNT += 1
                break

    return  LINKS_COUNT

def IS_THERE_CURRANCY_SYMBOLS( MESSAGE):
    CURRENCY_SYMBOLS_COUNT = 0
    pattern = r'(?:\$|€|£|¥|₹|﷼|₽)\s*'
    MATCHES = re.findall(pattern, MESSAGE)
    for match in MATCHES:
        CURRENCY_SYMBOLS_COUNT += 1

    return CURRENCY_SYMBOLS_COUNT

def IS_THERE_SPECIAL_SYMBOLS( MESSAGE ):
    SPECIAL_SYMBOLS_COUNT = 0
    pattern = r'[^a-zA-Z0-9$.,€£\s]'
    MATCHES = re.findall(pattern, MESSAGE)
    for match in MATCHES:
        SPECIAL_SYMBOLS_COUNT += 1

    return SPECIAL_SYMBOLS_COUNT

def IS_THERE_SPECIAL_WORDS( MESSAGE ):
    SPECIAL_WORDS_COUNT = 0
    WORDS = MESSAGE.split()
    SPECIALWORDS = ['MONEY', 'FREE', 'URGENT', 'WINNER', 'ERROR', 'HERE', 'DOLLAR', 'GUARANTEED', 'CLICKHERE','ACCOUNT', 'VERIFICATION', 'IPHONE', 'SURPRISE', 'ONECAT', 'LIFETIME', 'ACTNOW', 'RICH', 'OFFER','BONUS', 'PRIZE', 'SALE', 'DEAL', 'CASH', 'SAVINGS', 'LIMITED', 'OPPORTUNITY', 'WIN','CONGRATULATIONS', 'HURRY', 'EXCLUSIVE', 'DISCOUNT', 'PROMOTION', 'SPECIAL', 'AMAZING', 'REWARD','BANK', 'TRANSFER', 'FOR', 'YOU', 'GIFT', 'SUCCESS', 'NOW', 'TODAY', 'BEST', 'INVEST', 'SECURE','HOT', 'LIMITEDTIME', 'EARN', 'FAST', 'SIMPLE', 'SECRET', 'PROFIT', 'VIP', 'INSIDER', 'FIRST','FINAL', 'SAVE', 'PROVEN', 'HASSLEFREE', 'BESTSELLER', 'FAVORITE', 'RISKFREE']
    pattern = r'\b(?:' + '|'.join(SPECIALWORDS) + r')\b'
    for word in WORDS:
        if re.findall(pattern, word):
            SPECIAL_WORDS_COUNT+=1

    return SPECIAL_WORDS_COUNT

def UPPERCASE_LETTERS_PERCENTAGE( MESSAGE ):
    if len(MESSAGE)> 0 :
        WORDS = MESSAGE.split()
        UPPERCASE_COUNT = 0
        for word in WORDS:
            for letter in word:
                if letter.isupper():
                    UPPERCASE_COUNT+=1

        UPPERCASE_PERCENTAGE = round( UPPERCASE_COUNT/len(MESSAGE) * 100  ,  2)
        return UPPERCASE_PERCENTAGE
    else:
        return 0

def BIG_WORDS_PERCENTAGE( MESSAGE ):
    BIG_WORDS_COUNT = 0
    WORDS = MESSAGE.split()
    if len(WORDS) > 0:
        for word in WORDS:
            if word.isupper():
                BIG_WORDS_COUNT+=1

        BIG_WORDS_PERCENTAGE = round( BIG_WORDS_COUNT/len(WORDS) * 100  ,  2)
        return BIG_WORDS_PERCENTAGE
    else:
        return 0


def SYSTEM_RECOGNITION_HEADER( MESSAGE ):

    TESTSAMPLE = []

    CLRANED_MESSAGE = PREPROCESSING_DATA(MESSAGE)

    PHONE_NUMBERS = IS_THERE_PHONE_NUMBERS(CLRANED_MESSAGE)
    TESTSAMPLE.append(PHONE_NUMBERS)

    LINKS = IS_THERE_LINKS(CLRANED_MESSAGE)
    TESTSAMPLE.append(LINKS)

    CURRANCY_SYMBOLS = IS_THERE_CURRANCY_SYMBOLS(CLRANED_MESSAGE)
    TESTSAMPLE.append(CURRANCY_SYMBOLS)

    SPECIAL_SYMBOLS = IS_THERE_SPECIAL_SYMBOLS(CLRANED_MESSAGE)
    TESTSAMPLE.append(SPECIAL_SYMBOLS)

    SPECIAL_WORDS = IS_THERE_SPECIAL_WORDS(CLRANED_MESSAGE)
    TESTSAMPLE.append(SPECIAL_WORDS)

    UPPERCASE_LETTERS = UPPERCASE_LETTERS_PERCENTAGE(CLRANED_MESSAGE)
    TESTSAMPLE.append(UPPERCASE_LETTERS)

    BIG_WORDS = BIG_WORDS_PERCENTAGE(CLRANED_MESSAGE)
    TESTSAMPLE.append(BIG_WORDS)

    TESTSAMPLE_HELPER = np.array(TESTSAMPLE).reshape(1, -1)
    return TESTSAMPLE_HELPER


def LABEL_TRANSFER( NUMBER ):
    SHARSLABEL = " "
    if (NUMBER == 0):
        SHARSLABEL = " HAM "
    elif (NUMBER == 1):
        SHARSLABEL = " SPAM "

    return SHARSLABEL


print("  WELCOM HERO ! \n "
      "  THIS IS ABDELJALIL's SYSTME RECOGNITION PROJECT FOR CLASSIFING EMAILS EITHERS HAM EMAILS OR SPAMS !"
      "  ALL CODE EXPLANITION IN README FILE "
      "  HOPE ENJOY TO USE IT : \n\n")
init()
TRAININGLABELESARRAY = GET_LABELES()
TRAININGFEATURESARRAY = GET_FEATURES()
FINAL_MODEL = MODEL_GENERATOR(TRAININGFEATURESARRAY, TRAININGLABELESARRAY)

USERCHOICE = 1
while (USERCHOICE == 1 ):

    CLIENT_EMAIL_MESSAGE = input("ENTER OR PAST YOUR EMAIL BODY HEROOOOOOOO : ")
    TESTSAMPLE = SYSTEM_RECOGNITION_HEADER( CLIENT_EMAIL_MESSAGE )
    TESTLABEL = FINAL_MODEL.predict(TESTSAMPLE)

    if TESTLABEL == 0 : print(Fore.BLUE + f"THIS MESSAGE IS A {LABEL_TRANSFER(TESTLABEL)} EMAIL \n " + Style.RESET_ALL)
    else : print(Fore.RED + f"THIS MESSAGE IS A {LABEL_TRANSFER(TESTLABEL)} EMAIL \n " + Style.RESET_ALL)

    CLOSEINGKEY = input("ANOTHER TRY ? TYPE 'ENTER' FOR CONTENUE | TYPE EXIT/exit  FOR EXIT THE SYSTEM INTERFACE : ")
    if CLOSEINGKEY == 'EXIT' or CLOSEINGKEY == 'exit' : break

print("\n\n SEEYEA BROTHER | TAKE CARE OF UR SELF !!! ")

