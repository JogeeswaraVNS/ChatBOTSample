# import json
# import numpy as np
# import random
# import nltk
# import pickle
# from nltk.stem import PorterStemmer
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.optimizers import SGD
# import difflib

# # Initialize the stemmer
# stemmer = PorterStemmer()

# # Load the data
# with open("intents (1).json") as file:
#     data = json.load(file)

# with open("data.pickle", "rb") as f:
#     words, labels, training, output = pickle.load(f)

# # Convert training and output to numpy arrays
# training = np.array(training)
# output = np.array(output)

# # Define the Keras model
# model = Sequential()
# model.add(Dense(8, input_shape=(len(training[0]),), activation='relu'))  # Input layer
# model.add(Dense(8, activation='relu'))  # Hidden layer
# model.add(Dense(len(output[0]), activation='softmax'))  # Output layer

# # Compile the model
# sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
# model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

# # Load a previously trained model or train the model if needed
# try:
#     model.load_weights("chatbot_model.h5")
# except:
#     # Train the model
#     model.fit(training, output, epochs=200, batch_size=8)
#     model.save("chatbot_model.h5")

# # Helper functions
# def bag_of_words(s, words):
#     bag = [0 for _ in range(len(words))]

#     s_words = nltk.word_tokenize(s)
#     s_words = [stemmer.stem(word.lower()) for word in s_words]

#     for se in s_words:
#         for i, w in enumerate(words):
#             if w == se:
#                 bag[i] = 1

#     return np.array(bag)

# def words_to_list(s):
#     a = []
#     ns = ""
#     s = s + " " 
#     for i in range(len(s)):
#         if s[i] == " ":
#             a.append(ns)
#             ns = ""
#         else:
#             ns = ns + s[i]
#     a = list(set(a))
#     return a

# def json_to_dictionary(data):
#     dictionary = []
#     fil_dict = []
#     vocabulary = []
#     for i in data["intents"]:
#         for pattern in i["patterns"]:
#             vocabulary.append(pattern.lower())
#     for i in vocabulary:
#         dictionary.append(words_to_list(i))
#     for i in range(len(dictionary)):
#         for word in dictionary[i]:
#             fil_dict.append(word)
#     return list(set(fil_dict))

# # Build vocabulary for chatbot
# chatbot_vocabulary = json_to_dictionary(data)

# # Spelling correction function
# def word_checker(s):
#     correct_string = ""
#     for word in s.casefold().split():
#         if word not in chatbot_vocabulary:
#             suggestion = difflib.get_close_matches(word, chatbot_vocabulary)
#             if len(suggestion) == 0:
#                 pass
#             else:
#                 correct_string = correct_string + " " + str(suggestion[0])
#         else:
#             correct_string = correct_string + " " + str(word)
#     return correct_string.strip()

# # Function to get response from the chatbot
# def get_response(msg):
#     inp = msg
#     if inp.lower() == "quit" or inp == None:
#         return "Goodbye!"

#     inp_x = word_checker(inp)
#     results = model.predict(np.array([bag_of_words(inp_x, words)]))[0]
#     results_index = np.argmax(results)
#     tag = labels[results_index]

#     if results[results_index] >= 0.9:
#         for tg in data["intents"]:
#             if tg['tag'] == tag:
#                 responses = tg['responses']
#                 return random.choice(responses)
#     else:
#         return "Sorry, I don't know how to answer that yet."

# # Example usage
# message = "Hello"
# response = get_response(message)
# print(response)

