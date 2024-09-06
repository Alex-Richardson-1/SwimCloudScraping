from bs4 import BeautifulSoup
import requests
import csv

# 2024 Guys https://www.swimcloud.com/recruiting/rankings/?page=
# 2024 Women https://www.swimcloud.com/recruiting/rankings/2024/F/?page=
# 2025 Guys https://www.swimcloud.com/recruiting/rankings/2025/M/?page=
# 2025 Women https://www.swimcloud.com/recruiting/rankings/2025/F/?page=

def main():
    closeOnly=True
    notDone=True
    pageNum=20

    #Opening the export file
    file=open("2025GuyRecruitsNearby.csv","w",encoding="utf-8",newline='')
    writer=csv.writer(file)
    
    #Creating the header
    writer.writerow(["Swimmer Name","HomeTown","SwimCloud Ranking"])
    count=0

    #Looping through all of the pages
    while(notDone):
        swimcloud=requests.get("https://www.swimcloud.com/recruiting/rankings/2025/M/?page=" + str(pageNum))
        pageNum=pageNum+1


        #Scraping swimcloud
        soup=BeautifulSoup(swimcloud.text, "html.parser")
        names=soup.findAll("a",attrs={"class":"u-text-semi"})
        places=soup.findAll("td",attrs={"class":"hidden-xs u-color-mute"})
        rankings=soup.findAll("td",attrs={"class":"u-text-end"})
        
        
        print("Page" , pageNum-1)
        sum=0
        for name, place, rank in zip(names,places, rankings):
            #Checking if they are within the range
            if(float(rank.text)>30.0):
                if(float(rank.text)>32.0):
                    file.close()
                    quit()
                else:
                    if(closeOnly):
                        #Checking if they are close to VA if so then writing their best 5 events according to swimcloud with the time
                        if((", VA" in place.text or ", MD" in place.text or ", NC" in place.text or ", PA" in place.text)):
                            swimmer="https://www.swimcloud.com"+name.attrs['href']+"/powerindex/"
                            eachSwimmer=requests.get(swimmer)
                            soup2=soup=BeautifulSoup(eachSwimmer.text, "html.parser")

                            ovr=soup.findAll("td",attrs={"class":"u-text-truncate u-text-semi"})
                            time=soup.findAll("td",attrs={"class":"c-table-clean__time u-text-semi"})
                            print(swimmer)
                            if(len(ovr)>5):
                                writer.writerow([name.text.strip(), place.text,rank.text.strip()])
                                writer.writerow(["Event","Time"])

                                writer.writerow([ovr[0].text,time[0].text])
                                writer.writerow([ovr[1].text,time[1].text])  
                                writer.writerow([ovr[2].text,time[2].text])  
                                writer.writerow([ovr[3].text,time[3].text])  
                                writer.writerow([ovr[4].text,time[4].text])    
                                writer.writerow([])
                         
                    #If we do not care about distance to VA then anyone between the points writing their best 5 events          
                    else:
                            swimmer="https://www.swimcloud.com"+name.attrs['href']+"/powerindex/"
                            eachSwimmer=requests.get(swimmer)
                            soup2=soup=BeautifulSoup(eachSwimmer.text, "html.parser")

                            ovr=soup.findAll("td",attrs={"class":"u-text-truncate u-text-semi"})
                            time=soup.findAll("td",attrs={"class":"c-table-clean__time u-text-semi"})
                            print(swimmer)
                            if(len(ovr)>5):
                                writer.writerow([name.text.strip(), place.text,rank.text.strip()])
                                writer.writerow(["Event","Time"])

                                writer.writerow([ovr[0].text,time[0].text])
                                writer.writerow([ovr[1].text,time[1].text])  
                                writer.writerow([ovr[2].text,time[2].text])  
                                writer.writerow([ovr[3].text,time[3].text])  
                                writer.writerow([ovr[4].text,time[4].text])    
                                writer.writerow([])
                    


main()
