import requests  
from bs4 import BeautifulSoup
import pandas as pd
  
  
def get_soup(url: str): 
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser')  
    return soup 
 
base_url = "https://www.hdfcbank.com/personal/pay/cards/credit-cards" 
soup = get_soup(base_url) 

df_rows = []
card_parents = soup.find_all("div", class_="cardparent") 
for card_parent in card_parents:
    card_name = card_parent.find('span', class_ = "card-name").text 
    print(card_name)

    href = card_parent.find("a",{'title': "KNOW MORE"}) or card_parent.find("a",{'title': "Know more"})\
                    or card_parent.find("a",{'title': "Know More"})\
                    or card_parent.find("a",{'title': "know more"})
    if not href:
        continue
    knowmore_url = "https://hdfcbank.com" + href['href']
    soup_2 = get_soup(knowmore_url)
    inner_content = soup_2.find("div", attrs={"class" : "inner-content col-lg-8 col-sm-8 right-section"}) 
    rewardpoints_info = "" 
    for li in inner_content.find_all("li"): 
        if "150" in li.text: 
            rewardpoints_info = li.text 
            break 
    if not rewardpoints_info:
        for para in inner_content.find_all("p"): 
            if "150" in para.text: 
                rewardpoints_info = para.text 
                break 
    #print(rewardpoints_info)
    renewal_offer = soup_2.find_all("div", attrs = {"class" : "row content-body"}) 
    renewal_membership = "" 
    for offer in renewal_offer: 
        paragraph = offer.find("p") 
        if paragraph and "renewal membership fee" in paragraph.text: 
            renewal_membership = paragraph.text 
            break 
    #print(renewal_membership) 
    fees_url = knowmore_url + "/fees-and-charges" 
    soup3 = get_soup(fees_url) 
    # print(fees_url) 
    fees = soup3.find_all("div", attrs = {"class" : "row content-body"}) 
    #print(fees) 
    card_fees = "" 
    for li in fees: 
        lis = li.find("li") 
        # print(lis) 
        if lis and "Membership Fee" in lis.text: 
            card_fees = lis.text 
            break 
    if not card_fees:
        for li in fees: 
            para = li.find("p") 
            # print(lis) 
            if para and "Membership Fee" in para.text: 
                card_fees = para.text 
                break 
    #print(card_fees) 
    #  
    mbenefit = soup_2.find_all("div", attrs = {"class" : "row content-body"}) 
    # print(mbenefit) 
    milestone_benefit = "" 
    for li in mbenefit: 
        ben = li.find("li") 
        # print(ben) 
        if ben and "worth" in ben.text: 
            milestone_benefit = ben.text 
            break 
    #print(milestone_benefit) 
    lounge = soup_2.find_all("div", attrs = {"class" : "row content-body"}) 
    # print(lounge) 
    lounge_access = "" 
    for li in lounge: 
        lon = li.find("p") 
        if lon and 'omplimentary' in lon.text: 
            lounge_access = lon.text 
            break 
    #print(lounge_access)
    df_rows.append([card_name, card_fees, lounge_access, rewardpoints_info, milestone_benefit, renewal_membership])

df = pd.DataFrame(df_rows, columns=['card_name', 'card_fees', 'lounge_access', 'rewardpoints_info', 'milestone_benefit', 'renewal_membership'])
df.to_csv('~/Downloads/hdfc_creditcard.csv')