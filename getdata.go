package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
        "strings"
        "regexp"
)

func getContents(url string) (string, error) {
	timeout := time.Duration(10 * time.Second)
	httpclient := http.Client{
		Timeout: timeout,
	}
	resp, err := httpclient.Get(url)

	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	contents, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(contents), nil
}




func returnOrgName(content string, re *regexp.Regexp)  string{
     lines := strings.Split(content, "\n")
     var name string

     for _, line :=  range lines {
        // fmt.Println("------", line)
         if re.MatchString(line) {
         //   fmt.Println(line) 
            result := re.FindStringSubmatch(line)
          //  fmt.Println(result[1], result[2]) 
            name = result[1]
            //url2 :=  result[1]

            /*for i, name := range re.SubexpNames() {
               fmt.Println(i, name)
            }
*/
           // fmt.Println(line)
         }
     }
     return name 
     
}


func returnFirstPage(content string, re *regexp.Regexp)  string {
     lines := strings.Split(content, "\n")
     var url2 string

     for _, line :=  range lines {
         if re.MatchString(line) {
            result:= re.FindStringSubmatch(line)
            url2 =  result[1]
         }
     }

     return url2
}

func main() {

        re := regexp.MustCompile("<a class=\"genome-btn download-btn\" href=\"(?P<hi>.*)\"")
        re1 := regexp.MustCompile("/portal/(?P<name>[^/]*)/(?P<name1>[^/]*).download.html")
	var filename string
	flag.StringVar(&filename, "file", "", "the url file")
	flag.Parse()

        halfUrl:="https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=MetaDetail&page=metaDetail&taxon_oid="


	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {

		content, err := getContents(halfUrl+scanner.Text())
		if err != nil {
			panic(err)
		}

                url2 := returnFirstPage(content, re)

		content, err = getContents(url2)

		if err != nil {
			panic(err)
                }

            //    fmt.Println(content)
                orgname := returnOrgName(content, re1)

		fmt.Println(scanner.Text(), orgname)
		//fmt.Println(len(content))
	}

}
