#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# ── шрифт с кириллицей ──────────────────────────────────────────────────
font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]

FONT = 'DejaVuSans'
FONT_BOLD = 'DejaVuSans-Bold'

for p in font_paths:
    if os.path.exists(p):
        name = 'DejaVuSans-Bold' if 'Bold' in p else 'DejaVuSans'
        try:
            pdfmetrics.registerFont(TTFont(name, p))
        except Exception:
            pass

# ── цвета ────────────────────────────────────────────────────────────────
DARK   = colors.HexColor('#0d0d0d')
GOLD   = colors.HexColor('#c9a84c')
RUST   = colors.HexColor('#c0392b')
GREY   = colors.HexColor('#4a4540')
MID    = colors.HexColor('#7a7570')
LIGHT  = colors.HexColor('#e8e3da')
WHITE  = colors.white
BG2    = colors.HexColor('#1a1a1a')

# ── стили ────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['h1'] = ParagraphStyle('h1',
        fontName=FONT_BOLD, fontSize=22, leading=28,
        textColor=GOLD, spaceAfter=6)

    s['h2'] = ParagraphStyle('h2',
        fontName=FONT_BOLD, fontSize=15, leading=20,
        textColor=LIGHT, spaceBefore=18, spaceAfter=6)

    s['h3'] = ParagraphStyle('h3',
        fontName=FONT_BOLD, fontSize=11, leading=15,
        textColor=GOLD, spaceBefore=12, spaceAfter=4)

    s['body'] = ParagraphStyle('body',
        fontName=FONT, fontSize=9, leading=14,
        textColor=LIGHT, spaceAfter=4)

    s['code'] = ParagraphStyle('code',
        fontName=FONT, fontSize=8, leading=12,
        textColor=colors.HexColor('#c0c0c0'),
        backColor=colors.HexColor('#1a1a1a'),
        leftIndent=10, rightIndent=10,
        spaceBefore=4, spaceAfter=4,
        borderPadding=(6,8,6,8))

    s['label'] = ParagraphStyle('label',
        fontName=FONT_BOLD, fontSize=8, leading=11,
        textColor=GREY, spaceAfter=2)

    s['caption'] = ParagraphStyle('caption',
        fontName=FONT, fontSize=8, leading=11,
        textColor=MID, spaceAfter=4)

    s['title_page'] = ParagraphStyle('title_page',
        fontName=FONT_BOLD, fontSize=30, leading=36,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=8)

    s['subtitle'] = ParagraphStyle('subtitle',
        fontName=FONT, fontSize=12, leading=16,
        textColor=LIGHT, alignment=TA_CENTER, spaceAfter=4)

    s['sub2'] = ParagraphStyle('sub2',
        fontName=FONT, fontSize=9, leading=13,
        textColor=MID, alignment=TA_CENTER, spaceAfter=20)

    return s

def hr(color=GOLD, thickness=1):
    return HRFlowable(width='100%', thickness=thickness,
                      color=color, spaceAfter=10, spaceBefore=4)

def sp(h=8):
    return Spacer(1, h)

# ── таблица ──────────────────────────────────────────────────────────────
def safe_para(text, style):
    """Escape HTML that ReportLab can't handle (class= attrs etc)."""
    import html as html_mod
    # If text contains < with class= attributes, escape it fully
    if 'class=' in text or '<span' in text or '<br>' in text.lower():
        text = html_mod.escape(text)
    return Paragraph(text, style)

def make_table(headers, rows, col_widths=None):
    st = make_styles()
    data = [[Paragraph('<b>' + h + '</b>', st['body']) for h in headers]]
    for row in rows:
        data.append([safe_para(str(c), st['body']) for c in row])

    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#242424')),
        ('TEXTCOLOR',  (0,0), (-1,0), GOLD),
        ('FONTNAME',   (0,0), (-1,0), FONT_BOLD),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#2a2a2a')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#141414')),
        ('TEXTCOLOR',  (0,1), (-1,-1), LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.HexColor('#141414'), colors.HexColor('#181818')]),
        ('TOPPADDING',  (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING',(0,0), (-1,-1), 8),
    ])
    w = col_widths or None
    return Table(data, colWidths=w, style=ts, hAlign='LEFT')

