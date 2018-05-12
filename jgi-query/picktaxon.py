import sys



def main(argv):
    listname = argv[1]
    outname = argv[2]

    reqsamples = {}
    with open(listname, 'r') as fin:
      for line in fin:
        fields = [ x.strip() for x in line.strip().split('\t') ]
        reqsamples[fields[0]] = True

    outresults={}
    with open(outname, 'r') as fin:
      for line in fin:
        fields = [ x.strip() for x in line.strip().split('\t') ]
        if fields[0] in reqsamples:
           outresults[fields[0]] = line.strip()

    for _, val in outresults.iteritems():
      print val


if __name__=="__main__":
    main(sys.argv)