# components=[
#     "Valrack: 12u",
#     "Dlink: 2 mtr patch cards",
#     "Dlink: mount box",
#     "Dlink 1 mtr patch cards",
#     "Dlink single face plates",
#     "Dlink i/os",
#     "Dlink patch panel",
#     "Sudhakar 1\" pvc",
#     "Standard 1\" casing and caping",
#     "Tp link tl pe 160s poe injector",
#     "Dlink cable box cat6 305 meters",
#     "Jntu biometric devices repairs",
#     "1 inc pvc casing and caping",
#     "1 inch pvc pipes",
#     "Cisco cbs350-48t$gin switch",
#     "Wall rack proteckwall mount rack 12u",
#     "Wallrack 15 u",
#     "Wallrack 24 u",
#     "Special fiberoptic lead",
#     "Sc to sc patchcord",
#     "Fiber termination box",
#     "Jumbojoint encoser",
#     "16 port poe switch",
#     "1 gig sfp module",
#     "Brother tze-221(9mm)",
#     "Brother tze-231(12mm)",
#     "Thermal paste",
#     "Usb to ps2",
#     "Brush",
#     "9v battery",
#     "T type connector",
#     "Cable ties 200mm",
#     "Cable ties 300mm",
#     "Fluke /modular crimper",
#     "Screwdriver 18\"",
#     "Screwdriver 12\"",
#     "Iron hammer",
#     "Cutting player",
#     "Lan tester",
#     "D-link network cable tester",
#     "Screw driver",
#     "Multi media 3mtrs fiber patch cords",
#     "Tools bag for technician",
#     "Tools bag for electrician",
#     "Coaxial cable wire cutter and stripper tool",
#     "Optotech @fiber optical power meter",
#     "Single mode lc-sc fiber patch cord 5mtr patch cords",
#     "Optical fiber patch cord",
#     "Usb to rj45 cisco console adapter",
#     "Mother boards",
#     "Cable ties",
#     "Bosch 620w air blower",
#     "Hikvision5mp ir fixed bullet cameras",
#     "Pole mount brackets",
#     "25 mm hdpe pipe",
#     "Plastic junction boxes",
#     "Network cat6 cable",
#     "Outdoor cable",
#     "Cable ties 200 mm",
#     "Cable ties 350mm",
#     "Tb hdd seagate",
#     "Sadc dc-kit",
#     "Duct pipe",
#     "Optical fiber6f for flats",
#     "Jaint encloser",
#     "Spicing fiber optic lead",
#     "Trenching work",
#     "Fiber termination box",
#     "Sc to sc patch cords",
#     "Zero db connectors",
#     "Gig sfp modules",
#     "Nic cord",
#     "Tp link poe injectors",
#     "Cordless impact drill machines",
#     "Hss 6mm bit",
#     "Hss 8mm bit",
#     "Drill bit set",
#     "Hss dril bitset",
#     "Cutting player",
#     "Power stage hammer",
#     "Screw driver",
#     "Wire sripper",
#     "9w batteries",
#     "Spring 30m",
#     "Hammerdrillbit",
#     "Screwdriver",
#     "Tester 813",
#     "Electrician screwwdriver set",
#     "Psp scisiors",
#     "Wilson scisiors",
#     "Cartini scisiors",
#     "Pahal nylon bag",
#     "Lan tester with wire tester",
#     "Basic 2.4 a dual cell charger",
#     "Tek pc repair screwdriver set",
#     "Envirio infinite 9v 800mah rechargeble batteries",
#     "Tp link usb to ctype rj 45 wired adaper",
#     "32 gb pendrive",
#     "64 gb pendrive",
#     "Curtain cloth",
#     "Powder coated ms rod with brackets",
#     "Stiching charges",
#     "Transport and fitting charges",
#     "D link 24 port fully loaded patch panel",
#     "D link cat6 cable box",
#     "Cat 6 i/o s",
#     "Rj 45 jacks box",
#     "Cmos batteries",
#     "Insulation tapes",
#     "250 mm tag pkts",
#     "Networking rack cooling fans",
#     "Pest controll for the month of feb 2022",
#     "Cisco 48 t 4g switches",
#     "Cisco cbs 550 48 t 4g in",
#     "Cisco cbs 350 24t 4g -in",
#     "Cisco cb350240t 4y-in",
#     "Flock and keys fore home",
#     "25mm *1.5 mm pvc pipes",
#     "25 mm pvc bends",
#     "Injector poe tp link",
#     "D-link cat6 cable( bundle of 305 mtrs )",
#     "Pest control for the month of march 2023",
#     "Tp link c80 !900router",
#     "Interner acces services for wired and wireless for theb period of 01-01-2023 to 31-03-2023",
#     "Internet accces for 2000mbps for the period of 01/04/2023",
#     "Hik vision 5 mp cameras",
#     "Hik vision 8 port switch poe",
#     "Cisco c100 non poe switch",
#     "Cisco 24 port non non poe switch",
#     "D link cat cable",
#     "D link patch panel",
#     "1 mtr patch cords",
#     "Rj 45 connectors",
#     "12 u valrack",
#     "1 \" pvc pipes",
#     "Standard nail clamps",
#     "1\" flexible bundles",
#     "300 mm cable ties",
#     "1\" metal screws",
#     "Cable ties",
#     "D-link Cat 6 cable box",
#     "D-link Patch panel",
#     "I/O s D-link",
#     "D-link back box",
#     "Single face plates",
#     "Vall rack",
#     "2 mtr patch cords",
#     "24 port PoE switch",
#     "1\" metal screws box",
#     "2\" casing and caping",
#     "Cable ties",
#     "Cable ties small",
#     "Aruba access point AP 515",
#     "Hik vision 5mp cameras",
#     "Hikvision 4MP cameras",
#     "Hikvision PoE switch",
#     "Dlink Cat 6 cable box",
#     "Sudhakar 1\" PVC pipes",
#     "Standard pole mount brackets",
#     "Diginode mini signage player",
#     "Digi cloud application",
#     "Total 18% inclusive",
#     "Hikvision 5 MP camera",
#     "Hikvion 4 MP Bullet cameras",
#     "Hikvion 8 port Poe switch",
#     "Dlink outdoor cable box",
#     "TP link C80 1900 Router",
#     "Cisco CBS 350-48T-4G -48 port NON PoE switch",
#     "25 mm casing and caping",
#     "! inch PVC pipe",
#     "32mm flexible bundle",
#     "25mm C clamps",
#     "200 mm Cable ties",
#     "PVC 4 way box",
#     "Screw box",
#     "15 U rack floor mount with accessories",
#     "Hikvision 2mp IP bullet camera",
#     "Hikvision NVR -16 channel",
#     "Seagate skywalk HDD 6 TB",
#     "Henson junction box",
#     "Ap-CBL-SERU console adapter cable",
#     "Service charges",
#     "Aruba access points",
#     "AP mounting brackets",
#     "Cisco CBS 35024P-4G",
#     "D link UPT Cat6 box",
#     "Dlink 24 port Patch panel",
#     "D link Cat 6 I/O s",
#     "D link single face plates",
#     "D link backboxes",
#     "D link 5 mtr patch cords",
#     "D-link 1 mtr patch cords",
#     "D link RJ45 jack box",
#     "Sudhakar 1\" PVC pipes",
#     "Sudhakar 2\" PVC pipes",
#     "2\" Clamps",
#     "D link 1 mtr patch cords",
#     "Pest control for the month of May 2023",
#     "PoE injectors",
#     "Pest control for the month of June 2023",
#     "Signage player with Diginode software",
#     "Digi Cloud application",
#     "Lan cord Broadcom",
#     "2 cote tractor immersion paint for CNCC room",
#     "12 V 100 AH SMF Quanta batteries",
#     "Pest control for the month of July",
#     "Cisco 24 port non PoE switch",
#     "Vallrack 12 U with cable manager",
#     "D link 2 mtr patch cords",
#     "D link 1 mtr patchcords",
#     "D link back box",
#     "D link I/O s",
#     "D link Patch panel",
#     "Sudhakar 1 inch PVC pipes",
#     "1 inch casing and caping",
#     "TP link 1605 PoE injector",
#     "D Link cable box UTP cable",
#     "Numeric 1 LVA UPS",
#     "Spike buster",
#     "HP -Aruba access points",
#     "AP mount bracket",
#     "24 port fully loaded",
#     "1.25 GIG modules",
#     "SC to SC patch cords",
#     "SC to LC patch cords",
#     "LC to LC patch cords",
#     "T box",
#     "HP 88 toner cartridge",
#     "24F OFC fiber pullings",
#     "PVC pipe",
#     "Labour charges",
#     "OFC joints",
#     "64 GB pen drives",
#     "CMOS batteries",
#     "Diginode player",
#     "DigiCloud applications",
#     "Sandisk 32 GB pen drives",
# ]


