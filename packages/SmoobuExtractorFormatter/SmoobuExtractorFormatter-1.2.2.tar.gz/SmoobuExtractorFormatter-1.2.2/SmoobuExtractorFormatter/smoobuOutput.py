import os
import pandas as pd
import numpy as np
import sys
import traceback

names = { "name_menage" : "frais_menage",
"name_taxe" : "taxe_sejour",
"name_commission" : "commission",
"name_gestion" : "frais_gestion",
"name_linge" : "supp_linge_serviettes",
"name_addon" : "addon" }




TAB_INITIAL = {
	"type": "type",

	"created-at": "created-at",

	"modifiedAt": "modifiedAt",

	"channel": "channel",

	"guest-name": "guest-name",

	"firstname": "firstname",

	"lastname": "lastname",

	"email": "email",

	"phone": "phone",

	"adults": "adults",

	"children": "children",

	"check-in": "check-in",

	"check-out": "check-out",

	"price": "total-price",

	"guest-app-url": "guest-app-url",

	"is-blocked-booking": "is-blocked-booking",

	"guestId": "guest_id",

	"apartment_id": "apartment_id",

	"apartment_name": "apartment-name",

	"plateforme_id": "plateforme_id",

	"plateforme_name": "plateforme-name",

	"client": "client",

	"statut": "statut",

	"nuits": "nuits",

	"reservation-id": "reservation-id",

	"reservation-num": "reservation-num",

	"created_at": "created_at",

	"modified_at": "modified_at",
    
    'Taxe de séjour ( seulement si réservation via Booking.com ) <-> addon' : names['name_sejour'],

	"basePrice": "basePrice",

	"Commission <-> commission": "commission",

	"frais de ménage <-> channelCustom": names['name_menage'],

	"taxe de séjour <-> channelCustom": names['name_taxe'],

	"Cleaning fee <-> cleaningFee": names['name_menage'],

	"Airbnb Collected Tax <-> channelCustom": names['name_taxe'],
    
    'Check Out 14H <-> addon' : names['name_addon'],

	"TVA <-> channelCustom": "TVA",

	"frais de linge de lit <-> channelCustom": "frais_linge_lit",

	"Frais de nettoyage <-> cleaningFee": names['name_menage'],

	"Taxe de séjour <-> addon": names['name_taxe'],
 
	"[Sejournez à Troyes] Frais de gestion <-> addon": "frais_gestion", # à voir
    
    'Frais de gestion <-> addon' : "frais_gestion_2",

	"PASS_THROUGH_PET_FEE <-> channelCustom": "supp_animaux",

}


SEJOUR_MOTS = ["Séjour", "Résidence", "Visite", "Escale", "Vacances", "Voyage","Tourisme"]
SEJOUR_WORDS = ["Stay", "Sojourn", "Visit", "Residence", "Stopover", "Vacation", "Trip",'Tourism']

SEJOUR = SEJOUR_MOTS + SEJOUR_WORDS


MENAGE_MOTS = ["ménage","nettoyage"]
MENAGE_WORDS = ["cleaning"]

MENAGE = MENAGE_MOTS + MENAGE_WORDS





