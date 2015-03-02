LENTA = 'LENTA'
GAZETA = 'GAZETA'

TLINK_TAG = 'TLINK'
TIMEX_TAG = 'TIMEX3'
EVENT_TAG = 'EVENT'


TIMEML_DATE = 'DATE'
TIMEML_TIME = 'TIME'


TLINK_TIME_ATTR = 'relatedToTime'
TLINK_EVENT_ATTR = 'eventInstanceID'
TIMEX_ID_ATTR = 'tid'
EVENT_ID_ATTR = 'eid'


EVENT_TAG_TEMPLATE = '<EVENT aspect="EVENT_ASPECT" tense="EVENT_TENSE" class="OCCURRENCE" eid="EVENTID">WORD</EVENT>'

EVENT_TAG_TEMPLATE_ID = 'EVENTID'
TIMEX_TAG_TEMPLATE_ID = 'TIMEXID'

MAKEINSTANCE_TAG_TEMPLATE = '<MAKEINSTANCE eiid="EVENTID" eventID="EVENTID"/>'
TLINK_TAG_TEMPLATE = '<TLINK eventInstanceID="EVENTID"  relatedToTime="TIMEXID" relType="REL_TYPE"/>'


#####CLASSIFICATOR FEATURES

FEATURE_NA = 'NODATA'
FEATURE_YES = 'Y'
FEATURE_NO = 'N'






###############FEATURES################


TIMEX_TYPE = 'timexType'
TIMEX_VALUE = 'timexValue'

TIMEX_EARLIER_THAN_DCT = 'timexEarlierThanDCT'
TIMEX_PREV_WORD = 'timexPrevWord'


MORPH_POS = 'morphPOS'
MORPH_LEMMA = 'morphLemma'
MORPH_TENSE = 'morphTense'
MORPH_ASPECT = 'morphAspect'
MORPH_BASTARD = 'bastard'

MORPH_DEVERBAL = 'deverbal'


SEM_IS_EVENT = 'semIsEvent'
SEM_IS_ACTIVITY = 'semIsActivity'
SEM_IS_COMMUNICATION = 'semIsCommunication'
SEM_IS_ASPECTUAL = 'semIsAspectual'
SEM_IS_TRANSITIVE = 'isTransitive'

SEM_IS_FIRST_NAME = 'isFirstName'
SEM_IS_GEO = 'isGeo'
SEM_IS_SURNAME = 'isSurname'


DISTANCE_DIR = 'distance_dir'
DISTANCE_ABS = 'distance_abs'
WORDS_BETWEEN = 'numOfWordsBetween'


SAME_DCT = 'isSameDCTRel'
SAME_IMPF = 'isSameImpf'


IS_GOOGLE_BIGRAM = 'isGoogleBigram'

####
OTHER = '9OTHR'

############TIMEX CODES##########
TIMEX_EARLIER = '1E'
TIMEX_LATER = '2L'



#####MORPH POS CODES############
NOUN = 'N'
VERB = 'V'
PARTICIPLE = 'PRT'
BRIEF_PARTICIPLE = 'BR_PRT'
COMP_ADJ = 'ACOMP'
CONVERB = 'CVB'
INFINITIVE = 'INF'


##########MORPH TENSES
TENSE_PAST = 'PST'
TENSE_PRESENT = 'PRS'
TENSE_FUTURE = 'FUT'


ASPECT_PERFECTIVE = u'PFV'
ASPECT_IMPERFECTIVE = u'IPFV'

#####################

IS_BIGRAM_Y = 'Y'
IS_BIGRAM_N = 'N'

####################
DISTANCE_BACK = '1BACK'
DISTANCE_FORWARD = '2FORWARD'
SAME_DCT_Y = 'Y'
SAME_DCT_N = 'N'




CLASS_LINK_Y = '1'
CLASS_LINK_N = '0'

FILENAME = 'filename'



CLASS_LINK = 'link'


ALL_FEATURES = [TIMEX_TYPE,
                TIMEX_PREV_WORD,
                #TIMEX_VALUE,
                
                #TIMEX_EARLIER_THAN_DCT,
                SAME_DCT,
                
                
                
                MORPH_POS,
                MORPH_LEMMA,
                MORPH_TENSE,
                MORPH_BASTARD,
                MORPH_DEVERBAL,
                MORPH_ASPECT,    
                
                
                SEM_IS_EVENT,
                SEM_IS_ACTIVITY,
                SEM_IS_COMMUNICATION,
                SEM_IS_ASPECTUAL,
                SEM_IS_TRANSITIVE,
                
                
                SAME_IMPF,
                #SEM_IS_FIRST_NAME,
                #SEM_IS_SURNAME,
                #SEM_IS_GEO,
                DISTANCE_DIR,
                DISTANCE_ABS,
                WORDS_BETWEEN,
                #IS_GOOGLE_BIGRAM,
                CLASS_LINK,
                #FILENAME
                ]






