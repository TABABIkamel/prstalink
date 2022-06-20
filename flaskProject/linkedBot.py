import time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import lxml


class linkedBot:

    def __init__(self, username, password, mongoConf):
        self.username = username
        self.password = password
        self.mongoConf = mongoConf
        self.browser = webdriver.Remote('http://chrome:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

    def login_linkedin(self):
        browser = self.browser
        browser.get("https://www.linkedin.com/")
        self.random_sleep()
        email = browser.find_element_by_id("session_key")
        password = browser.find_element_by_id("session_password")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        self.random_sleep()
        password.send_keys(self.password)
        self.random_sleep()
        password.send_keys(Keys.RETURN)
        time.sleep(10)

    def google_search(self, googling):
        browser = self.browser
        browser.get("https://www.google.com/")
        search = browser.find_element_by_name("q")
        search.clear()
        self.random_sleep()
        search.send_keys("site:linkedin.com/in/ " + self.add_And(googling))
        self.random_sleep()
        search.send_keys(Keys.RETURN)
        google_list = self.bf_search()
        profiles = self.linkedin_search(google_list)
        browser.quit()

    def linkedin_search(self, google_list):
        profiles = []
        mongo = self.mongoConf
        match = 10000000
        browser = self.browser
        for link in google_list:
            try:
                browser.get(link)
                time.sleep(6)
                src = self.browser.page_source
                soup = BeautifulSoup(src, 'lxml')
                self.humain_scrapping()
                name = None
                about = None
                try:
                    try:
                        imgAll = soup.find('div', {'class': 'pv-top-card__non-self-photo-wrapper ml0'})
                        img = imgAll.find_all('img')[0].attrs['src']
                    except:
                        pass
                    try:
                        name_div = soup.find('div', {'class': 'mt2 relative'})
                    except:
                        name_div = None

                    try:
                        name = name_div.find('h1').get_text().strip()
                    except:
                        name = None
                    try:
                        loc = soup.find('span',
                                        {
                                            'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
                    except:
                        loc = None
                    try:
                        profile_title = soup.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
                    except:
                        profile_title = None
                    try:
                        connection = None
                        connection = soup.find('ul',
                                               {'class': 'pv-top-card--list pv-top-card--list-bullet display-flex pb1'})
                        connection = connection.find_all('li')
                        connection = connection[0].find('span', {'class': 't-bold'}).get_text().strip()
                    except:
                        connection = None
                    info = []
                    info.append(img)
                    info.append(link)
                    info.append(name)
                    info.append(loc)
                    info.append(profile_title)
                    info.append(connection)
                    experiences = []
                    experience = []
                    educations = []
                    education = []
                    profiles = []
                except:
                    pass
                exp_section = soup.find_all('section', {'class', 'artdeco-card ember-view relative break-words pb3 mt2'})

                for exp in exp_section:
                    try:
                        div_one = exp.find('div', {'class', 'pvs-header__container'})

                        div_two = div_one.find('div', {'class', 'pvs-header__top-container--no-stack'})

                        div_three = div_two.find('div', {'class', 'pvs-header__left-container--stack'})

                        div_four = div_three.find('div', {'class', 'pvs-header__title-container'})

                        h2_five = div_four.find('h2', {'class', 'pvs-header__title text-heading-large'})

                        titre_section = h2_five.find('span').get_text().strip();
                    except:
                        titre_section = None
                    if (titre_section == 'Experience' or titre_section == 'Expérience'):
                        try:
                            exp_div = exp.find('div', {'class', 'pvs-list__outer-container'})
                            exp_ul = exp_div.find('ul', {'class', 'pvs-list ph5 display-flex flex-row flex-wrap'})
                            exps_li = exp_ul.find_all('li', {'class',
                                                             'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
                        except:
                            exps_li = None
                        for exp_li in exps_li:
                            try:
                                div_inside_li = exp_li.find('div', {'class',
                                                                    'pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested'})
                                div_inside = div_inside_li.find('div')

                                a_inside_div = div_inside.find('a',
                                                               {'class', 'optional-action-target-wrapper display-flex'})

                                div_inside_a = a_inside_div.find('div',
                                                                 {'class', 'ivm-image-view-model pvs-entity__image'})

                                div_inside = div_inside_a.find('div', {'class',
                                                                       'ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex'})

                                img_all = div_inside.find('img')  # [0].attrs['src']

                                image_experience = img_all.attrs['src']
                            except:
                                # div_inside_li = None
                                image_experience = None
                            try:
                                div_all_experience_sauf_img = div_inside_li.find('div', {'class',
                                                                                         'display-flex flex-column full-width align-self-center'})
                            except:
                                div_all_experience_sauf_img = None
                            try:
                                div_inside = div_all_experience_sauf_img.find('div', {'class',
                                                                                      'display-flex flex-row justify-space-between'})
                            except:
                                div_inside = None
                            try:
                                div_inside_global = div_inside.find('div',
                                                                    {'class', 'display-flex flex-column full-width'})
                            except:
                                div_inside_global = None
                            try:
                                div_inside = div_inside_global.find('div', {'class', 'display-flex align-items-center'})
                            except:
                                div_inside = None
                            try:
                                span_inside = div_inside.find('span', {'class', 'mr1 t-bold'})
                            except:
                                span_inside = None
                            try:
                                span_title_exp = span_inside.find('span')
                            except:
                                span_title_exp = None

                            try:
                                title_exp = span_title_exp.get_text().strip()
                            except:
                                title_exp = None
                            # end title experience
                            try:
                                exp_span_name_societe_exp = div_inside_global.find('span', {'class', 't-14 t-normal'})
                            except:
                                exp_span_name_societe_exp = None
                            try:
                                name_societe_exp = exp_span_name_societe_exp.find('span').get_text().strip();
                            except:
                                name_societe_exp = None
                            try:
                                exp_spans = div_inside_global.find_all('span',
                                                                       {'class', 't-14 t-normal t-black--light'})
                            except:
                                exp_spans = None
                            try:
                                date_debut_exp = exp_spans[0].find('span').get_text().strip();
                            except:
                                date_debut_exp = None
                            try:
                                location_exp = exp_spans[1].find('span').get_text().strip();
                            except:
                                location_exp = None
                            experience.append(image_experience)
                            experience.append(title_exp)
                            experience.append(name_societe_exp)
                            experience.append(date_debut_exp)
                            experience.append(location_exp)
                            experiences.append(experience)
                            experience = []
                    elif titre_section == 'Education' or titre_section == 'Formation':
                        try:
                            exp_div = exp.find('div', {'class', 'pvs-list__outer-container'})
                        except:
                            exp_div = None
                        try:
                            exp_ul = exp_div.find('ul', {'class', 'pvs-list ph5 display-flex flex-row flex-wrap'})
                        except:
                            exp_ul = None
                        try:
                            exps_li = exp_ul.find_all('li', {'class',
                                                             'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
                        except:
                            exps_li = None
                        for exp_li in exps_li:
                            try:
                                div_inside_li = exp_li.find('div', {'class',
                                                                    'pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested'})
                            except:
                                div_inside_li = None
                            try:
                                div_inside = div_inside_li.find('div')
                            except:
                                div_inside = None
                            try:
                                a_inside_div = div_inside.find('a',
                                                               {'class', 'optional-action-target-wrapper display-flex'})
                            except:
                                a_inside_div = None
                            try:
                                div_inside_a = a_inside_div.find('div',
                                                                 {'class', 'ivm-image-view-model pvs-entity__image'})
                            except:
                                div_inside_a = None
                            try:
                                div_inside = div_inside_a.find('div', {'class',
                                                                       'ivm-view-attr__img-wrapper ivm-view-attr__img-wrapper--use-img-tag display-flex'})
                            except:
                                div_inside = None
                            try:
                                img_all = div_inside.find('img')  # [0].attrs['src']
                            except:
                                img_all = None
                            try:
                                image_ecole = img_all.attrs['src']
                            except:
                                image_ecole = None
                            try:
                                div_all_experience_sauf_img = div_inside_li.find('div', {'class',
                                                                                         'display-flex flex-column full-width align-self-center'})
                            except:
                                div_all_experience_sauf_img = None
                            try:
                                div_inside = div_all_experience_sauf_img.find('div', {'class',
                                                                                      'display-flex flex-row justify-space-between'})
                            except:
                                div_inside = None
                            try:
                                div_inside_global = div_inside.find('a', {'class',
                                                                          'optional-action-target-wrapper display-flex flex-column full-width'})
                            except:
                                div_inside_global = None
                            try:
                                div_inside = div_inside_global.find('div', {'class', 'display-flex align-items-center'})
                            except:
                                div_inside = None
                            try:
                                span_inside = div_inside.find('span', {'class', 'mr1 hoverable-link-text t-bold'})
                            except:
                                span_inside = None
                            try:
                                span_title_educ = span_inside.find('span')
                            except:
                                span_title_educ = None
                            try:
                                nom_ecole = span_title_educ.get_text().strip()
                            except:
                                nom_ecole = None
                            try:
                                type_diplome_span = div_inside_global.find('span', {'class', 't-14 t-normal'})
                                type_diplome = type_diplome_span.find('span').get_text().strip()
                            except:
                                type_diplome = None
                            try:
                                durre_education = div_inside_global.find('span',
                                                                         {'class',
                                                                          't-14 t-normal t-black--light'}).find(
                                    'span').get_text().strip()
                            except:
                                durre_education = None
                            education.append(image_ecole)
                            education.append(nom_ecole)
                            education.append(type_diplome)
                            education.append(durre_education)
                            educations.append(education)
                            education = []
                    elif (titre_section == 'About' or titre_section == 'Infos'):
                        try:
                            about_div = exp.find('div', {'class', 'display-flex ph5 pv3'})
                            about_div_inside = about_div.find('div', {'class', 'display-flex full-width'})
                            inside = about_div_inside.find('div', {'class',
                                                                   'pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center'})
                            about = inside.find('div', {'class',
                                                        'inline-show-more-text inline-show-more-text--is-collapsed'}).find(
                                'span').get_text().strip()
                        except:
                            about = None
                mongo.db.profiles.insert_one(
                    {'imgProfile': img, 'link': link, 'name': name, 'location': loc, 'profile_title': profile_title,
                     'about': about,
                     'experience': experiences,
                     'education': educations,
                     'match': match})
                experiences = []
                educations = []
                about = None
                match = match - 0.000001
            except:
                pass
        return profiles

    def random_scrolling(self):
        for x in range(1, random.randint(1, 4)):
            for i in range(0, random.randint(500, 900)):
                self.browser.execute_script("window.scrollTo(0," + str(i) + ");")
                time.sleep(random.uniform(0.00001, 0.00000005))
            for x in range(0, random.randint(500, 1000)):
                self.browser.execute_script("window.scrollBy(0,-1 );")
                time.sleep(random.uniform(0.00001, 0.00000005))
        self.random_sleep()

    def scrolldown(self):
        for i in range(0, random.randint(500, 900)):
            self.browser.execute_script("window.scrollTo(0," + str(i) + ");")
            time.sleep(random.uniform(0.00001, 0.00000005))

    def humain_scrapping(self):
        random.choice([self.random_sleep(), self.random_scrolling()])

    def random_sleep(self):
        time.sleep(random.randint(1, 5))

    def add_And(self, chaine):
        tmp = chaine.split()
        fin = ""
        for tmp1 in tmp:
            tmp1 = tmp1 + " AND"
            fin = fin + " " + tmp1
        return fin

    def bf_search(self):
        mongo = self.mongoConf
        # 'https://www.linkedin.com/in/sihem-aouadi-671801159/',
        # return ['https://www.linkedin.com/in/sihem-aouadi-671801159/',
        #         'https://wwww.linkedin.com/in/zohra-daly-70201513a/',
        #     'https://www.linkedin.com/in/ali-zammel/'
        #     ,'https://www.linkedin.com/in/raouf-rhimi-15a466223/'
        #     ,'https://www.linkedin.com/in/motaz-marzouki/',
        #         'https://www.linkedin.com/in/aicha-sassi-68a3494a',
        #         'https://www.linkedin.com/in/yosri-abdedayem-893936168',
        #         'https://www.linkedin.com/in/aymen-sassi-397651114',
        #         'https://www.linkedin.com/in/wiem-souei-93005573',
        #         'https://www.linkedin.com/in/oumaima-ktayfi',
        #         'https://www.linkedin.com/in/ayoub-chebbi',
        #         'https://www.linkedin.com/in/chaouki-jaziri-4654161a4',
        #         'https://www.linkedin.com/in/amira-naimi-3304b495',
        #         'https://www.linkedin.com/in/ahmed-laamiri-76948361',
        #         'https://www.linkedin.com/in/ragheb-zidi-913b87193',
        #         'https://www.linkedin.com/in/nourchene-ben-ammar'
        #         ]
        #### debut valid code
        pavTab = []
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        profilesID: list[str] = []
        pav = soup.find_all('div', {'class': 'yuRUbf'})
        pavTab.append(pav)
        time.sleep(10)
        for pavi in pav:
            self.random_sleep()
            link = pavi.find('a')
            userId = link.get('href')
            user = str(userId)
            self.random_sleep()
            x = user.replace(user[0:10], 'https://www')
            if user.__contains__('linkedin'):
                f = open('test.csv', 'a')
                writer = csv.writer(f, delimiter=';')
                profilesID.append(x)
                writer.writerow([x])
                mongo.db.urlprofiles.insert_one({'link': x})

        try:
            suivant = soup.find('a', {'id': 'pnnext'})

            textSuivant = suivant.get_text().strip()

        except:
            return profilesID
        while suivant is not None:
            try:
                textSuivant = suivant.get_text().strip()

                self.browser.find_element_by_link_text(textSuivant).click()
                src = self.browser.page_source
                soup = BeautifulSoup(src, 'lxml')
                self.random_sleep()
                pav = soup.find_all('div', {'class': 'yuRUbf'})
                self.humain_scrapping()

                pavTab.append(pav)
                time.sleep(10)
                for pavi in pav:
                    self.random_sleep()
                    link = pavi.find('a')
                    userId = link.get('href')
                    user = str(userId)
                    self.random_sleep()

                    x = user.replace(user[0:10], 'https://www')

                    if user.__contains__('linkedin'):
                        f = open('test.csv', 'a')
                        writer = csv.writer(f, delimiter=';')
                        profilesID.append(x)
                        writer.writerow([x])
                        mongo.db.urlprofiles.insert_one({'link': x})
            except:
                f.close()
                return profilesID
            try:
                suivant = soup.find('a', {'id': 'pnnext'})
                self.random_sleep()
                textSuivant = suivant.get_text().strip()
            except:
                f.close()
                return profilesID
        #### end valid code