class SmoobuOutput:
    
    """
    Changes the format of the excel (or the json) given by the scrapping tool
    of the Smoobu application 
    
    :param file: the excel file or the json file to be changed
    :type file: str
    
    :param table: the table of the columns/keys to be changed
    :type table: dict

    """
    
    def __init__(self,file):
        self.file = file
        
        
    def format_allBookings(self,path_output = "./",table = TAB_INITIAL, names = names, to_drop = []):
        
        def len_value(x):
                return len(x)

        def one_value(x):
            if isinstance(x, list) and len(x) > 0 :
                return x[0]
            else :
                return None
            
        def sum_value(x):
            
            sum = 0
            if isinstance(x, list) and len(x) > 0 :
                for i in range(len(x)):
                    if x[i] != None and (isinstance(x[i], float) or isinstance(x[i], int)):
                        sum += x[i]
            
            return sum
                        
        
        
        file_name,file_extension = os.path.splitext(self.file)
    

        if(file_extension == ".xlsx"):
                
                bookings = pd.read_excel(self.file)
                #bookings.rename(columns = table, inplace = True)
                
                columns = bookings.columns 
                dict = {}

                bookings.rename(columns = table, inplace = True)
                
                del bookings[names['name_addon']]
                
                columns_exist = {}
                columns_notexist = []
                
                for name in table.keys():
                    if name in columns :
                        columns_exist[name] = True
                    else :
                        columns_exist[name] = False
                        columns_notexist.append(name)
                
                
                number_menage = bookings[names['name_menage']].shape[0]
                number_sejour = bookings[names['name_taxe']].shape[0]
                
                # merging every columns into one : baseprice
                
                bookings['basePrice_'] = bookings[names['name_baseprice']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                
                lens1 = bookings['basePrice_'].apply(len_value)
                
                del bookings[names['name_baseprice']]
                
                bookings['basePrice_'] = bookings['basePrice_'].apply(one_value)
                
                
                # merging every columns into one : frais de menage
                
                bookings['frais_menage_'] = bookings[names['name_menage']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                

                lens = bookings['frais_menage_'].apply(len_value)
                
                del bookings[names['name_menage']]
                
                bookings['frais_menage_'] = bookings['frais_menage_'].apply(one_value)
                
                
                # merging every columns into one : taxe de sejour
            
            
                print(bookings[names['name_taxe']].head())
                bookings['taxe_sejour_'] = bookings[names['name_taxe']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                lens2 = bookings['taxe_sejour_'].apply(len_value)
                
                del bookings[names['name_taxe']]
                
                bookings['taxe_sejour_'] = bookings['taxe_sejour_'].apply(one_value)
                
                # merge every column into one : commission 
                
                bookings['commission_'] = bookings[names['name_commission']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)

                lens3 = bookings['commission_'].apply(len_value)
                
                del bookings[names['name_commission']]
                
                bookings['commission_'] = bookings['commission_'].apply(one_value)
                
                # merge evry column into one : gestion 
                
                bookings['frais_gestion_'] = bookings[names['name_gestion']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                
                lens4 = bookings['frais_gestion_'].apply(len_value)
                
                del bookings[names['name_gestion']]
                
                bookings['frais_gestion_'] = bookings['frais_gestion_'].apply(one_value)
                
                # merge every column into one : frais_electricite
                
                bookings['frais_electricite_'] = bookings[names['name_electricite']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                
                lens5 = bookings['frais_electricite_'].apply(len_value)
                
                del bookings[names['name_electricite']]
                
                bookings['frais_electricite_'] = bookings['frais_electricite_'].apply(one_value)
                
                
                # sum every column into one : linge de lit et serviettes 
                
                bookings['frais_linge_serviettes_'] = bookings[names['name_linge']].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                
                lens6 = bookings['frais_linge_serviettes_'].apply(len_value)
                
                del bookings[names['name_linge']]
                
                bookings['frais_linge_serviettes_'] = bookings['frais_linge_serviettes_'].apply(sum_value)
                
                # delete all the cancel columns 
                
                # Find keys containing "cancel" and store them in the list
                keys_to_delete = []
                for key in bookings.keys():
                    if 'cancel' in key:
                        keys_to_delete.append(key)

                # Delete the keys from the dictionary
                for key in keys_to_delete:
                    del bookings[key]
                    
                # delete the columns that are on the paramater 
                
                for key in to_drop:
                    if key in bookings.keys():
                        del bookings[key]


                # New column
                payé_voyageur_calculated = ['basePrice_', 'frais_menage_', 'taxe_sejour_', 'frais_gestion_', 'frais_linge_serviettes_','frais_electricite_']
                bookings['payé-voyageur_calculated'] = 0.0

                for frais in payé_voyageur_calculated:
                    if frais in bookings.columns:
                        bookings['payé-voyageur_calculated'] += bookings[frais].fillna(0.0)

                try:
                    bookings['delta'] = (abs(bookings['total-price'] - bookings['payé-voyageur_calculated']))
                    bookings = bookings.round(2)  # to avoid rounding errors
                    bookings['Added-Taxes'] = np.where(bookings['taxe_sejour_'] == bookings['delta'], True, False)
                    bookings['Equals-Prices'] = np.where(bookings['total-price'] == bookings['payé-voyageur_calculated'], True, False)

                    del bookings['delta']
                except KeyError as error:
                    _, _, tb = sys.exc_info()
                    line_number = traceback.extract_tb(tb)[-1][1]       
                    print(f"Error occurred on line {line_number}: {error}")
                    print("\nThere is a problem with the columns: total-price and payé-voyageur_calculated\n")

                # newly formated data to excel
                bookings = bookings.round(2)
                bookings.to_excel( path_output +"/Smoobu_"+file_name.split("/")[-1] + ".xlsx", index = False)
                
                print("\nSmoobu file created \n")
                for file in os.listdir():
                    if file == "Smoobu_"+file_name.split("/")[-1] + ".xlsx":
                        file_path = os.path.join(os.getcwd(), file)
                        print("File path:", file_path)
                        break
                return bookings
    
        
        else:
                print("Le fichier n'est pas au format excel")
                return None
            







    
        
        