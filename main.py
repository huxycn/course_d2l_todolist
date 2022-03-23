import json
from bs4 import BeautifulSoup


with open('html/course.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

h2_list = soup.findAll('h2', attrs={'class': 'fs-4'})
div_list = soup.findAll('div', attrs={'class': 'module'})

course = {
    'title': '动手学深度学习',
    'chapters': []
}

for h2, div in zip(h2_list, div_list):
    chapter = {
        'title': h2['id'],
        'lectures': []
    }
    for dl in div.find('dl').findAll('dl'):
        lecture = {
            'title': dl.text.strip(),
            'assets': {
                'book': '',
                'pdf': '',
                'notebook': '',
                'video': ''
            }
        }
        for a in dl.findAll('a'):
            url = a['href']
            if url.startswith('assets'):
                url = 'https://courses.d2l.ai/zh-v2/' + url
                if 'pdfs' in url:
                    lecture['assets']['pdf'] = url
                if 'notebooks' in url:
                    lecture['assets']['notebook'] = url
            else:
                if 'video' in url:
                    lecture['assets']['video'] = url
                if 'zh-v2.d2l.ai' in url:
                    lecture['assets']['book'] = url

        chapter['lectures'].append(lecture)
    course['chapters'].append(chapter)

with open('json/course.json', 'w') as f:
    f.write(json.dumps(course, ensure_ascii=False))

with open('json/course.json', 'r') as f:
    course = json.load(f)


with open(f"readme.md", 'w') as f:
    # f.write('把李沐老师的 [动手深度学习在线课程](https://courses.d2l.ai/zh-v2/) 网页数据解析，导出格式化数据，做成打卡表格，方便管理学习进度\n')
    # f.write('Title,Book,PDF,Notebook,Video,Finished\n')
    f.write('| Title | Book | PDF | Notebook | Video | 打卡 |\n')
    f.write('| --- | :---: | :---: | :---: | :---: | :---: |\n')
    for i, chapter in enumerate(course['chapters']):
        f.write(f"| **{chapter['title']}** | {'='*4} | {'='*3} | {'='*8} | {'='*5} | {'='*2} |\n")
        # f.write(f"| **{chapter['title']}** | ---- | --- | ------- | ----- | 打卡 |\n")
        # f.write('| Title | Book | PDF | Notebook | Video | 打卡 |\n')
        # f.write('| --- | :---: | :---: | :---: | :---: | :---: |\n')

        for lecture in chapter['lectures']:
            line = f"| {lecture['title']} |"
            for k, v in lecture['assets'].items():
                if v:
                    line += f" [{k}]({v}) |"
                else:
                    line += f" - |"
            line += '\n'
            f.write(line)

