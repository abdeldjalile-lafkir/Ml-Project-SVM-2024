import mysql.connector
import re


Connection_Key = mysql.connector.connect(host="localhost",user="root",password="",database="PROJECTAIdatabase")
SQL = Connection_Key.cursor()



text = (" Lorem Ipsum has $ been the 0676041742 industry's standard dummy text ever since "
        " the 1500s, ! when ¤ an unknown GARANTED printer took %¤ a galley of & PRIZE type and scrambled 0776257396 it "
        " to 213-657-31-21-35 make https://www.kaggle.com/  a type CONGRATULATION  specimen ¤ book. It has CLICK % survived not only  @ ¤ ERROR https://jetbrains.com/ five centuries,"
        " but  FREE also / URGENT the leap into  ) DONT MISS OUT  electronic ½ typesetting,WINNER remaining essentially "
        " containing IPHONE Lorem _ - Ipsum 0657312135 passages, HERE and _  more recently with desktop publishing "
        " GIFT 0664610676 software £ DOLLAR like Aldus £ PageMaker ( including $ versions of https://github.com/ Lorem Ipsum. ")




#REPROSSESING DATA : # Replace all periods and commas ann whitespaces and regularwords with an empty string
def PREPROCESSING_DATA( MESSAGE ):
    pattern = r'\b(?:and|or|a|an|the|is|are|was|were|be|been|being|has|have|had|do|does|did|will|would|shall|should|can|could|may|might|must|of|in|on|at|to|from|with|by|as|for|but|not|so|than|yet|either|neither|nor|although|because|if|unless|while|whereas|whether|though|since|until|before|after|during|over|under|between|among|through|above|below|beside|against|off|up|down|out|into|throughout|around|away|upon|along|across|into|onto|from|toward|underneath|within|beneath|[,])\b'
    CLEANED_DATA = re.sub(pattern, '', MESSAGE)
    CLEANED_DATA = re.sub(r'\s+', ' ', CLEANED_DATA)
    return CLEANED_DATA






# PATTERNS FOR EXTRACT FEATURES :

def IS_THERE_PHONE_NUMBERS(MESSAGE):
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


'''
text2 = PREPROCESSING_DATA(text)
print(f"IS_THERE_PHONE_NUMBERS : {IS_THERE_PHONE_NUMBERS(text2)}")
print(f"IS_THERE_LINKS : {IS_THERE_LINKS(text2)}")
print(f"IS_THERE_CURRANCY_SYMBOLS : {IS_THERE_CURRANCY_SYMBOLS(text2)}")
print(f"IS_THERE_SPECIAL_SYMBOLS :{IS_THERE_SPECIAL_SYMBOLS(text2)}")
print(f"IS_THERE_SPECIAL_WORDS : {IS_THERE_SPECIAL_WORDS(text2)}")
print(f"BIG_WORDS_PERCENTAGE :{BIG_WORDS_PERCENTAGE(text2)}")
print(f"UPPERCASE_LETTES_PERCENTAGE :{UPPERCASE_LETTERS_PERCENTAGE(text2)}")

'''




# TRANSFER DATASET TO NUMERICALE VALUES | EXTRACTE FEATURES !!
SQL.execute(f" SELECT * From FINALEDATASETTABLE ")
SQL_DATASET = SQL.fetchall()
for row in SQL_DATASET:


    if(row[0] == "ham"): LABEL = 0
    elif(row[0] == "spam"): LABEL = 1

    CLEANED_ROW = PREPROCESSING_DATA(row[1])

    PHONE_NUMBERS = IS_THERE_PHONE_NUMBERS(CLEANED_ROW)
    LINKS = IS_THERE_LINKS(CLEANED_ROW)
    CURRANCY_SYMBOLS = IS_THERE_CURRANCY_SYMBOLS(CLEANED_ROW)
    SPECIAL_SYMBOLS = IS_THERE_SPECIAL_SYMBOLS(CLEANED_ROW)
    SPECIAL_WORDS = IS_THERE_SPECIAL_WORDS(CLEANED_ROW)
    UPPERCASE_LETTERS = UPPERCASE_LETTERS_PERCENTAGE(CLEANED_ROW)
    BIG_WORDS = BIG_WORDS_PERCENTAGE(CLEANED_ROW)

    #print(CLEANED_ROW)
    #print(LABEL , PHONE_NUMBERS,LINKS,CURRANCY_SYMBOLS,SPECIAL_SYMBOLS,SPECIAL_WORDS,UPPERCASE_LETTERS,BIG_WORDS)

    #SQL.execute(f"INSERT INTO FNALEDATASETFEATURESTABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({LABEL},{PHONE_NUMBERS},{LINKS},{CURRANCY_SYMBOLS},{SPECIAL_SYMBOLS},{SPECIAL_WORDS},{UPPERCASE_LETTERS},{BIG_WORDS} )")



