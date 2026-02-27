"""
PDF Rapor Motoru — Eğitim Check-Up
Öğrenci kişisel bilgileri + test sonuçları + AI analiz raporlarını
profesyonel PDF formatında dışa aktarır.
"""

import io
import re
import textwrap
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ============================================================
# FONT KAYDI (Türkçe karakter desteği)
# ============================================================
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

try:
    pdfmetrics.registerFont(TTFont("DejaVu", FONT_DIR + "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Italic", FONT_DIR + "DejaVuSans-Oblique.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-BoldItalic", FONT_DIR + "DejaVuSans-BoldOblique.ttf"))
    FONT_NAME = "DejaVu"
    FONT_BOLD = "DejaVu-Bold"
    FONT_ITALIC = "DejaVu-Italic"
except Exception:
    FONT_NAME = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    FONT_ITALIC = "Helvetica-Oblique"

# ============================================================
# RENK PALETİ
# ============================================================
PRIMARY   = HexColor("#1B2A4A")  # Koyu lacivert
SECONDARY = HexColor("#2E86AB")  # Açık mavi
ACCENT    = HexColor("#A23B72")  # Bordo/mor
SUCCESS   = HexColor("#155724")  # Yeşil
BG_LIGHT  = HexColor("#F8F9FA")  # Açık gri arka plan
BG_HEADER = HexColor("#1B2A4A")  # Header arka plan
BORDER    = HexColor("#DEE2E6")  # Kenar rengi

# ============================================================
# STİL TANIMLARI
# ============================================================

def _get_styles():
    """PDF için özel Türkçe uyumlu stiller döndürür."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='TR_Title',
        fontName=FONT_BOLD,
        fontSize=20,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=26,
    ))

    styles.add(ParagraphStyle(
        name='TR_Subtitle',
        fontName=FONT_NAME,
        fontSize=10,
        textColor=SECONDARY,
        alignment=TA_CENTER,
        spaceAfter=20,
    ))

    styles.add(ParagraphStyle(
        name='TR_H1',
        fontName=FONT_BOLD,
        fontSize=14,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        leading=18,
        borderPadding=(0, 0, 4, 0),
    ))

    styles.add(ParagraphStyle(
        name='TR_H2',
        fontName=FONT_BOLD,
        fontSize=12,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        leading=16,
    ))

    styles.add(ParagraphStyle(
        name='TR_H3',
        fontName=FONT_BOLD,
        fontSize=10,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        leading=14,
    ))

    styles.add(ParagraphStyle(
        name='TR_Body',
        fontName=FONT_NAME,
        fontSize=9,
        textColor=black,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
        leading=13,
    ))

    styles.add(ParagraphStyle(
        name='TR_Small',
        fontName=FONT_NAME,
        fontSize=7.5,
        textColor=HexColor("#6C757D"),
        alignment=TA_CENTER,
        spaceBefore=4,
    ))

    styles.add(ParagraphStyle(
        name='TR_TableHeader',
        fontName=FONT_BOLD,
        fontSize=9,
        textColor=white,
        alignment=TA_CENTER,
        leading=12,
    ))

    styles.add(ParagraphStyle(
        name='TR_TableCell',
        fontName=FONT_NAME,
        fontSize=8.5,
        textColor=black,
        alignment=TA_LEFT,
        leading=11,
    ))

    styles.add(ParagraphStyle(
        name='TR_TableCellCenter',
        fontName=FONT_NAME,
        fontSize=8.5,
        textColor=black,
        alignment=TA_CENTER,
        leading=11,
    ))

    styles.add(ParagraphStyle(
        name='TR_ReportText',
        fontName=FONT_NAME,
        fontSize=8.5,
        textColor=HexColor("#212529"),
        alignment=TA_JUSTIFY,
        spaceAfter=3,
        leading=12,
    ))

    styles.add(ParagraphStyle(
        name='TR_Bullet',
        fontName=FONT_NAME,
        fontSize=8.5,
        textColor=HexColor("#212529"),
        alignment=TA_LEFT,
        spaceAfter=2,
        leading=12,
        leftIndent=12,
        bulletIndent=0,
    ))

    return styles


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def _safe(text):
    """XML-unsafe karakterleri temizler (ReportLab Paragraph için)."""
    if not text:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def _section_divider():
    """Bölüm ayırıcı çizgi."""
    return HRFlowable(
        width="100%", thickness=1,
        color=BORDER, spaceAfter=8, spaceBefore=8
    )


def _header_bar(text, styles):
    """Renkli bölüm başlığı."""
    data = [[Paragraph(f"<b>{_safe(text)}</b>", styles['TR_TableHeader'])]]
    t = Table(data, colWidths=[17.5 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t


def _markdown_to_flowables(md_text, styles):
    """
    Basitleştirilmiş Markdown → ReportLab flowable dönüştürücü.
    AI raporlarındaki Markdown formatını PDF'e çevirir.
    """
    if not md_text:
        return [Paragraph("<i>Rapor içeriği bulunamadı.</i>", styles['TR_Body'])]

    flowables = []
    lines = md_text.split('\n')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flowables.append(Spacer(1, 3))
            continue

        # Heading'ler
        if stripped.startswith('#### '):
            text = stripped[5:]
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', _safe(text).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>'))
            text = re.sub(r'&lt;b&gt;(.*?)&lt;/b&gt;', r'<b>\1</b>', text)
            clean = re.sub(r'<[^>]+>', '', text).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            flowables.append(Paragraph(f"<b>{_safe(clean)}</b>", styles['TR_H3']))
            continue
        if stripped.startswith('### '):
            text = stripped[4:]
            clean = re.sub(r'[*#]', '', text).strip()
            flowables.append(Paragraph(f"<b>{_safe(clean)}</b>", styles['TR_H2']))
            continue
        if stripped.startswith('## '):
            text = stripped[3:]
            clean = re.sub(r'[*#]', '', text).strip()
            flowables.append(Paragraph(f"<b>{_safe(clean)}</b>", styles['TR_H1']))
            continue
        if stripped.startswith('# '):
            text = stripped[2:]
            clean = re.sub(r'[*#]', '', text).strip()
            flowables.append(Paragraph(f"<b>{_safe(clean)}</b>", styles['TR_H1']))
            continue

        # Yatay çizgi
        if stripped in ('---', '***', '___'):
            flowables.append(_section_divider())
            continue

        # Madde işaretleri
        bullet_match = re.match(r'^[-*•]\s+(.+)', stripped)
        if bullet_match:
            text = bullet_match.group(1)
            text = _format_inline(text)
            flowables.append(Paragraph(f"• {text}", styles['TR_Bullet']))
            continue

        # Numaralı liste
        num_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if num_match:
            num = num_match.group(1)
            text = num_match.group(2)
            text = _format_inline(text)
            flowables.append(Paragraph(f"{num}. {text}", styles['TR_Bullet']))
            continue

        # Normal paragraf
        text = _format_inline(stripped)
        flowables.append(Paragraph(text, styles['TR_ReportText']))

    return flowables


def _format_inline(text):
    """Bold ve italic Markdown işaretlerini ReportLab XML'e çevirir."""
    safe = _safe(text)
    # **bold**
    safe = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', safe)
    # *italic*
    safe = re.sub(r'\*(.+?)\*', r'<i>\1</i>', safe)
    # `code`
    safe = re.sub(r'`(.+?)`', r'<font color="#E83E8C">\1</font>', safe)
    # Emoji'leri koru (çoğu DejaVu'da desteklenir)
    return safe