# ── блок с кодом ─────────────────────────────────────────────────────────
def code_block(text, st):
    import html as html_mod
    escaped = html_mod.escape(text)
    escaped = escaped.replace('\n', '<br/>').replace(' ', '&nbsp;')
    return Paragraph(escaped, st['code'])

# ── ДОКУМЕНТ ─────────────────────────────────────────────────────────────
def build():
    path = '/home/user/-/portfolio_context.pdf'
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=2*cm,
        title='Portfolio Context — Далир Мансуров',
        author='Claude Code'
    )

    st = make_styles()
    story = []

    # ═══════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════
    story += [
        sp(60),
        Paragraph('PORTFOLIO CONTEXT', st['title_page']),
        Paragraph('Далир Мансуров — Веб-дизайнер и разработчик', st['subtitle']),
        Paragraph('Полный контекст проекта для Claude Code / VS Code', st['sub2']),
        hr(GOLD, 2),
        sp(6),
    ]

    tbl_meta = make_table(
        ['Параметр', 'Значение'],
        [
            ['Файл',        'portfolio_2.html'],
            ['Ветка',       'claude/fix-portfolio-issues-dc632'],
            ['GitHub Pages','https://mansurovdalir09-lang.github.io/-/portfolio_2.html'],
            ['Стек',        'Чистый HTML / CSS / JS (без фреймворков)'],
            ['Язык',        'Двуязычный: RU + AR (RTL)'],
            ['Email',       'mansurov.dalir09@gmail.com'],
        ],
        [4.5*cm, 12*cm]
    )
    story += [tbl_meta, sp(20)]

    # ═══════════════════════════════════════════════════════
    # 1. ИСПРАВЛЕНИЯ
    # ═══════════════════════════════════════════════════════
    story += [
        Paragraph('1. СПИСОК ИСПРАВЛЕНИЙ', st['h1']),
        hr(), sp(4),
    ]

    fixes = [
        ('БАГ #1 — Пустой экран на iOS Safari',
         'Элементы .hero-h1, .hero-tag, .hero-sub, .hero-ctas, .hero-stats имели opacity:0 '
         'из-за animation-fill-mode:both. JS падал раньше анимации → элементы оставались '
         'невидимыми навсегда.',
         'Добавить базовый opacity:1. Анимации запускать через класс .js-loaded который '
         'JS добавляет на body после загрузки.'),
        ('БАГ #2 — Uncaught Script Error (все анимации сломаны)',
         'canvas.getContext("2d") вызывался без проверки на null. '
         'Если canvas не найден — JS падает, счётчики = 0, IntersectionObserver не инициализируется.',
         'const ctx = canvas ? canvas.getContext("2d") : null; '
         'Все функции shredder проверяют: if(!ctx) return;'),
        ('БАГ #3 — JS без try/catch',
         'Любая ошибка в JS ломает весь сайт.',
         'Обернуть весь код в DOMContentLoaded + try/catch. '
         'В catch — fallback: принудительно показать весь контент.'),
        ('БАГ #4 — mix-blend-mode на cursor → белый экран iOS',
         'Fixed position + mix-blend-mode на iOS Safari вызывает инверсию всего контента.',
         'Убрать mix-blend-mode полностью. '
         'Курсор показывать только на desktop через @media (hover:hover) and (pointer:fine).'),
        ('ДИЗАЙН #5 — Hero layout сломан на мобильном',
         'Hero-контент — двухколоночный grid. На мобиле нет переключения в 1 колонку.',
         '@media (max-width:900px): grid-template-columns:1fr, padding-top:120px, '
         'hero-stats: flex-direction:row flex-wrap:wrap'),
        ('ДИЗАЙН #6 — CTA заголовки слипаются',
         '.cta-h2 имел line-height:0.9 → слово "ПОГОВОРИМ" обрезалось на mobile.',
         'line-height:1.1; word-break:break-word; font-size:clamp(52px,8vw,110px)'),
        ('ТЕКСТ #7 — Арабская версия: "НЕ МОЯ РАБОТА" не переводится',
         'Блок .big-no захардкожен в HTML без data-i18n.',
         'В switchLang() добавить: bigNoEl.innerHTML = isAr '
         '? "<span>لا</span> أقبل هذه المشاريع" : "<span>НЕ</span> МОЯ РАБОТА"'),
        ('ТЕКСТ #8 — Калькулятор: цены в рублях при AR',
         'При переключении на AR цены должны быть в риалах.',
         'if(currentLang==="ar") { totalSAR = Math.round(total/25/100)*100; '
         'priceEl.textContent = "⃁ " + totalSAR.toLocaleString("ar-SA"); }'),
        ('ТЕКСТ #9 — Счётчики остаются на 0',
         'Из-за JS crash (баг #2) IntersectionObserver не инициализировался.',
         'После fix #2 должно заработать автоматически. '
         'Убедиться что data-count атрибуты присутствуют на элементах.'),
        ('ТЕКСТ #10 — Арабская грамматика',
         'شهراً في الرياض / هذه التجربة أعطتني / وتعلمت',
         '١٠ شهور في الرياض / هذه التجربة منحتني / وتعَّلمت'),
    ]

    for title, problem, solution in fixes:
        story.append(KeepTogether([
            Paragraph(title, st['h3']),
            make_table(
                ['Проблема', 'Решение'],
                [[problem, solution]],
                [8*cm, 8*cm]
            ),
            sp(6),
        ]))

    # ═══════════════════════════════════════════════════════
    # 2. НОВЫЕ ПРАВКИ (из последнего разговора)
    # ═══════════════════════════════════════════════════════
    story += [
        sp(10),
        Paragraph('2. НОВЫЕ ПРАВКИ (приоритет)', st['h1']),
        hr(RUST), sp(4),
    ]

    new_fixes = make_table(
        ['#', 'Что исправить', 'Где', 'Как'],
        [
            ['A',
             'Страна: "из Таджикистана" → "из России"',
             'about_p1 в CONTENT (ru и ar)',
             'В RU: "...разработчик из России"\nВ AR: "...مطور من روسيا"'],
            ['B',
             'Блок "Не моя работа" не работает',
             '.nomy-item элементы',
             'Добавить hover-анимацию зачёркивания или\nвизуальный эффект при клике/hover'],
            ['C',
             'Имя на арабском — написано по-русски',
             '.hero-h1 (id="heroH1")',
             'В switchLang() → isAr:\nheroH1.innerHTML = \'<span class="accent">دالير</span>\n<br><span class="accent">منصوروف</span>\''],
            ['D',
             'Текст про Эр-Рияд — неверный',
             'about_p2 в CONTENT',
             'RU: "Провёл 10 месяцев в Эр-Рияде,\nизучая арабский язык"\nAR: "قضيت ١٠ شهور في الرياض\nأتعلّم اللغة العربية"'],
            ['E',
             'Новый символ риала ⃁ (U+20C1)',
             'updateCalc() функция',
             'Использовать символ ⃁\nФоллбэк если не поддерживается: ريال\nПроверить: document.fonts'],
        ],
        [0.6*cm, 4.5*cm, 3.5*cm, 7.5*cm]
    )
    story += [new_fixes, sp(16)]

    # ═══════════════════════════════════════════════════════
    # 3. JS КОД — КЛЮЧЕВЫЕ ФРАГМЕНТЫ
    # ═══════════════════════════════════════════════════════
    story += [
        Paragraph('3. JS — КЛЮЧЕВЫЕ ФРАГМЕНТЫ', st['h1']),
        hr(), sp(4),
    ]

    story += [
        Paragraph('3.1 — Hero анимация (FIX #1)', st['h2']),
        Paragraph('CSS: базовые состояния видимые:', st['caption']),
        code_block(
            '.hero-h1, .hero-tag, .hero-sub, .hero-ctas, .hero-stats { opacity: 1; }\n'
            '.js-loaded .hero-h1 { animation: heroSlide 0.9s 0.1s ease forwards; }\n'
            '.js-loaded .hero-tag { animation: heroSlide 0.9s ease forwards; }\n'
            '@keyframes heroSlide {\n'
            '  from { opacity: 0; transform: translateY(24px); }\n'
            '  to   { opacity: 1; transform: translateY(0); }\n'
            '}',
            st
        ),
        Paragraph('JS: добавить класс после загрузки:', st['caption']),
        code_block(
            'window.addEventListener("DOMContentLoaded", function() {\n'
            '  try {\n'
            '    document.body.classList.add("js-loaded"); // FIX #1\n'
            '    // ... весь остальной код ...\n'
            '  } catch(e) {\n'
            '    console.error(e);\n'
            '    // fallback:\n'
            '    document.querySelectorAll(".hero-h1,.hero-tag,.hero-sub,.hero-ctas,.hero-stats")\n'
            '      .forEach(el => { el.style.opacity="1"; el.style.transform="none"; });\n'
            '    document.querySelectorAll(".reveal").forEach(el => el.classList.add("visible"));\n'
            '  }\n'
            '});',
            st
        ),
        sp(8),

        Paragraph('3.2 — Canvas null check (FIX #2)', st['h2']),
        code_block(
            '// БЫЛО (краш если canvas=null):\n'
            'const canvas = document.getElementById("shredder-canvas");\n'
            'const ctx = canvas.getContext("2d"); // ← CRASH\n\n'
            '// СТАЛО:\n'
            'const canvas = document.getElementById("shredder-canvas");\n'
            'const ctx = canvas ? canvas.getContext("2d") : null;\n'
            '// В каждой функции shredder:\n'
            'function drawShredder() {\n'
            '  if (!ctx) return;\n'
            '  // ...\n'
            '}',
            st
        ),
        sp(8),

        Paragraph('3.3 — switchLang() — полный список изменений', st['h2']),
        code_block(
            'function switchLang(lang) {\n'
            '  var isAr = lang === "ar";\n'
            '  document.body.classList.toggle("lang-ar", isAr);\n\n'
            '  // data-i18n элементы\n'
            '  document.querySelectorAll("[data-i18n]").forEach(el => {\n'
            '    var key = el.getAttribute("data-i18n");\n'
            '    if (CONTENT[lang][key]) el.innerHTML = CONTENT[lang][key];\n'
            '  });\n\n'
            '  // FIX #7: bigNoEl\n'
            '  var bigNoEl = document.getElementById("bigNoEl");\n'
            '  if (bigNoEl) {\n'
            '    bigNoEl.innerHTML = isAr\n'
            '      ? \'<span style="color:var(--rust);">لا</span> أقبل هذه المشاريع\'\n'
            '      : "<span>НЕ</span> МОЯ РАБОТА";\n'
            '  }\n\n'
            '  // FIX C: имя на арабском\n'
            '  var heroH1 = document.getElementById("heroH1");\n'
            '  if (heroH1) {\n'
            '    heroH1.innerHTML = isAr\n'
            '      ? \'<span class="accent">دالير</span><br>\'\n'
            '        + \'<span class="accent">منصوروف</span>\'\n'
            '      : \'<span class="accent">ДАЛИР</span><br>\'\n'
            '        + \'<span class="accent">МАН</span>\'\n'
            '        + \'<span class="ghost">СУРОВ</span>\';\n'
            '  }\n\n'
            '  updateCalc();\n'
            '}',
            st
        ),
        sp(8),

        Paragraph('3.4 — Калькулятор: SAR + новый символ риала (FIX #8 + E)', st['h2']),
        code_block(
            '// Новый символ риала (Unicode U+20C1, утверждён 20.02.2025)\n'
            'var RIYAL_SYMBOL = "\\u20C1"; // ⃁\n\n'
            'function updateCalc() {\n'
            '  var total = calcBase + calcExtras;\n'
            '  var priceEl = document.getElementById("calcPrice");\n'
            '  if (!priceEl) return;\n\n'
            '  if (currentLang === "ar") {\n'
            '    var totalSAR = Math.round(total / 25 / 100) * 100;\n'
            '    priceEl.textContent = RIYAL_SYMBOL + " "\n'
            '      + totalSAR.toLocaleString("ar-SA");\n'
            '  } else {\n'
            '    priceEl.textContent = total.toLocaleString("ru-RU") + " ₽";\n'
            '  }\n'
            '}',
            st
        ),
        sp(8),

        Paragraph('3.5 — CSS cursor (FIX #4, без mix-blend-mode)', st['h2']),
        code_block(
            '/* ПО УМОЛЧАНИЮ — курсор скрыт */\n'
            '#cursor, #cursor-ring { display: none; }\n\n'
            '/* ТОЛЬКО desktop с hover */\n'
            '@media (hover: hover) and (pointer: fine) {\n'
            '  body { cursor: none; }\n'
            '  #cursor {\n'
            '    display: block;\n'
            '    background: var(--gold);\n'
            '    /* НЕТ mix-blend-mode! */\n'
            '  }\n'
            '}',
            st
        ),
    ]

    # ═══════════════════════════════════════════════════════
    # 4. КОНТЕНТ — ТЕКСТЫ
    # ═══════════════════════════════════════════════════════
    story += [
        sp(10),
        Paragraph('4. ТЕКСТЫ (CONTENT объект)', st['h1']),
        hr(), sp(4),
    ]

    story += [
        Paragraph('4.1 — About секция', st['h2']),
        make_table(
            ['Ключ', 'RU текст', 'AR текст'],
            [
                ['about_p1',
                 'Веб-дизайнер и разработчик из России. Специализируюсь на создании сайтов, которые не просто красиво выглядят — они работают на бизнес.',
                 'مصمم ومطور مواقع من روسيا. متخصص في إنشاء مواقع لا تبدو جميلة فحسب — بل تعمل لصالح العمل.'],
                ['about_p2',
                 'Провёл 10 месяцев в Эр-Рияде, изучая арабский язык. Этот опыт дал мне глубокое понимание культуры и требований ближневосточного рынка.',
                 'قضيت ١٠ شهور في الرياض أتعلّم اللغة العربية. هذه التجربة منحتني فهماً عميقاً للثقافة ومتطلبات السوق الشرق أوسطية.'],
            ],
            [3*cm, 7*cm, 6*cm]
        ),
        sp(10),

        Paragraph('4.2 — Hero h1 (имя)', st['h2']),
        make_table(
            ['Язык', 'HTML'],
            [
                ['RU', '<span class="accent">ДАЛИР</span><br><span class="accent">МАН</span><span class="ghost">СУРОВ</span>'],
                ['AR', '<span class="accent">دالير</span><br><span class="accent">منصوروف</span>'],
            ],
            [2*cm, 14*cm]
        ),
        sp(10),

        Paragraph('4.3 — Арабская грамматика (FIX #10)', st['h2']),
        make_table(
            ['Было (неверно)', 'Стало (верно)'],
            [
                ['شهراً في الرياض', '١٠ شهور في الرياض'],
                ['هذه التجربة أعطتني', 'هذه التجربة منحتني'],
                ['وتعلمت', 'وتعَّلمت'],
            ],
            [8*cm, 8*cm]
        ),
    ]

    # ═══════════════════════════════════════════════════════
    # 5. ЦЕНЫ И КОНТАКТЫ
    # ═══════════════════════════════════════════════════════
    story += [
        sp(10),
        Paragraph('5. ЦЕНЫ И КОНТАКТЫ', st['h1']),
        hr(), sp(4),

        Paragraph('Цены калькулятора (RUB)', st['h2']),
        make_table(
            ['Тип сайта', 'Цена RUB', 'Цена SAR (÷25)', 'Срок'],
            [
                ['Лендинг',             '50 000 ₽',  '2 000 ⃁', '10 дней'],
                ['Интернет-магазин',    '100 000 ₽', '4 000 ⃁', '21 день'],
                ['Корпоративный сайт',  '130 000 ₽', '5 200 ⃁', '28 дней'],
                ['Двуязычный AR/RU',    '85 000 ₽',  '3 400 ⃁', '17 дней'],
            ],
            [5*cm, 3.5*cm, 3.5*cm, 3.5*cm]
        ),
        sp(10),

        Paragraph('Контакты (правильные ссылки)', st['h2']),
        make_table(
            ['Канал', 'Ссылка / значение'],
            [
                ['WhatsApp',  'https://wa.me/79513894443'],
                ['Telegram',  'https://t.me/Dalir37'],
                ['Instagram', 'https://www.instagram.com/mansurov.dalir2018/'],
                ['Email',     'mansurov.dalir09@gmail.com'],
            ],
            [3.5*cm, 13*cm]
        ),
    ]

    # ═══════════════════════════════════════════════════════
    # 6. СИМВОЛ РИАЛА
    # ═══════════════════════════════════════════════════════
    story += [
        sp(10),
        Paragraph('6. НОВЫЙ СИМВОЛ САУДОВСКОГО РИАЛА', st['h1']),
        hr(GOLD), sp(4),

        make_table(
            ['Параметр', 'Значение'],
            [
                ['Символ',              '⃁ (Saudi Riyal Sign)'],
                ['Unicode код',         'U+20C1'],
                ['Unicode версия',      '17.0 (сентябрь 2025)'],
                ['Дата утверждения',    '20 февраля 2025, король Салман'],
                ['JS escape',           '\\u20C1'],
                ['Направление',         'LTR и RTL (в отличие от ﷼ U+FDFC)'],
                ['Фоллбэк',             'ريال (если шрифт не поддерживает U+20C1)'],
                ['Курс к рублю',        '1 SAR ≈ 25 RUB'],
            ],
            [5*cm, 11*cm]
        ),
        sp(8),

        Paragraph('Использование в коде:', st['caption']),
        code_block(
            'var RIYAL = "\\u20C1"; // ⃁\n\n'
            '// Проверка поддержки (опционально):\n'
            'function getRiyalSymbol() {\n'
            '  // U+20C1 в Unicode 17.0 — поддержка постепенная\n'
            '  // Используем как есть, браузеры обновятся\n'
            '  return "\\u20C1";\n'
            '}\n\n'
            '// В updateCalc():\n'
            'priceEl.textContent = getRiyalSymbol() + " " + totalSAR.toLocaleString("ar-SA");',
            st
        ),
    ]

    # ═══════════════════════════════════════════════════════
    # 7. ТЕХНИЧЕСКИЙ СТЕК
    # ═══════════════════════════════════════════════════════
    story += [
        sp(10),
        Paragraph('7. ТЕХНИЧЕСКИЙ СТЕК', st['h1']),
        hr(), sp(4),

        make_table(
            ['Технология', 'Использование'],
            [
                ['HTML5',                'Семантическая разметка, без фреймворков'],
                ['CSS3',                 'Переменные, Grid, Flexbox, @media, @keyframes'],
                ['Vanilla JS',           'ES5/ES6, IntersectionObserver, DOM manipulation'],
                ['Google Fonts',         'Inter, Bebas Neue, Cormorant Garamond, Noto Kufi Arabic'],
                ['i18n система',         'CONTENT объект + data-i18n атрибуты'],
                ['switchLang(ru|ar)',     'Переключение языка, direction:rtl через .lang-ar на body'],
                ['IntersectionObserver', 'Reveal анимации + счётчики при прокрутке'],
                ['Canvas API',           'Shredder эффект (опциональный), с null-проверкой'],
            ],
            [5*cm, 11*cm]
        ),
    ]

    # ═══════════════════════════════════════════════════════
    # 8. ЧЕК-ЛИСТ ТЕСТИРОВАНИЯ
    # ═══════════════════════════════════════════════════════
    story += [
        sp(10),
        Paragraph('8. ЧЕК-ЛИСТ ТЕСТИРОВАНИЯ', st['h1']),
        hr(RUST), sp(4),

        make_table(
            ['#', 'Тест', 'Ожидаемый результат'],
            [
                ['1', 'Открыть в iOS Safari',
                 'Тёмный фон + заголовок ДАЛИР МАН виден сразу (не пустой экран)'],
                ['2', 'Нажать عربي',
                 'RTL layout, все тексты на арабском, имя "دالير منصوروف"'],
                ['3', 'Калькулятор → AR',
                 'Цены в ⃁ риалах (50000₽ → 2000 ⃁)'],
                ['4', 'Секция "Не моя работа" → AR',
                 'Заголовок меняется на "لا أقبل هذه المشاريع"'],
                ['5', 'Прокрутить до статистики',
                 'Счётчики анимируются: 3, 3, 8'],
                ['6', 'Мобильный 375px',
                 'Hero — 1 колонка, статистика в строку'],
                ['7', 'Проверить About секцию',
                 '"из России", "изучая арабский язык в Эр-Рияде"'],
                ['8', 'Desktop hover на cursor',
                 'Кастомный курсор без инверсии контента'],
            ],
            [0.7*cm, 6*cm, 9*cm]
        ),
    ]

    # build
    doc.build(story)
    print('PDF создан:', path)
    return path

if __name__ == '__main__':
    build()
