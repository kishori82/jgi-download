import sys



def main(argv):
   filename = argv[1]
   
   samples={}
   with open(filename, 'r') as fp:
      for line in fp:
         fields = [ x.strip()  for x in line.strip().split('\t') ]
         samples[fields[0]] = fields[2:]
        
   samplenames = samples.keys()

   clustered = {}
   for i in range(0, len(samplenames)):
     if samplenames[i] in clustered:
        continue
     clustered[samplenames[i]] =[]

     for j in range(i+1, len(samplenames)):
          if isSimilar(samplenames[i], samplenames[j], samples):
             clustered[samplenames[i]].append(samplenames[j])
         

   i =1
   for key, value in clustered.iteritems():
      if len(value)>1:
         print i, key, ' '.join(value)
         i += 1
   
def isSimilar(a, b, samples):
   if len(samples[a]) != len(samples[b]):
       return False
   
   for i in range( len(samples[a])):
        if samples[a][i]!=samples[b][i]:
           return False

   return True

if __name__=="__main__":
   main(sys.argv)
