import requests
from bs4 import BeautifulSoup

main_link = 'http://www.mirabelkowy.pl/'

dates = ['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']

translator = {'jajko':['jajko','jajka','jajek'],'cukier':['cukier','cukru'],'mąka':['mąka','mąki'],'mleko':['mleko','mleka'],'papryka':['papryka','papryki'],
				'pomidor':['pomidor','pomidory','pomidora'],'ryż':['ryż','ryżu'],'marchewka':['marchewka','marchewki'],'kukurydza':['kukurydza','kukurydzy'],
				'kurczak':['kurczak','kurczaka'],'sól':['sól','soli'],'pieprz':['pieprz','pieprzu']}

#Aby program zadział poprawnie należy w liście poniżej (lista składników, które posiadamy w domu) umieścić tylko nazwy w mianowniku liczby pojedynczej
ingredients = ['sól','pieprz','kukurydza','kurczak','pomidor','']

valid_recipies = []



response = requests.get(main_link)
length_of_main_link = len(main_link)
text_html = response.text
soup = BeautifulSoup(text_html,'html.parser')
links = []
for i in soup.find_all('a'):
	links.append(i.get('href'))
#print(links)

all_links = []

for link in links:
	for date in dates:
		if date in link and len(link) < length_of_main_link + 10 and len(link) > length_of_main_link + 5:
			all_links.append(link)




def match_ingredients(ingredients,link,list_temp):
	temp = 0

	f_response = requests.get(link)
	f_text = f_response.text
	f_soup = BeautifulSoup(f_text,'html.parser')

	f_recipe_ingredients_list = list(f_soup.p.find_all('li'))
	f_replace_list = ['<li><span style="font-size: 85%;"><i>','</i></span></li>']

	for i in range(len(f_recipe_ingredients_list)):
		f_recipe_ingredients_list[i] = str(f_recipe_ingredients_list[i])
		for j in range(len(f_replace_list)):
			if f_replace_list[j] in f_recipe_ingredients_list[i]:
				f_recipe_ingredients_list[i] = f_recipe_ingredients_list[i].replace(f_replace_list[j],'')

	for len1 in range(len(f_recipe_ingredients_list)):
		for len2 in range(len(ingredients)):
			f_temp_list = translator[ingredients[len2]]
			for item in f_temp_list:
				if item in f_recipe_ingredients_list[len1]:
					temp += 1

	if temp > 0.5*len(f_recipe_ingredients_list):
		list_temp.append(link)
		print(link)




for link in all_links:
	#print(link)
	recipe_link = link
	response_1 = requests.get(recipe_link)
	text_response_1 = response_1.text 
	soup_1 = BeautifulSoup(text_response_1,'html.parser')
	recipies = []
	for link_1 in soup_1.find_all('a'):
		if recipe_link in link_1.get('href') and link_1.get('href') not in recipies and recipe_link != link_1.get('href'):
			#recipies.append(link.get('href'))
			match_ingredients(ingredients,link_1.get('href'),valid_recipies)

	