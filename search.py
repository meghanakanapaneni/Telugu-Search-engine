from math import sqrt 
import operator 
import functools 
import unicodedata 
 
_WORD_MIN_LENGTH = 3 
_STOP_WORDS = frozenset([ 
'nee', 'kuda', 'ne', 'kooda', 'ee', 'ah', 'oka', 'tho',  
'lo', 'lu', 'ra', 'ni', 'em', 'nuvvu', 'nenu','ga', 
'ika','ki','mee', 'aa', 'orey', 'thanu',  'oo', 'ila', 'inka', 
'ani','adi','di','pai','kaani', 'emi', 'ye', 'ee', 'ko', 
'arey', 'osey','pora','pove', 'era','me','nuv', 'o', 'naa',  
'le', 'na', 'oh', 'ne','akaraku','akarlo','poo','era','inkenti', 
'naa','la','laa','rani','raja','vah','va','rara','puski','undi','ney']) 
 
def word_split(text): 
 
    word_list = [] 
    wcurrent = [] 
    windex = None 
    position=1 
    for i, c in enumerate(text): 
        if c.isalnum(): 
            wcurrent.append(c) 
            windex = i 
       
        elif wcurrent: 
            word = ''.join(wcurrent) 
            word_list.append((position, word)) 
            wcurrent = [] 
            position=position+1 
 
    if wcurrent: 
        word = ''.join(wcurrent) 
        word_list.append((position, word)) 
        position=position+1 
    return word_list 
 
def words_cleanup(words): 
    cleaned_words = [] 
    for index, word in words: 
        if len(word) < _WORD_MIN_LENGTH or word in _STOP_WORDS: 
            continue 
        cleaned_words.append((index, word)) 
    return cleaned_words 
 
def words_normalize(words): 
    normalized_words = [] 
    for index, word in words: 
        wnormalized = word.lower() 
        normalized_words.append((index, wnormalized)) 
    return normalized_words 
   
def reverse(s):  
    if len(s) == 0:  
        return s  
    else:  
        return reverse(s[1:]) + s[0]  
           
def words_stemming(words): 
 
    stemmed_words = [] 
    word1='' 
    word2='' 
    for index, word in words: 
        word1=reverse(word) 
        if(word1[:2]=='ul' or word1[:2]=='id' or word1[:2]=='un' or word1[:2]=='in' or word1[:2]=='ag'): 
            word2=word1[2:] 
            if len(word2) < _WORD_MIN_LENGTH : 
                stemmed_words.append((index,word)) 
            elif (reverse(word2) not in stemmed_words): 
                stemmed_words.append((index,reverse( word2))) 
        else: 
            if (word not in stemmed_words): 
                stemmed_words.append((index,word)) 
     
    return stemmed_words 
 
def word_index(text): 
    
    words = word_split(text) 
    words = words_normalize(words) 
    words = words_cleanup(words) 
    words = words_stemming(words) 
    return words 
 
def inverted_index(text): 
 
    inverted = {} 
 
    for index, word in word_index(text): 
        locations = inverted.setdefault(word, []) 
        locations.append(index) 
 
    return inverted 
 
def inverted_index_add(inverted, doc_id, doc_index): 
    for word, locations in doc_index.items(): 
        indices = inverted.setdefault(word, {}) 
        indices[doc_id] = locations 
    return inverted 
 
def search(inverted, query): 
 
    words = [word for _, word in word_index(query) if word in inverted] 
    results = [set(inverted[word].keys()) for word in words] 
    return functools.reduce(lambda x, y: x & y, results) if results else [] 
     
def cosine_similarity(query,document): 
    list1=[] 
    query_dic={} 
    doc_dic={} 
    sum1=0 
    words=word_index(query) 
    words1=word_index(document) 
    for i,j in words: 
        list1.append(j) 
    for i in list1: 
        k=list1.count(i) 
        if(i not in query_dic.keys()): 
            query_dic[i]=k 
    list1=[]   
    for i,j in words1: 
        list1.append(j) 
    for i in list1: 
        k=list1.count(i) 
        if(i not in doc_dic.keys()): 
            doc_dic[i]=k 
    sum_squ_que=0 
    sum_squ_doc=0 
    for i,j in query_dic.items(): 
        sum_squ_que+=j*j 
        for p,q in doc_dic.items(): 
            if(i==p): 
                sum1=sum1+(j*q) 
                break 
    for p,q in doc_dic.items(): 
        sum_squ_doc+=q*q 
    if(sqrt(sum_squ_que)*sqrt(sum_squ_doc) == 0 ): 
        return 0 
    return round(sum1/(sqrt(sum_squ_que)*sqrt(sum_squ_doc)),2) 
             
 
