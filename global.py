from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import time
import os

class file_struct(object):
    def __init__(self, driver, filename):
        self.d = driver
        self.f = filename+".tar.gz.part"
        self.fn = filename

class all_files(object):
    files = []
    path = os.getcwd()

    def add(self, driver, f):
        f = file_struct(driver, f)
        self.files.append(f)

    def check(self, fs):
        files = os.listdir(self.path)
        if fs.f not in files:
            global count
            count -= 1
            fs.d.close()
            return True 

    def check_all(self):
        for fs in self.files:
            if self.check(fs):
                self.files.remove(fs)
                print fs.fn + " has completed downloading"
count = 0
def main():

    af = all_files()
    path = os.getcwd()    
    url = "https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=MetaDetail&page=metaDetail&taxon_oid="
    with open(path+"/datasets") as f:
        lines = f.read().splitlines()
        for l in lines:
            old_string = l 
            end = old_string.rfind("=")
            taxon_id = old_string[end+1:]
            if url not in l:
                l = url+taxon_id
            if count > 5:
                time.sleep(300)
            print l
            #imgm(l, taxon_id, af)
            #af.check_all()
    # When we have at least tried all of the links, sleep for 30 minutes to let lingering downloads finish
    #print "Finished dataset download"
    #time.sleep(1800)


def construct_profile():
    try:
        profile = FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir', os.getcwd())
        profile.set_preference('browser.download.manager.showWhenStarting', False)

        MIME = "application/gzip, application/x-gzip, application/x-gunzip, application/gzipped, application/gzip-compressed, application/x-compressed, application/x-compress, gzip/document, application/octet-stream, application/csv, text/csv"

        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", MIME)
    except:
        print "Exception creating profile"

    return profile

def login(driver): 
    try:
        login_xpath = '//*[@title="Your JGI SSO username and NOT your IMG username!"]'
        login = driver.find_element_by_xpath(login_xpath)
        login_name = "kishori@mail.ubc.ca"
        login.send_keys(login_name)

        password_xpath = "/html/body/div[4]/div[3]/div/div[2]/form/table/tbody/tr/td/input[2]"
        password = driver.find_element_by_xpath(password_xpath)
        password_password = "globalstudy1"
        password.send_keys(password_password)

        ok_xpath = "/html/body/div[4]/div[3]/div/div[2]/form/table/tbody/tr/td/input[3]"
        ok = driver.find_element_by_xpath(ok_xpath)
        ok.click()
    except:
        print "Exception occurred in the login stage"
        raise

def download(driver):
    try:
        download_xpath = '//*[@title="Download Data"]'
        download = driver.find_element_by_xpath(download_xpath)
        download.click()
    except:
        print "Exception occurred in the first download stage"
        raise

def download2(driver):
    try:
        #time.sleep(5)
        #second_download = driver.find_element_by_link_text("Download")
        #second_download.click()
        
        # The Download is the first link
        second_download_xpath = "/html/body/div[2]/div[2]/div/ul/li[1]/a"
        download2 = driver.find_element_by_xpath(second_download_xpath)
        download2.click()
    except:
        print "Exception occurred in the second download stage"
        raise

def privacy(driver):
    try:
        #privacy = driver.find_element_by_id("data_usage_policy:okButton")
        #privacy.click()
        second_ok_xpath = "/html/body/div[4]/form/div[4]/div/div/table/tbody/tr/td[1]/input"
        ok2 = driver.find_element_by_xpath(second_ok_xpath)
        ok2.click()
    except:
        try:
            # The Download is the second link
            second_download_xpath = "/html/body/div[2]/div[2]/div/ul/li[2]/a"
            download2 = driver.find_element_by_xpath(second_download_xpath)
            download2.click()

            second_ok_xpath = "/html/body/div[4]/form/div[4]/div/div/table/tbody/tr/td[1]/input"
            ok2 = driver.find_element_by_xpath(second_ok_xpath)
            ok2.click()
        except:
            print "Exception occured in the privacy agreement, possibly because of the mixing"
            raise

def click_imgm(driver):
    try:
        time.sleep(7)
        imgm_xpath = "/html/body/div[4]/div/form/div[5]/div[2]/span/div/div/div/div[1]/div/table[1]/tbody/tr/td[1]/div/a/img[1]"
        imgm = driver.find_element_by_xpath(imgm_xpath)
        imgm.click()
    except:
        print "Exception occurred in trying to click the imgm symbol"
        raise

def download_tarball(driver, taxon_id):
    try:
        time.sleep(7)
        link = driver.find_element_by_partial_link_text(taxon_id)
        link.click()
    except:
        print "Exception in the download stage"
        raise

def imgm(l, taxon_id, af):
    try:
        output = open("downloadedFiles", "w")
        profile = construct_profile() 
        print 'profile'
        driver = webdriver.Firefox(firefox_profile = profile)
        print 'driver created'
        driver.get(l)
    # Page1) Input kishori's login credentials into the page 
        print "started driver"
        login(driver)
        print "logging in"
    # Page2 and 3) Click download
        download(driver)
        download2(driver)
    # Click the OK to the privacy agreement
        privacy(driver)
    # Click on the imgm to load it's contents
        click_imgm(driver)
    # Download the tarball
        download_tarball(driver, taxon_id)
    # Cleanup activities
        output.write(taxon_id)
        global count
        count += 1
        af.add(driver, taxon_id)
        time.sleep(5)
    except:
        print "Exception occurred but the show must go on"
        driver.close()

if __name__ == "__main__":
    main()
