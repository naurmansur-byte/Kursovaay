"""Export the original Markdown lesson kit for review/import; never uploads files."""
from __future__ import annotations
import argparse
import re
from html import escape
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt as DocxPt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak

REPO = Path(__file__).resolve().parents[1]

def plain(text):
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
    return text.replace('**', '').replace('`', '').replace('<br>', '\n').strip()

def blocks(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or re.fullmatch(r'-{3,}', line):
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [plain(s) for s in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c.strip()) for c in cells):
                    rows.append(cells)
                i += 1
            yield 'table', rows
            continue
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if match:
            yield 'heading', (len(match[1]), plain(match[2]))
            i += 1
            continue
        if line.startswith('```'):
            i += 1
            data = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                data.append(lines[i])
                i += 1
            yield 'paragraph', '\n'.join(data)
            i += 1
            continue
        if re.match(r'^[-*]\s+', line):
            yield 'paragraph', '• ' + plain(line[2:])
            i += 1
            continue
        if re.match(r'^\d+[.)]\s+', line):  # пункт нумерованного списка — отдельным абзацем
            yield 'paragraph', plain(line)
            i += 1
            continue
        data = [plain(line)]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||[-*] |```|\d+[.)]\s)', lines[i].strip()):
            data.append(plain(lines[i]))
            i += 1
        yield 'paragraph', ' '.join(data)

def page_break_title(title):
    match = re.match(r'Страница (\d+) из', title)
    return bool(match and int(match[1]) > 1)

def export_docx(text, output):
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(1.5)
    section.left_margin = section.right_margin = Cm(1.6)
    doc.styles['Normal'].font.name = 'DejaVu Sans'
    doc.styles['Normal'].font.size = DocxPt(10.7)
    doc.styles['Normal'].paragraph_format.space_after = DocxPt(5)
    for kind, value in blocks(text):
        if kind == 'heading':
            level, title = value
            if page_break_title(title):
                doc.add_page_break()
            doc.add_heading(title, level=min(level, 3))
        elif kind == 'table':
            table = doc.add_table(rows=0, cols=max(len(row) for row in value))
            table.style = 'Table Grid'
            for row in value:
                cells = table.add_row().cells
                for cell, content in zip(cells, row):
                    cell.text = content
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.font.size = DocxPt(9.5)
        else:
            doc.add_paragraph(value)
    section.footer.paragraphs[0].text = 'ХимБио просто • Черновик для проверки преподавателем'
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    Document(output)  # Verify the written Office container opens.

def export_notes_pdf(text, output):
    font = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    bold = font.with_name('DejaVuSans-Bold.ttf')
    if not font.exists():  # Windows (Max's PC): Arial has Cyrillic.
        font, bold = Path('C:/Windows/Fonts/arial.ttf'), Path('C:/Windows/Fonts/arialbd.ttf')
    if not font.exists() or not bold.exists():
        raise RuntimeError('Install DejaVu Sans fonts before PDF export')
    pdfmetrics.registerFont(TTFont('DejaVu', str(font)))
    pdfmetrics.registerFont(TTFont('DejaVuBold', str(bold)))
    body = ParagraphStyle('body', fontName='DejaVu', fontSize=10.7, leading=14, spaceAfter=5)
    cell = ParagraphStyle('cell', parent=body, fontSize=9.4, leading=12, spaceAfter=2)
    heading = ParagraphStyle('heading', fontName='DejaVuBold', fontSize=12, leading=16, spaceBefore=7, spaceAfter=7)
    title_style = ParagraphStyle('title', parent=heading, fontSize=15, leading=19)
    width = A4[0] - 90
    story = []
    for kind, value in blocks(text):
        if kind == 'heading':
            level, title = value
            if page_break_title(title):
                story.append(PageBreak())
            story.append(Paragraph(escape(title), title_style if level == 1 else heading))
        elif kind == 'table':
            n = max(map(len, value))
            rows = [[Paragraph(escape(c).replace('\n', '<br/>'), cell) for c in row] for row in value]
            table = Table(rows, colWidths=[width/n]*n, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.HexColor('#CBD5E1')),
                                       ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EFF6FF')),
                                       ('VALIGN',(0,0),(-1,-1),'TOP'),
                                       ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]))
            story += [table, Spacer(1,6)]
        else:
            story.append(Paragraph(escape(value).replace('\n','<br/>'), body))
    def footer(canvas, doc):
        canvas.setFont('DejaVu',8)
        canvas.drawString(45,24,'ХимБио просто • Черновик, ждёт проверки преподавателем')
        canvas.drawRightString(A4[0]-45,24,str(doc.page))
    output.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(output),pagesize=A4,leftMargin=45,rightMargin=45,topMargin=35,bottomMargin=38).build(story,onFirstPage=footer,onLaterPages=footer)

# --- Презентация в стиле 2 «ХимБио просто» (Макс, 13.10.2026) -----------------------------
# Обложка тёмная; слайды объяснения светлые (читаемость в Google Meet); ответ — отдельный тёмный слайд
# сразу после задания. Шрифты Unbounded и Manrope есть в Google Slides; в PowerPoint без них — замена.
INK, PAPER, ACCENT, MUTED, TINT, LIGHT = '151515', 'FFFFFF', 'F13A43', '6B6760', 'F5F2EB', 'F3F0E8'
CALLOUT = re.compile(r'^(Ловушка|Запомни|Задание[^:]*|Вопрос[^:]*|Входной вопрос|Проверь себя|Попробуй)\s*:\s*(.+)$', re.I)


def _rgb(hex_):
    return RGBColor.from_string(hex_)


def _box(slide, x, y, w, h, fill, rotation=0):
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb = _rgb(fill); shape.line.fill.background(); shape.shadow.inherit = False
    shape.rotation = rotation
    return shape


def _runs(paragraph, text, size, color, font='Manrope', bold=False, accent_bold=False):
    """**жирное** -> отдельные runs; accent_bold красит жирное в красный."""
    for k, part in enumerate(re.split(r'(\*\*[^*]+\*\*)', text)):
        if not part:
            continue
        strong = part.startswith('**')
        run = paragraph.add_run(); run.text = part.strip('*') if strong else part
        run.font.name, run.font.size, run.font.bold = font, Pt(size), bold or strong
        run.font.color.rgb = _rgb(ACCENT if strong and accent_bold else color)


def _text(slide, x, y, w, h, size=20, color=INK):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    return tf


def _para(tf):
    return tf.paragraphs[0] if not tf.paragraphs[0].runs and len(tf.paragraphs) == 1 else tf.add_paragraph()


def _chrome(slide, label, counter, dark):
    fg = LIGHT if dark else INK
    _box(slide, .7, .52, .13, .13, ACCENT)
    p = _para(_text(slide, .9, .38, 8, .4)); _runs(p, label, 11, fg, bold=True)
    p = _para(_text(slide, 10.6, .38, 2.1, .4)); _runs(p, counter, 11, MUTED if not dark else 'A8A39A', bold=True)
    from pptx.enum.text import PP_ALIGN
    p.alignment = PP_ALIGN.RIGHT


def _title(slide, text, color):
    tf = _text(slide, .7, .85, 12, 1.1)
    p = _para(tf); _runs(p, text, min(30, 760 / (max(len(text), 1) * .8)), color, font='Unbounded', bold=True)


def _table(slide, rows, top, body_size):
    cols = max(len(r) for r in rows)
    shape = slide.shapes.add_table(len(rows), cols, Inches(.8), Inches(top), Inches(11.7), Inches(.5 * len(rows)))
    table = shape.table
    for i, row in enumerate(rows):
        for j in range(cols):
            cell = table.cell(i, j); cell.text = ''
            cell.fill.solid(); cell.fill.fore_color.rgb = _rgb(INK if i == 0 else (TINT if i % 2 == 0 else PAPER))
            p = cell.text_frame.paragraphs[0]
            _runs(p, row[j] if j < len(row) else '', body_size - (3 if i == 0 else 2), LIGHT if i == 0 else INK, bold=i == 0)
    return top + .5 * len(rows) + .25


def _content(slide, lines, top, body_size, dark=False):
    """Пункты, нумерация, абзацы, таблицы; строки-выноски («Ловушка: …», «Задание: …») — блоками внизу."""
    fg = LIGHT if dark else INK
    rows, callouts, flow = [], [], []
    for line in lines:
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                rows.append(cells)
            continue
        if rows:
            flow.append(('table', rows)); rows = []
        m = CALLOUT.match(line.lstrip('- ').strip())
        if m and not dark:
            callouts.append(m.groups())
        else:
            flow.append(('line', line))
    if rows:
        flow.append(('table', rows))
    tf = None
    for kind, item in flow:
        if kind == 'table':
            top = _table(slide, item, top, body_size); tf = None
            continue
        if tf is None:
            tf = _text(slide, .8, top, 11.7, 4.8)
        p = _para(tf); p.space_after = Pt(6)
        bullet = re.match(r'^(?:[-*]|(\d+)[.)])\s+(.*)$', item)
        if bullet:
            marker = f'{bullet.group(1)}.  ' if bullet.group(1) else '■  '
            _runs(p, marker, body_size - (0 if bullet.group(1) else 6), ACCENT, bold=True)
            _runs(p, bullet.group(2), body_size, fg, accent_bold=not dark)
        else:
            _runs(p, item, body_size, fg, accent_bold=not dark)
    heights = [.5 + .38 * max(1, (len(label) + len(text) + 79) // 80) for label, text in callouts]
    y = 7.5 - .4 - sum(h + .15 for h in heights)
    for (label, text), h in zip(callouts, heights):
        trap = label.lower().startswith('ловушка')
        _box(slide, .8, y, 11.7, h, ACCENT if trap else INK)
        tf2 = _text(slide, 1.05, y + .1, 11.3, h - .15)
        p = _para(tf2); _runs(p, f'{label.upper()}:  ', body_size - 5, 'FFFFFF' if trap else ACCENT, font='Unbounded', bold=True)
        _runs(p, text, body_size - 3, 'FFFFFF' if trap else LIGHT)
        y += h + .15


def _blocks(body):
    def grab(name):
        m = re.search(rf'(?:### {name}[^\n]*|\*\*{name}[^\n]*\*\*)\s*\n(.*?)(?=\n### |\n\*\*(?:Текст|Заметки|Раскрытие|Ответ|Формулы)[^\n]*\*\*\s*\n|\Z)', body, re.S)
        return m.group(1).strip() if m else ''
    return grab('Текст ученику'), grab('Раскрытие ответа')


def _lines(text):
    return [ln.strip() for ln in plain_keep_bold(text).splitlines() if ln.strip()]


def plain_keep_bold(text):
    """Как plain(), но сохраняет **жирное** для runs."""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text).replace('`', '')