# vendors=[
# 'M/S NGSS Pvt. Ltd.,Hyderabad',
#     'M/S secure data products limitted',
#     'M/S Blue blossoms technogies (p) ltd',
#     'M/S Blue blossoms Technologies (p) ltd',
#     'M/S Novoture Elecrical &digital systems (p) ltd',
#     'M/S Digital D solutions','M/S patel Engineering',
#     'M/S Nisha computers','M/S Nisha computers','M/S Veda',
#     'M/S Sri Gaesh enterprises','M/S Data Systems',
#     'M/S Sri sai sttionary &computers','M/S Spectrum',
#     'M/S Amezan','M/S Amezan','M/S MFS Whole sale (P) ltd',
#     'M/S jubilee Traders','Hanutech solutins','Isudo technolgies',
#     'M/S Cobra Cables','M/S Global technologies',
#     'M/S Exel Pest control','M/S Exel Pest control',
#     'M/S Exel Pest control','M/S Shree om enterprises',
#     'M/S Poineer E labs limited ISP','M/S Excel Pest control',
#     'MS Blue blossom technologies','M/S blue blosssom technologies',
#     'M/S VSE Computers','M/S Ram engineering and controls',
#     'M/S Digital D solutions','M/S excel pest control',
#     'M/S Blue blossoms technolgies','M/S Blue blossoms technolgies',
#     'M/S Excel pest controll','M/S Raghavenra Enterprises',
#     'M/S Raghavendra Enterprises',
#     'M/S Tools and spares corporation','M/S Sangvi brothers',
#     'M/S SS enterprises','M/S Mek Corporation',
#     'M/S Vijetha Super market P Ltd','M/S Pahal International',
#     'M/S Vian Enterprises','M/s Appario retail P Ltd',
#     'M/S Tavakkal E commerce','Appario retail P ltd',
#     'Appario Retail P ltd','Received from Central Stores',
#     'M/S Poinneer E labs','M/S Excel pest control',
#     'M/S Trans dyne Engineering P ltd',
#     'M/S Next Generation simple solutions P ltd',
#     'M/S Excel pest control','M/S blue blossoms technologies P ltd',
#     'M/S Blue blossoms technologies Pltd','M/S link &Line',
#     'Sree Rama sales corporation Pvt ltd',
#     'M/S Cloudance tech P ltd','M/S Mouritech',
#     'excel pest controll','AWL IT tech p Ltd',
#     'M/S Poineer Elabs Limited','M/S Poineer E labs Limited ISP',
#     'M/S NGSS P Ltd','M/S NGSS P ltd','M/S NGSS (P) ltd',
#     'M/S NGSS (P) ltd','M/S Diginode signage solutions',
#     'M/S Microcare computers  P ltd','M/S Mouritech',
#     'M/S Mouritech','M/S Mouritech','M/S NGSS P ltd',
#     'M /S ecel pest control','NGSSS P ltd','Excel pest control',
#     'M/S Diginode','M/S Blue blossoms technologies p ltd',
#     'Mohammad moosa paint contractor','Sreenidhi power systems',
#     'Excel Pest control','M/S NGSS P LTd','NGHSS P Ltd',
#     'Excel pest control','AWL Tech P ltd',
#     'received from central stores','M/S AWL tech  pvt ltd',
#     'M/S Cache peripherals (p) ltd','SS fiber services',
#     'M/S Blue blossoms technologioes (p) ltd','SS fiber services',
#     'M/S Received from central stores','M/S  Ecel pest Control',
#     'M/S AWL tech p ltd','SS Fiber services',
#     'M/S Diginode Signage solutions',
#     'M/S Sunrise sysytems and solutions','NGSS (P) ltd',
#     'NGSS (P) ltd','Diginode signage solutions','Exel pest control',
#     'SS fiber services','NGSS (p) ltd',
#     'Kompu serve  surya kiran SD Road secenderabad ,',
#     'KEITH electronics  (P) Ltd3 Flat no401 yallareddyguda Ameerpet HYderabad',
#     'M/S Dharmashastra Services  khammam',
#     'M/S Sree rama sales india P ltd hyd',
#     'M/S Sreenidhi power sysytems,Tirumalagerry secenderabad',
#     'M/S excel pest control','M/S Rajdeep Engineering pvt ltd',
#     'M/S Excel pest control','NGSS P Ltd',
#     'M/S Ram enginneering Controls'
# ]


