import re, os, subprocess, json, shutil
MD='/home/claude/docs/md/'; OUT='/tmp/claude-0/lessons/'
EX={'e3':('e3/reading','E3 Reading'),'e2':('e2/speaking-listening','E2 Speaking & Listening'),'e1':('e1/speaking-listening','E1 Speaking & Listening')}
def clean(t): return re.sub(r'&#91;image:[^\]]*\\\]','',t)
def sections(text,level):
    parts=re.split(r'(?m)^(?=%s )'%('#'*level),text)
    return [p for p in parts if p.startswith('#'*level+' ')]
lessons=[]
ov=clean(open(MD+'all-levels__exam-prep-lesson-plans-4-13__1-overview.md').read())
for s in sections(ov,2):
    m=re.match(r'## Entry (\d) (Reading|Speaking and Listening), Lesson (\d+): (.*)',s)
    if m: lessons.append(('e'+m[1],int(m[3]),m[4].strip(),s))
for k,f in [('e3','2-e3-reading'),('e2','3-e2-sl'),('e1','4-e1-sl')]:
    t=clean(open(MD+f'all-levels__exam-prep-lesson-plans-4-13__{f}.md').read())
    for s in sections(t,2):
        m=re.match(r'## Lesson (\d+): (.*)',s)
        if m: lessons.append((k,int(m[1]),m[2].strip(),s))
docs=[]
for k,n,title,s in sorted(lessons):
    folder,name=EX[k]
    body=s.split('\n',1)[1]
    intro,*subs=re.split(r'(?m)^(?=### )',body)
    hand=[x for x in subs if x.startswith('### Handout')]
    plan=[x for x in subs if not x.startswith('### Handout')]
    head=f"{name} – Exam Prep Lesson {n}: {title}"
    slug=f"exam-prep/lesson-{n:02d}"
    os.makedirs(f'/home/claude/esol/{folder}/exam-prep',exist_ok=True)
    def build(md,suffix,ttl):
        src=OUT+f'{k}-{n}-{suffix}.md'
        md=md.replace('### ','## ')
        open(src,'w').write('![](logo.png){width=1.4in}\n\n# '+ttl+'\n\n'+md)
        dst=f'/home/claude/esol/{folder}/{slug}-{suffix}.docx'
        subprocess.run(['pandoc',src,'-o',dst,'--reference-doc=/home/claude/docs/ref.docx','--resource-path=/home/claude/docs'],check=True)
        return dst
    p=build(intro+''.join(plan),'plan',head+' – Lesson plan and answers')
    docs.append({"folder":folder,"group":"Exam prep lessons","path":p.split('/home/claude/esol/')[1],"title":f"Lesson {n}: {title} – plan and answers"})
    if hand:
        hb=''.join(hand); h=build(('' if 'Name:' in hb else 'Name: ____________________   Date: ____________\n\n')+hb,'handouts',head+' – Handouts')
        docs.append({"folder":folder,"group":"Exam prep lessons","path":h.split('/home/claude/esol/')[1],"title":f"Lesson {n}: {title} – student handouts"})
json.dump(docs,open('/home/claude/build/lessondocs.json','w'),indent=1)
print(len(lessons),'lessons',len(docs),'docs')