def export_slides(source, output):
    sections = list(re.finditer(r'^## Слайд (\d+)\.?\s*([^\n]*)', source, re.M))
    if not sections:
        raise RuntimeError('Expected headings: ## Слайд N. Title')
    readme = output.parent.parent.parent / 'course' / output.parent.name / 'README.md'
    topic_match = re.search(r'^# Неделя\s*0?(\d+)[.:]\s*(.+)$', readme.read_text(encoding='utf-8'), re.M) if readme.exists() else None
    week_no, topic = (topic_match.group(1), topic_match.group(2).strip()) if topic_match else (output.parent.name[-2:].lstrip('0'), '')
    label = f'ХИМБИО ПРОСТО · НЕДЕЛЯ {week_no}'
    deck = Presentation()
    deck.slide_width, deck.slide_height = Inches(13.333), Inches(7.5)
    blank = deck.slide_layouts[6]

    cover = deck.slides.add_slide(blank)
    cover.background.fill.solid(); cover.background.fill.fore_color.rgb = _rgb(INK)
    _chrome(cover, 'ХИМБИО ПРОСТО · ПОДГОТОВКА К ЕНТ', '', dark=True)
    plaque = _box(cover, .8, 2.0, 3.1, .85, ACCENT, rotation=-3)
    p = _para(plaque.text_frame); _runs(p, f'НЕДЕЛЯ {week_no}', 24, 'FFFFFF', font='Unbounded', bold=True)
    tf = _text(cover, .8, 3.2, 11.8, 2.4)
    p = _para(tf); _runs(p, (topic or '').upper(), min(48, 1000 / (max(len(topic), 1) * .78)), LIGHT, font='Unbounded', bold=True)
    p = _para(_text(cover, .8, 6.3, 11.8, .5)); _runs(p, 'Уроки недели · презентация с заметками для преподавателя', 14, 'A8A39A')
    cover.notes_slide.notes_text_frame.text = 'Обложка недели.'

    total = len(sections)
    for index, match in enumerate(sections):
        number, name = match.group(1), plain(match.group(2)).strip()
        body = source[match.end():sections[index + 1].start() if index + 1 < total else len(source)].strip()
        visible, answer = _blocks(body)
        if not visible:
            raise RuntimeError(f'Missing visible text block on slide {number}')
        lines = _lines(visible)
        estimated = sum(max(1, (len(ln) + 69) // 70) for ln in lines)
        if estimated > 20:
            raise RuntimeError(f'Slide {number} too dense; revise visible text before export')
        size = 22 if estimated <= 10 else 20 if estimated <= 14 else 18
        slide = deck.slides.add_slide(blank)
        slide.background.fill.solid(); slide.background.fill.fore_color.rgb = _rgb(PAPER)
        _chrome(slide, label, f'{number} / {total}', dark=False)
        _title(slide, name, INK)
        _content(slide, lines, 2.0, size)
        slide.notes_slide.notes_text_frame.text = body
        if answer:
            reveal = deck.slides.add_slide(blank)
            reveal.background.fill.solid(); reveal.background.fill.fore_color.rgb = _rgb(INK)
            _chrome(reveal, label, f'{number} / {total} · ответ', dark=True)
            plaque = _box(reveal, .8, 1.0, 1.9, .65, ACCENT, rotation=-3)
            p = _para(plaque.text_frame); _runs(p, 'ОТВЕТ', 18, 'FFFFFF', font='Unbounded', bold=True)
            p = _para(_text(reveal, 3.0, 1.0, 9.6, .7)); _runs(p, name, 18, 'A8A39A', font='Unbounded', bold=True)
            alines = _lines(answer)
            asize = 24 if sum(len(a) for a in alines) < 300 else 20
            _content(reveal, alines, 2.1, asize, dark=True)
            reveal.notes_slide.notes_text_frame.text = 'Показать после попытки учеников.\n\n' + answer
    output.parent.mkdir(parents=True, exist_ok=True)
    deck.save(output)
    restored = Presentation(output)
    print(f'PPTX: {len(restored.slides)} slides ({total} content + answers + cover), teacher notes retained')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--week',default='week-01')
    args=parser.parse_args()
    source=(REPO/'course'/args.week).resolve()
    if source.parent != (REPO/'course').resolve():raise ValueError('Expected course/week-NN')
    output=REPO/'exports'/args.week
    student={'notes-student','pre-work','homework'}
    for name in ['notes-student','pre-work','homework','lesson-1-plan','lesson-2-plan','homework-solutions','teacher-notes','README']:
        text=(source/f'{name}.md').read_text(encoding='utf-8')
        if name in student and text.startswith('---'):
            continue  # новая разметка: ученику — оформленный PDF (ниже), Word не нужен
        export_docx(text,output/('student' if name in student else 'teacher')/f'{name}.docx')
    quiz=(source/'quiz.md').read_text(encoding='utf-8')
    boundary=re.search(r'^## (?:Ключ|Для преподавателя|Преподавател|Только преподавателю)',quiz,re.M)
    if not boundary:raise RuntimeError('Expected separate teacher section in quiz.md')
    export_docx(quiz[:boundary.start()],output/'student/quiz.docx')
    export_docx(quiz,output/'teacher/quiz-with-key.docx')
    # Оформленные раздатки и слайды-картинки (Макс): нужны пакет markdown и Chrome/Chromium. Без них — простые версии.
    import importlib.util, sys as _sys
    _sys.path[:0] = [str(REPO/'tools'/'handout'), str(REPO/'tools'/'slides')]
    designed = importlib.util.find_spec('markdown') is not None
    for name in ['notes-student', 'pre-work', 'homework', 'quiz']:
        md = source/f'{name}.md'
        if designed and md.read_text(encoding='utf-8').startswith('---'):
            import handout
            try:
                handout.main(str(md.relative_to(REPO)), str((output/'student'/f'{name}.pdf').relative_to(REPO)))
                continue
            except RuntimeError as error:
                print(f'Handout skipped ({error}); plain PDF used')
        if name == 'notes-student':
            export_notes_pdf(md.read_text(encoding='utf-8'), output/'student/notes-student.pdf')
    export_slides((source/'slides-outline.md').read_text(encoding='utf-8'),output/'slides-editable.pptx')
    try:
        import slides
        slides.build(args.week)
    except Exception as error:  # нет Chrome — остаётся редактируемая версия
        print(f'Image slides skipped ({error}); use slides-editable.pptx')
    print(f'Local review/import files: {output}; no Google upload was performed')

if __name__=='__main__':main()