# def get_random_vendor():
#     return random.choice(vendors)


# # get_random_vendor()


# def generate_random_quantity(min_quantity=1, max_quantity=100):
#     """Generate a random quantity purchased between min_quantity and max_quantity."""
#     return random.randint(min_quantity, max_quantity)

# # generate_random_quantity()



# def generate_random_price(min_price=500, max_price=50000):
#     """Generate a random purchased price between min_price and max_price."""
#     return round(random.uniform(min_price, max_price))


# # generate_random_price()



# import random
# from datetime import datetime, timedelta

# def random_date(start, end):
#     """Generate a random date between two datetime objects."""
#     return start + timedelta(days=random.randint(0, (end - start).days))

# start_date = datetime(2002, 7, 12)
# end_date = datetime(2024, 12, 31)


# generated_date = random_date(start_date, end_date)

# # generated_date.strftime("%Y-%m-%d")




# def generate_random_stock_entry_number_numeric(length=8):
#     """Generate a random numeric stock entry number of specified length."""
#     random_number = ''.join(random.choices(string.digits, k=length))
#     return f"STK-{random_number}"

# # generate_random_stock_entry_number_numeric()


# import string
# def generate_random_invoice_number_numeric(length=8):
#     """Generate a random numeric invoice number of specified length."""
#     random_number = ''.join(random.choices(string.digits, k=length))
#     return f"INV-{random_number}"


# generate_random_invoice_number_numeric()

# with app.app_context():
#     for i in components:
#         generated_date = random_date(start_date, end_date)
#         row=PurchasedComponents(get_random_vendor(),i,generate_random_quantity(),generate_random_price(),generated_date.strftime("%Y-%m-%d"),generate_random_stock_entry_number_numeric(),generate_random_invoice_number_numeric())
#         db.session.add(row)
#         db.session.commit()
