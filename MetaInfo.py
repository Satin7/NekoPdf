from semanticscholar import SemanticScholar
import pandas as pd

def sch(info):
    sch=SemanticScholar(timeout=2)
    paper = sch.paper(info)
    if paper=={}:
        return 'Paper Not Found by S.S., sorry.','Not Found by S.S.'

    title='# '+paper['title']
    name=[]
    for author in paper['authors']:
        name.append(author['name'])
    abstract=paper['abstract']
    cites=paper['citations']
    citeinfo=pd.DataFrame(columns=['title','auther(s)','venue','publish date','doi'])
    for cite in cites:
        citenames=''
        for author in cite['authors']:
            citenames+=author['name']+' '
        for key,value in cite.items():
            if value==None:
                cite[key]='NoInfo'
        info={'title':cite['title'],'author(s)':citenames,'venue':cite['venue'],'publish date':str(cite['year']),'doi':cite['doi']}
        #info=pd.DataFrame([cite['title'],citenames,cite['venue'],str(cite['year']),'https://doi.org/'+cite['doi']])
        citeinfo.append(info,ignore_index=True)

    if abstract==None:
        abstract='NoInfofromSemanticScholar'
    
    return title+'\n'+'_'+' '.join(name)+'_'+'\n'+abstract+'\n\n', citeinfo