def _add_page_number(canvas_obj, doc):
    """Sayfa numarası ve footer ekler."""
    canvas_obj.saveState()
    page_num = canvas_obj.getPageNumber()

    # Alt çizgi
    canvas_obj.setStrokeColor(BORDER)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(1.5 * cm, 1.2 * cm, A4[0] - 1.5 * cm, 1.2 * cm)

    # Footer text
    canvas_obj.setFont(FONT_NAME, 7)
    canvas_obj.setFillColor(HexColor("#6C757D"))
    canvas_obj.drawString(
        1.5 * cm, 0.8 * cm,
        f"Egitim Check-Up | Psikometrik Degerlendirme Raporu"
    )
    canvas_obj.drawRightString(
        A4[0] - 1.5 * cm, 0.8 * cm,
        f"Sayfa {page_num}"
    )
    canvas_obj.restoreState()


# ============================================================
# ANA PDF ÜRETİCİ
# ============================================================

def generate_student_pdf(student_data, analysis_history, include_charts=True):
    """
    Öğrencinin tüm bilgilerini, test sonuçlarını ve AI raporlarını
    tek bir PDF dosyasına dönüştürür.

    Args:
        student_data: dict — {"info": StudentInfo, "tests": [...]}
        analysis_history: list — get_student_analysis_history() çıktısı
        include_charts: bool — Grafikleri dahil et (matplotlib figürlerini image olarak)

    Returns:
        io.BytesIO — PDF dosya buffer'ı
    """
    info = student_data["info"]
    tests = student_data["tests"]
    styles = _get_styles()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        title=f"{info.name} - Egitim Check-Up Raporu",
        author="Egitim Check-Up Sistemi",
    )

    story = []

    # ──────────────────────────────────────
    # KAPAK / BAŞLIK
    # ──────────────────────────────────────
    story.append(Spacer(1, 1.5 * cm))

    # Logo / Başlık kutusu
    cover_data = [[
        Paragraph(
            '<b>EGITIM CHECK-UP</b>',
            ParagraphStyle('cover', fontName=FONT_BOLD, fontSize=24, textColor=PRIMARY, alignment=TA_CENTER)
        )
    ]]
    cover_table = Table(cover_data, colWidths=[17.5 * cm])
    cover_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LINEBELOW', (0, 0), (-1, -1), 2, PRIMARY),
        ('LINEABOVE', (0, 0), (-1, -1), 2, PRIMARY),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Kisisel Egitim &amp; Kariyer Analiz Merkezi", styles['TR_Subtitle']))
    story.append(Spacer(1, 1 * cm))

    # Öğrenci adı büyük
    story.append(Paragraph(
        f"<b>{_safe(info.name)}</b>",
        ParagraphStyle('name', fontName=FONT_BOLD, fontSize=18, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=6)
    ))
    story.append(Paragraph("Psikometrik Degerlendirme Raporu", styles['TR_Subtitle']))

    story.append(Spacer(1, 1 * cm))

    # Rapor tarihi
    now = datetime.now()
    story.append(Paragraph(
        f"Rapor Tarihi: {now.strftime('%d.%m.%Y %H:%M')}",
        ParagraphStyle('date', fontName=FONT_NAME, fontSize=10, textColor=HexColor("#6C757D"), alignment=TA_CENTER)
    ))

    story.append(PageBreak())

    # ──────────────────────────────────────
    # BÖLÜM 1: KISISEL BILGILER
    # ──────────────────────────────────────
    story.append(_header_bar("BOLUM 1: OGRENCI PROFILI", styles))
    story.append(Spacer(1, 8))

    grade_val = getattr(info, 'grade', None)
    grade_text = f"{grade_val}. Sinif" if grade_val else "Belirtilmemis"

    profile_rows = [
        ["Ad Soyad", str(info.name)],
        ["Yas", str(info.age)],
        ["Cinsiyet", str(info.gender)],
        ["Sinif", grade_text],
        ["E-posta / Kullanici", str(info.username)],
        ["Toplam Giris", str(info.login_count)],
        ["Cozulen Test Sayisi", str(len(tests))],
    ]

    # Profil tablosu
    profile_table_data = []
    for label, value in profile_rows:
        profile_table_data.append([
            Paragraph(f"<b>{_safe(label)}</b>", styles['TR_TableCell']),
            Paragraph(_safe(value), styles['TR_TableCell']),
        ])

    profile_table = Table(profile_table_data, colWidths=[5 * cm, 12.5 * cm])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(profile_table)

    # Test listesi özet
    if tests:
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Tamamlanan Testler:</b>", styles['TR_H2']))

        test_summary_data = [[
            Paragraph("<b>No</b>", styles['TR_TableHeader']),
            Paragraph("<b>Test Adi</b>", styles['TR_TableHeader']),
            Paragraph("<b>Tarih</b>", styles['TR_TableHeader']),
        ]]
        for i, t in enumerate(tests, 1):
            test_summary_data.append([
                Paragraph(str(i), styles['TR_TableCellCenter']),
                Paragraph(_safe(t["test_name"]), styles['TR_TableCell']),
                Paragraph(str(t.get("date", "-")), styles['TR_TableCellCenter']),
            ])

        test_table = Table(test_summary_data, colWidths=[1.5 * cm, 11 * cm, 5 * cm])
        test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_LIGHT]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(test_table)

    story.append(PageBreak())

    # ──────────────────────────────────────
    # BÖLÜM 2: TEST SONUÇLARI (Puan Detayları + Sistem Raporları)
    # ──────────────────────────────────────
    story.append(_header_bar("BOLUM 2: TEST SONUCLARI VE PUAN DETAYLARI", styles))
    story.append(Spacer(1, 8))

    if not tests:
        story.append(Paragraph("Henuz test sonucu bulunmamaktadir.", styles['TR_Body']))
    else:
        for idx, t in enumerate(tests):
            # Test başlığı
            test_title_data = [[
                Paragraph(
                    f"<b>{idx+1}. {_safe(t['test_name'])}</b> &nbsp; | &nbsp; Tarih: {t.get('date', '-')}",
                    ParagraphStyle('th', fontName=FONT_BOLD, fontSize=9.5, textColor=white, alignment=TA_LEFT)
                )
            ]]
            test_title_table = Table(test_title_data, colWidths=[17.5 * cm])
            test_title_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), SECONDARY),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(Spacer(1, 8))
            story.append(test_title_table)
            story.append(Spacer(1, 6))

            # Puan tablosu
            if t.get("scores") and isinstance(t["scores"], dict):
                scores = t["scores"]
                score_data = [[
                    Paragraph("<b>Olcek / Boyut</b>", styles['TR_TableHeader']),
                    Paragraph("<b>Puan / Deger</b>", styles['TR_TableHeader']),
                ]]
                for k, v in scores.items():
                    score_data.append([
                        Paragraph(_safe(str(k)), styles['TR_TableCell']),
                        Paragraph(_safe(str(v)), styles['TR_TableCellCenter']),
                    ])

                score_table = Table(score_data, colWidths=[10 * cm, 7.5 * cm])
                score_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
                    ('TEXTCOLOR', (0, 0), (-1, 0), white),
                    ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_LIGHT]),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(score_table)
                story.append(Spacer(1, 6))

            # Sistem raporu (test_data.py'deki otomatik rapor)
            report_text = t.get("report", "")
            if report_text:
                story.append(Paragraph("<b>Sistem Raporu:</b>", styles['TR_H3']))
                report_flowables = _markdown_to_flowables(report_text, styles)
                story.extend(report_flowables)

            story.append(_section_divider())

    story.append(PageBreak())

    # ──────────────────────────────────────
    # BÖLÜM 3: AI ANALIZ RAPORLARI
    # ──────────────────────────────────────
    story.append(_header_bar("BOLUM 3: AI DESTEKLI ANALIZ RAPORLARI (Claude)", styles))
    story.append(Spacer(1, 8))

    if not analysis_history:
        story.append(Paragraph(
            "Bu ogrenci icin henuz AI destekli analiz raporu olusturulmamistir.",
            styles['TR_Body']
        ))
    else:
        story.append(Paragraph(
            f"Toplam <b>{len(analysis_history)}</b> adet AI analiz raporu bulunmaktadir.",
            styles['TR_Body']
        ))
        story.append(Spacer(1, 8))

        for idx, record in enumerate(analysis_history):
            # Rapor başlığı
            combo = record.get('combination', 'Bilinmiyor')
            date = record.get('date', '-')

            report_header_data = [[
                Paragraph(
                    f"<b>AI Rapor {idx+1}: {_safe(combo)}</b> &nbsp; | &nbsp; {date}",
                    ParagraphStyle('rh', fontName=FONT_BOLD, fontSize=9.5, textColor=white, alignment=TA_LEFT)
                )
            ]]
            report_header = Table(report_header_data, colWidths=[17.5 * cm])
            report_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), ACCENT),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(report_header)
            story.append(Spacer(1, 6))

            # Rapor içeriği (Markdown → flowable)
            report_content = record.get('report', '')
            if report_content:
                flowables = _markdown_to_flowables(report_content, styles)
                story.extend(flowables)
            else:
                story.append(Paragraph("<i>Rapor icerigi bos.</i>", styles['TR_Body']))

            story.append(Spacer(1, 8))
            story.append(_section_divider())

            # Son rapor değilse sayfa sonu
            if idx < len(analysis_history) - 1:
                story.append(PageBreak())

    # ──────────────────────────────────────
    # FOOTER NOTU
    # ──────────────────────────────────────
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=8))

    disclaimer = (
        "Bu rapor, EGITIM CHECK-UP psikometrik degerlendirme sistemi tarafindan, "
        "yapay zeka destekli analiz altyapisiyla uretilmistir. Raporda yer alan "
        "tum yorumlar, ogrencinin psikometrik test verilerine dayanmaktadir. "
        "Bu rapor klinik tani icermez ve klinik degerlendirme yerine gecmez."
    )
    story.append(Paragraph(disclaimer, styles['TR_Small']))
    story.append(Paragraph(
        f"Rapor uretim tarihi: {now.strftime('%d.%m.%Y %H:%M')} | Egitim Check-Up v2.0",
        styles['TR_Small']
    ))

    # Build PDF
    doc.build(story, onFirstPage=_add_page_number, onLaterPages=_add_page_number)
    buffer.seek(0)
    return buffer


def generate_student_pdf_filename(student_name):
    """PDF dosya adı üretir."""
    safe_name = student_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    return f"{safe_name}_Rapor_{timestamp}.pdf"