print("FEATURES ADDED SUCCFULLY !!!!!!") #: 91564 sample
Connection_Key.commit()
SQL.close()
Connection_Key.close()


# TRAINING VALIDATION ANNNNNNNNNNNNNNNNND  TESTING !!
'''
HAMSAMPLES = []
SQL.execute(f" SELECT * From FNALEDATASETFEATURESTABLE WHERE LABEL = 0")
SQL_DATASET = SQL.fetchall()
for row in SQL_DATASET:
    HAMSAMPLES.append(row)
    
print(len(HAMSAMPLES)) #43623 ham sample
i = 0
for hamsample in HAMSAMPLES:
    if( i < 30000 ): #30,000 SAMPLE OF TRAINING DATA
        #SQL.execute(f"INSERT INTO PROJRCTAI_TRAININGDATATABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({hamsample[0]},{hamsample[1]} ,{hamsample[2]},{hamsample[3]},{hamsample[4]},{hamsample[5]},{hamsample[6]},{hamsample[7]})")
        i+=1
    elif( 30000 <= i  < 40000 ): #10,000 SAMPLE OF VALIDATION DATA
        #SQL.execute(f"INSERT INTO PROJRCTAI_VALIDATIONDATATABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({hamsample[0]},{hamsample[1]} ,{hamsample[2]},{hamsample[3]},{hamsample[4]},{hamsample[5]},{hamsample[6]},{hamsample[7]})")
        i += 1
    elif ( 40000 <= i < 40500): #500 SAMPLE OF VALIDATION DATA
        #SQL.execute(f"INSERT INTO PROJRCTAI_TESTINGDATATABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({hamsample[0]},{hamsample[1]} ,{hamsample[2]},{hamsample[3]},{hamsample[4]},{hamsample[5]},{hamsample[6]},{hamsample[7]})")
        i += 1

Connection_Key.commit()
print("HAMSAMPLES SEPARETED SUCCEFULLY ")





SPAMSAMPLES = []
SQL.execute(f" SELECT * From FNALEDATASETFEATURESTABLE WHERE LABEL = 1")
SQL_DATASET = SQL.fetchall()
for row in SQL_DATASET:
    SPAMSAMPLES.append(row)

print(len(SPAMSAMPLES))  #44521 spam sample
i = 0
for spamsample in SPAMSAMPLES:
    if( i < 30000 ): #30,000 SAMPLE OF TRAINING DATA
        #SQL.execute(f"INSERT INTO PROJRCTAI_TRAININGDATATABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({spamsample[0]},{spamsample[1]} ,{spamsample[2]},{spamsample[3]},{spamsample[4]},{spamsample[5]},{spamsample[6]},{spamsample[7]})")
        i+=1
    elif( 30000 <= i  < 40000 ): #10,000 SAMPLE OF VALIDATION DATA
        #SQL.execute(f"INSERT INTO PROJRCTAI_VALIDATIONDATATABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({spamsample[0]},{spamsample[1]} ,{spamsample[2]},{spamsample[3]},{spamsample[4]},{spamsample[5]},{spamsample[6]},{spamsample[7]})")
        i += 1
    elif ( 40000 <= i < 40500): #500 SAMPLE OF VALIDATION DATA
        #SQL.execute(f"INSERT INTO PROJRCTAI_TESTINGDATATABLE (LABEL, PHONE_NUMBERS_COUNT, LINKS_COUNT, CURRANCY_SYMBOLS_COUNT, SPECIAL_SYMBOLS_COUNT, SPECIAL_WORDS_COUNT, UPPERCASE_LETTERS_PERCENTAGE, BIG_WORDS_PERCENTAGE) VALUES ({spamsample[0]},{spamsample[1]} ,{spamsample[2]},{spamsample[3]},{spamsample[4]},{spamsample[5]},{spamsample[6]},{spamsample[7]})")
        i += 1

Connection_Key.commit()
print("SPAMSAMPLES SEPARETED SUCCEFULLY ")
'''














'''
# For hard margin SVM
svm_classifier_hard_margin = SVC(kernel='linear', C=np.inf)
svm_classifier_hard_margin.fit(X_train, y_train)

# For soft margin SVM (adjust the value of C as needed)
svm_classifier_soft_margin = SVC(kernel='linear', C=1.0)  # Example C value
svm_classifier_soft_margin.fit(X_train, y_train)



# For Linear Kernel
svm_classifier_linear = SVC(kernel='linear')

# For Polynomial Kernel
svm_classifier_poly = SVC(kernel='poly', degree=3)  # Example degree value

# For RBF Kernel
svm_classifier_rbf = SVC(kernel='rbf', gamma=0.1)  # Example gamma value

# For Sigmoid Kernel
svm_classifier_sigmoid = SVC(kernel='sigmoid', gamma=0.1, coef0=0.0)  # Example gamma and coef0 values
'''