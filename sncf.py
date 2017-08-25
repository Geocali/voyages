class sncf:
    def __init__(self, driver):
        self.driver = driver

    def charger_page(self, city_start, city_stop, time_go, date_go):

        time_back = ""
        date_back = ""
        url = "https://www.voyages-sncf.com/billet-train?PASSENGER_1_CARD_BIRTH_DATE=&\
_AGENCY=VSC&\
DESTINATION_CITY_CHECK=&\
PASSENGER_2_CARD_NUMBER=&\
PASSENGER_1FID_NUM_BEGIN=&\
OUTWARD_DATE=" + date_go + "&\
TRAVEL_TYPE=A&\
ORIGIN_CITY=" + city_start + "&\
OUTWARD_SCHEDULE_TYPE=DEPARTURE_FROM&\
_LANG=fr&PASSENGER_2_FID_PROG=&\
PASSENGER_1_CARD=WEEKE&\
ORIGIN_CITY_RR_CODE=&\
INWARD_TIME=" + time_back + "&\
ORIGIN_CITY_CHECK=&\
CODE_PROMO_2=&\
INWARD_DATE=" + date_back + "&\
PASSENGER_2_CARD=NONE&\
DESTINATION_CITY=" + city_stop + "&\
PASSENGER_1=ADULT&\
PASSENGER_2=ADULT&\
COMFORT_CLASS=2&\
OUTWARD_TIME=" + time_go + "&\
DISTRIBUTED_COUNTRY=FR&\
DESTINATION_CITY_RR_CODE=&\
SOURCE=VSD&\
PASSENGER_1_CARD_NUMBER=&\
PASSENGER_1_FID_PROG=&\
PASSENGER_2FID_NUM_BEGIN=&\
CODE_PROMO_1=&\
PASSENGER_2_CARD_BIRTH_DATE="

        # on charge la page
        page = self.driver.get(url)

        # on clique sur le bouton qui lance la recherche
        xpath = "/html/body/div[3]/div[3]/div/div/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]/form/fieldset[3]/input[1]"
        elem = self.driver.find_element_by_xpath(xpath)
        elem.click()

        # on attend les résultats de la recherche
        delay = 100 # seconds
        xpath_header = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/proposal-header/div"
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath_header)))
            print("Page is ready!")
        except:
            print("Loading took too much time!")

        # On clique sur le bouton "voir plus" pour voir tous les trains suivants
        xpath_more = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/div[3]/div/button[1]"
        #elem = driver.find_element_by_class_name("btn-link next-btn")
        elem = self.driver.find_element_by_xpath(xpath_more)
        elem.click()

    def lire_ligne(row):
        self.driver.delete_all_cookies()

        # on vérifie qu'on n'est pas arrivé au bout
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]"
        try:
            elem = self.driver.find_element_by_xpath(xpath)
        except:
            raise Exception('My error!')

        # gare de départ
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[1]/div/div[1]/div[2]/span"
        try:
            elem = self.driver.find_element_by_xpath(xpath)
        except:
            return None
        gare_depart = elem.text

        # gare d'arrivée
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[1]/div/div[2]/div[2]/span"
        elem = self.driver.find_element_by_xpath(xpath)
        gare_arrivee = elem.text

        # date départ
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[1]/div/div[1]/div[1]/time"
        elem = self.driver.find_element_by_xpath(xpath)
        date_depart = elem.get_attribute("datetime")

        # date arrivée
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[1]/div/div[2]/div[1]/time"
        elem = self.driver.find_element_by_xpath(xpath)
        date_arrivee = elem.get_attribute("datetime")

        # nombre de correspondances
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[1]/div/div[3]/div[2]"
        elem = self.driver.find_element_by_xpath(xpath)
        txt_corr = elem.text.split("\n")[1].split(" ")[0]
        if txt_corr == "direct":
            nb_corr = 0
        else:
            nb_corr = int(txt_corr)

        # durée
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[1]/div/div[3]/div[3]/time"
        elem = self.driver.find_element_by_xpath(xpath)
        duree_min = int(elem.text.split("h")[0]) * 60 + int(elem.text.split("h")[1])

        # prix billet non modifiable
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[3]/div[1]/div/button/span"
        try:
            elem = self.driver.find_element_by_xpath(xpath)
            prix_non_modif = int(elem.text.split(",")[0]) + int(elem.text.split(",")[1][:-1])
        except:
            prix_non_modif = None

        # prix billet modifiable sous conditions
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[3]/div[2]/div/button/span"
        try:
            elem = self.driver.find_element_by_xpath(xpath)
            prix_modif_cond = int(elem.text.split(",")[0]) + float(elem.text.split(",")[1][:-1])/100
        except:
            prix_modif_cond = None

        # prix billet modifiable
        xpath = "/html/body/div[2]/div[3]/main/section/vsd-app[1]/div/div[1]/div/search-results-page/div/main/div[2]/div[2]/div/div/vsd-proposals-block/div/div[2]/div/vsd-proposal-list/div/div/div[" + str(row) + "]/div[1]/div/div[3]/div[3]/div/button/span"
        try:
            elem = self.driver.find_element_by_xpath(xpath)
            prix_modif = int(elem.text.split(",")[0]) + float(elem.text.split(",")[1][:-1])/100
        except:
            prix_modif = None

        c = ["gare_depart", "gare_arrivee", "date_depart", "date_arrivee", "nb_corr", "duree_min", "prix_non_modif", "prix_modif_cond", "prix_modif"]
        d = [gare_depart, gare_arrivee, date_depart, date_arrivee, nb_corr, duree_min, prix_non_modif, prix_modif_cond, prix_modif]
        df = pd.DataFrame(data=d, index=c)
        df.transpose()

        return df

    def lire_page():
        dfs = []
        row = 1
        continuer = True

        while continuer:
            try:
                df_price = get_row(self.driver, row)
                if df_price is not None:
                    dfs.append(df_price.transpose())
                else:
                    a = 1
                    #print("None")
                #print(row)
            except:
                continuer = False
                #print("arf")

            row += 1

        df_prices = pd.concat(dfs)

        # on enregistre la date à laquelle on a fait la mesure
        time = str(datetime.datetime.now()).split(".")[0]
        df_prices['time_checked']=pd.Series(time)

        return df_prices