if __name__ == '__main__': 
    doc1 = """ 
Kanulu neevi kanneeru naadi Hrudayam needi savvadi naadi Suvaasan needi sughandam naadi Sneha bandhammaatram mana iddaridi. nee navvu badhanu kooda navvinchaali,nee jeevitham chavuni kooda brathikinchali,nee vijayaporatanni choosi,otami thana parajayanni oppukovali,nee prema enthati virodhannaina tholaginchali,ee anna manasulo velugula eppatiki brathiki undaali. Pagalaite raatri kuda autundi. 
Niraasha vaddu manaki manchi jarugutundi. Denikaina samayam padutundi. Antavaraku manaki opika avasaram vundi. 
""" 
    doc2 = """ 
Oka raithu undevaadu.Athanikoka asamaanamaina baathu undedhi.Prati roju ah baathu oka andamaina merise bangaaru guddu pettedhi.Danni ammukoni raithu dhanavantudu ayyadu.Athyasha tho oka roju ah baathu ni kosi anni gudlu teeskovaali anukuntaadu.Nuvvu em kaavalukuntunav 
Nenu MBBS chadivi, Police Ayyi,Manchi software company lo, lawyerga work chesi pedda peddha building lu kattukuntu collector ga job chesukunta orey nijam chepu ra nuvu balakrishna fan kada 
""" 
    doc3 = """ 
Samudram pedda peddha alaloo reputhundhi,aa alalooo manalanu bhayapeduthaayii, kaani Prema nemmadhiga udi sunaami reputhundhi,aa sunaami manasulni kalipee varakoo Nidhurapoohu. Laxmi mee inta nartinchaga Santhosham paalai pongaga Deepa kaantulu veluguneeyaga Anandamga jarupukondi Diwali panduga  
""" 
    doc4 = """ 
Apude suryodayam ayyindi. Ika Radha kudaa lechi college ki ready avuthundi. Radha 20 yella telugu inti ammayi. Chaala lakshanam ga untundi. Thanaki amma, nanna oka thammudu unnaru. Valla nanna oka mamulu kuragaayala dukanam unna madhyatharagathi vyapari. Roju roju chese vyaparam tho kastha kastha kuuda betti pillalni chadivinchukuntunnadu. Amma peddhaga chaduvukoledu kaani loka gyanam ekkuva. Thalli thandrulu appudappudu sambandalu chudatam modalu kuda pettesaru. Andaru paduchu pilla laaga thanu kudaa thana pelli gurinchi chaala kalalu kantunnadi Radha.  
""" 
    doc5 = """ 
Interview roju vachesindi. Podhune lechi snanam chesi thondara thondaraga ready ayipoyi bus stop vaipu sagindi. Bus vachindi. Kaani chaala rush ga undi. Kaani tension lo bus ekkesi mothaniki office ki cherindi. Ila oka nela gadichindi. Ika Radha pani roju podhune lechi paper thirageyatam. Ila oka roju chusthundaga oo roju paper lo oka udhyogam gurinchi prakatana vachindi. 
"""     
    doc6 = """ 
Ika mundu chusesariki oka 50 unnaru. Mothaniki okkokari interview ayyi thana peru pilicharu interview ki. Vellindi interview kuda baagane ayindi. Inka andaridhi ayyi vallu results 5 ki announce chesthamu ani chepparu. Appude 3 ayindi. Pottalo akali kaani medhadu manasu mathram udhyoga alochanalu. Ika 4 ayindi. Inka emi cheppatledu. 5 ayindi. Inka ippatlo cheppelaga suchanalu levu. 
""" 
    doc7 = """ 
Chetilo oka paper pattukunnaru. Ika valla company gurinchi okkokaru lectures ivva sagaaru. Ika results cheppe time vachindi. HR paper lo chusthu announce chesthunnadu. 55 lo rendu perlu anukuntu Radha alochanalu. Inthalo oka preu chepparu kaani adi Radha di kaadu. Ika rendo peru Radha chevilo padindhi. Kallalo neelu vachayi. Ika alane kallalo neella tho thirigi bus ekki intiki vachesi amma ni pattukuni edchesindi.  
""" 
    doc8 = """ 
Ika office lo eroju modati roju. Poddhune car 9 ki vachindi ekki, Radha office lo adugu pettindi. Velli HR ni kalisindi. HR oka conference room chupinchi kurchomannadu. Akkada thanatho paatu select ayina Krishna kuda unnadu. Iddaru matladukuntundaga, valla head vachadu. Ika Radha shock tho lechi nilchundi.  
"""     
    doc9 = """ 
Ila oka aaru nelalu gadichindi. Kaani roju roju ki Radha manasulo Sheshu pai prema perigipothundi. Inkoka vaipu Sheshu, Radha, Krishna manchi snehithulu ayipoyaaru. Paiga Radha valla nanna kudaa Radha dabbulu kudabetti, bank loan thisukuni, Kocham peddha shop addeki thisukuni super market laaga pettadu. Paiki kashtapadi vachina vyakthi kanuka, manchi quality ni maintain chesthunnadu.  
""" 
    doc10 = """ 
Appudu Radha aa matalu thattukoleka vallidarini vadilesi intiki vellipoyindi. Sheshu, Krishna phone chesthe lift cheyatam ledu. Poni intiki veldama ante bagodhemo ani velatam ledu. Sare ika somavaram varaku wait cheyalsinde ani wait chesthunadu Sheshu.Kaani Krishna ki manasu urukoleka aadivaram rathri thana daggariki velladu.  
""" 
    doc11 = """ 
Ila oka rendu ellu gadichipoyayi. Radha inka Sheshu ni pattinchukovatamledu. Krishna mathram thanani inka premisthune unnadu. Eppudaina thanaki kudirinantha varaku sahayapaduthuntaadu Radha ki. Sheshu thana girlfriend tho pelli ayipoyindi. Oka papa kuda. Radha vallu kudaa financial ga baagunnaru.  
""" 
    doc12 = """ 
Malli thana bad luck modalaindani anukuni, esari devudini thittaleka intiki bayalu derindhi. Kaani ippudu edurayye pelli chuppulo emi cheppalo thelika, Krishna pai prema ni ela aapukovalo thelika madanapaduthundi. Intiki vachesariki amma, nanna santhoshanni chusi, ika emi cheyaleka sardukupodam anukundi.  
"""     
    doc13 = """ 
Ika ippudu Radha ki em cheyalo ardam kavatam ledu. Amma ni chusthe edo anumanam. Thiduthundi anukunte navvindi paiga tharuvatha antundi asalu em jaruguthundo naaku asalu ardam kavatamledu ani anukundi. Ippudu emi cheyanu? Itu Krishna kuda phone ethatam ledu. Kaani ishtam leni vaadini inka chudatam enduku? Ani badha paduthu kurchundi 
""" 
    doc14 = """ 
Chethilona chethulesukunna chotulona Chooputhoti choopulallukunna darilona Swasaloki swasalallukunna mayalona Anandha varnaala sarigama Samayama, Samayama, Samayama Kadhalake kshanamaa Jathapade yedhalalo madhurima Vadulukoke vinumaa Aa ningi jabillipai Ye neeti jaadunnado 
Ney choodalene appude Ee nela jabillipai Santhosha bhashpalani Choosthu unnane ipude 
""" 
    doc15 = """ 
Kadhile meghalapai Nadiche padhalilaa Merise oo minugurai Vayase aadindhilaa Pedhavitho choosaa Ney kanulatho navvaanugaa Second ko vintha Nuvvu thodunda batte kadha Ee lokamanthaa aagi Manavanke choosina Pattanattu podham Vere lokamlo thelipodham 
Na na na na Na na na na Nuvvante artham nenenaa Na na na na Na na na na Naa gunde shabdham needhena 
""" 
    doc16 = """ 
Undiporaadhey gunde needhele Hathukoraadey gundeke nanne Ayyo ayyo padham Nelapai aaganannadhi Malli malli gaallo Meghamai theluthunnadhi 
Andham ammayi aithey Neela undhaa annattundhe Momaataale vaddhannaaye Adagaalante kaugile Mande yendallo vendi vennelane Mundhe nenepudu choodale Cheekatlo kooda needalaa Neevente nenu undagaa Vere janmantu naake yedhukule Neetho ee nimisham chaalule 
"""     
    doc17 = """ 
Oka ammai undedi, roju chusedi, chusthu navvedi, navvuthu pata paadedi, paaduthu siggu padedi, nenu anukunna prema ani, tharuvatha thelisindi pichhidani. oka intlo kodalu atta godava padutuntaru pakkinti ayana vacchi era me vallu kotladutunte nuv evari pakka nilchuntavu goda pakka ra. ne kallu nemali kallu ne mukku chilaka mukku ne nadaka hamsa nadaka ne palukulu kokila ganam  
""" 
    doc18 = """ 
Entha Jaali Gunde needhi Naa kallu Nagnanga unnayani Prathi rooju Kanneti poralatho kapputhuntavu. prema anedi pamu lantidi paditea aadutundi kadilistea kaatestundi aaaaaaaaa kshanam kosamea andaru eduruchustntaru punnami ratri vastea antea pandagea pandaga kondaru dad avutaru andaru kaaleru kondaru mom avutaru andaru kaaleru kani andaru friends avutaru manalaga 
""" 
    doc19 = """ 
nirmalamaina nee navvu niswarthamaina nee sneham ante naku entho istam nuvvu na eduruga unna lekunna na hrudayamlo eppatiki nilichi untav Bhasha kanna goppadi bhavam Bhavam kanna goppadi abhimanam Abhimanam kanna goppadi aasha Aasha kanna goppadi aanandam Aanandam gaa undali neevu kalakaalam oh! nestam 
""" 
    doc20 = """ 
nalone pongenu narmada neelallo murisina thaamara anthatlo marenu ruthuvulaaa pilla neevalla neetho pongey velluva nelallo eedhina thaarakaa 
bangaru poovulla kaanuka pereley kanchana oh shanthi shanthi oh shanthi naa pranam sarvam neevey le naa swasey neevey dochavey 
cheli nene neevu ayyavey 
"""     
     
    inverted = {} 
    sim_list=[] 
    documents = {'doc1':doc1, 'doc2':doc2,'doc3':doc3, 'doc4':doc4,'doc5':doc5, 'doc6':doc6,'doc7':doc7, 'doc8':doc8,'doc9':doc9, 'doc10':doc10,'doc11':doc11, 'doc12':doc12,'doc13':doc13, 'doc14':doc14,'doc15':doc15, 'doc16':doc16,'doc17':doc17, 'doc18':doc18,'doc19':doc19, 'doc20':doc20} 
    for doc_id, text in documents.items(): 
        doc_index = inverted_index(text) 
        inverted_index_add(inverted, doc_id, doc_index) 
 
    # Print Positional Inverted-Index 
    for word, doc_locations in sorted(inverted.items()): 
        print (word, doc_locations) 
 
    queries = ['radha krishna','amma','sheshu','unnoticed','pedda peddha'] 
    for query in queries: 
        result_docs = search(inverted, query) 
        print ("Search for '%s': %r" % (query, result_docs)) 
        for _, word in word_index(query): 
            def extract_text(doc, index):  
                return documents[doc][index:index+20].replace('\n', ' ') 
        count=0         
        result_dic={} 
        for doc_id,text in sorted(documents.items()): 
            sim=cosine_similarity(query,text) 
            if(sim>0.0): 
                count=count+1 
                result_dic[doc_id]=sim 
        for i,j in sorted(result_dic.iteritems(), reverse=True,  key=lambda (k,v): v): 
           print(str(i) +" score : "+ str(j)) 
        if(count==0): 
            print("No results found") 
         