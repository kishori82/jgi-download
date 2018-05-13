import sys, os, re
import subprocess
import optparse



def downloadfile(_string, filename):
   string = _string.replace("amp;", "") 
   download_command = ("curl \'https://genome.jgi.doe.gov" + string + "\' -b cookies > {}".format(filename))

   print download_command
   subprocess.call(download_command, shell=True)


usage = sys.argv[0] + " -o/--organism  <organism>  -l/--login <login> -p/--pass <password> -f <file1>  -f <file2> "
parser = optparse.OptionParser(usage=usage)
parser.add_option("-o", "--organism", dest="organism",  default=None, help="organism name")
parser.add_option("-l", "--login", dest="login", default=None, help="JGI login name")
parser.add_option("-p", "--pass", dest="password", default=None, help="JGI password")
parser.add_option("-f", "--file", dest="files",  default=[], action="append",  help="file to download")
parser.add_option("-L", "--list", dest="list",  action="store_true", default=False,  help="list file names")
parser.add_option("-m", "--map", dest="taxon_to_organism",  default=None,  help="taxon to organism map file")
parser.add_option("-t", "--taxon", dest="taxon",  default=None,  help="taxon name")

def main(argv):
   global parser
   opt, args = parser.parse_args(argv)

   if opt.login:
      loginToJGI(opt)

   if opt.taxon_to_organism:
      taxon_to_organism=read_taxon_to_organism(opt.taxon_to_organism)
      if opt.taxon and  opt.organism == None:
         opt.organism = taxon_to_organism[opt.taxon]

      if opt.taxon==None and  opt.organism:
         opt.taxon = taxon_to_organism[opt.organism]


         
   if opt.files and opt.organism:
      downloadFiles(opt)

   if opt.list and opt.organism:
      listFiles(opt)

def read_taxon_to_organism(taxon_to_organism_file):
   taxon_to_organism_map={}
   with open(taxon_to_organism_file, 'r') as fin:
      for line in fin:
         fields = [ x.strip() for x in line.strip().split('\t') ]
         if len(fields)==2:
            taxon_to_organism_map[fields[0]] = fields[1]
            taxon_to_organism_map[fields[1]] = fields[0]
      
   return taxon_to_organism_map


def loginToJGI(opts):
      USER=opts.login
      PASSWORD=opts.password
      LOGIN_STRING = ("curl 'https://signon.jgi.doe.gov/signon/create' "
                "--data-urlencode 'login={}' "
                "--data-urlencode 'password={}' "
                "-c cookies > /dev/null"
                .format(USER, PASSWORD))

      subprocess.check_output(LOGIN_STRING, shell=True)


def listFiles(opt):
   organism = opt.organism

   refiles = re.compile("filename=\"([^\"]*)\".*size=\"([^\"]*)\"") 
   download_command = ("curl https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism={} -b cookies > {}".format(organism, organism+".xml"))
   subprocess.call(download_command, shell=True)

   i = 1
   print
   print  "FILES: ", opt.taxon, opt.organism
   with open(organism + ".xml", 'r') as fin:
      for line in fin:
         res = refiles.search(line)
         if res:
             print "[{}]".format(i), res.group(1), res.group(2)
             i += 1
               
   os.remove(organism + ".xml")



def downloadFiles(opt):
   organism = opt.organism
   files = opt.files

   refiles = [ (x, re.compile("url=\"(\S+" + x + ")") )for x in files ]
   download_command = ("curl https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism={} -b cookies > {}".format(organism, organism+".xml"))
   subprocess.call(download_command, shell=True)

   with open(organism + ".xml", 'r') as fin:
      for line in fin:
         for file, refile in refiles:
            res = refile.search(line)
            if res:
                downloadfile(res.group(1),  file)
               
   os.remove(organism + ".xml")


if __name__=="__main__":
   main(sys.argv)
