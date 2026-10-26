# Weekly lesson build – instructions

Run on Thursday night after Atin replies "go". Builds NEXT week's lessons (Mon–Thu) and files them in the libraries.

Read `teaching/classes-2026-27.md` first: holidays, week numbers, what each class has covered, and exam timing. After each build, add the new week's topics to "Covered" there.

## Timetable (2026/27)
- Until Feb 2027 half term: Mon & Wed E3 Reading (Atin, both days); Tue E1 Speaking & Listening (Atin; Barry does Fri); Thu E2 Speaking & Listening (Atin; Joey does Fri).
- From Feb 2027 half term: Mon & Wed E3 Speaking & Listening; Tue E1 Writing. No Thursday class.
- Each day: two lessons (morning, afternoon), 9:30–2:30, ~45 min break, late start after register.
- Skip Hackney college holidays. In the Record of Work, a holiday is one line ("Half term holiday"), not blank rows.

## Course pattern
- Semester 1: Sept → Feb half term, exam in December. Semester 2: Feb half term → summer, exam around May.
- Each skill is one semester: Reading → Speaking & Listening → Writing → next level's Reading.
- Exam board: ESB Skills for Life. Never put exam dates on materials – use "Week N" and "Exam week".

## Each lesson gets
- A short lesson plan (aims, ESB criteria, timings, activities, differentiation).
- Printable handouts as Word .docx: A4, Arial/Calibri ≥11pt, fewest sides, "made by Atin" logo, answers in a separate .docx.
- Colour images and whole-class material on 16:9 projector pages (HTML), not printed.
- At least one online interactive activity per day (HTML, works on PC widescreen and phones, no audio – no headphones). No live-Claude features in public pages.
- At least one Kahoot quiz per class per week (give the questions ready to paste into Kahoot).
- Hackney / London contexts; learners are adult migrants, many in hostels, often not allowed to work.
- Reading questions must not reuse vocabulary from the text (paraphrase); no invented facts.
- Dialogue-ordering activities: only one valid order.

## Filing
- Public repo AtinWix/esol: `<level>/<skill>/weekNN/` – lesson plans (.docx), handouts (.docx), activities (.html). Every .docx also gets a PDF copy with the same name (soffice --headless --convert-to pdf) – the site shows the PDF on screen, with a Word download button. Update the home page and README with `tools/home.py` in this repo (add new entries to tools/esol.json for online pages and tools/docs.json for Word docs; fix the /home/claude/build paths in the script to wherever the repos are cloned). Add the "made by Atin" logo to every page. Remove any "Made with Claude Design" badge.
- Private repo AtinWix/personal: `teaching/` – the running scheme of work per class, and this week's Record of Work snippets (copy-and-paste text, one per day). SMART targets, records of work and schemes of work NEVER go in the public repo.
- Commit as `Claude <noreply@anthropic.com>`, then push both repos.

## Spare capacity
After next week is done, if the run still has room, add up to 4 more lessons to the next gap in another course book (any level E1–L2), in week order. Stop there.

## Finish
Send Atin one short message: what was built, links (https://atinwix.github.io/esol/…), and the Record of Work snippets. British English, brief.
