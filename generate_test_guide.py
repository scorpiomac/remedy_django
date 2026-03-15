#!/usr/bin/env python3
"""
Génère le guide de test REMEDY au format PDF.
Usage : python generate_test_guide.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem
import datetime

# ── Palette ────────────────────────────────────────────────
BRAND    = colors.HexColor("#1d4ed8")   # bleu principal
BRAND_LT = colors.HexColor("#dbeafe")   # bleu clair
GREEN    = colors.HexColor("#16a34a")
GREEN_LT = colors.HexColor("#dcfce7")
ORANGE   = colors.HexColor("#ea580c")
ORANGE_LT= colors.HexColor("#ffedd5")
RED      = colors.HexColor("#dc2626")
RED_LT   = colors.HexColor("#fee2e2")
GREY     = colors.HexColor("#64748b")
GREY_LT  = colors.HexColor("#f1f5f9")
BLACK    = colors.HexColor("#0f172a")
WHITE    = colors.white

W, H = A4

OUT = "/usr/local/lsws/Example/html/remedy_django/REMEDY_Guide_Test.pdf"

styles = getSampleStyleSheet()

# ── Styles personnalisés ────────────────────────────────────
def S(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

sTitle    = S("sTitle",    fontName="Helvetica-Bold",   fontSize=26, textColor=WHITE,  alignment=TA_CENTER, spaceAfter=4)
sSubtitle = S("sSubtitle", fontName="Helvetica",        fontSize=13, textColor=BRAND_LT, alignment=TA_CENTER, spaceAfter=2)
sH1       = S("sH1",       fontName="Helvetica-Bold",   fontSize=15, textColor=WHITE,  spaceBefore=0, spaceAfter=0)
sH2       = S("sH2",       fontName="Helvetica-Bold",   fontSize=12, textColor=BRAND,  spaceBefore=14, spaceAfter=4, borderPad=0)
sH3       = S("sH3",       fontName="Helvetica-Bold",   fontSize=10, textColor=BLACK,  spaceBefore=8, spaceAfter=3)
sBody     = S("sBody",     fontName="Helvetica",        fontSize=9,  textColor=BLACK,  spaceBefore=2, spaceAfter=2, leading=14)
sNote     = S("sNote",     fontName="Helvetica-Oblique",fontSize=8.5, textColor=GREY, spaceBefore=2, spaceAfter=2, leading=13)
sCode     = S("sCode",     fontName="Courier",          fontSize=8.5, textColor=BLACK,  backColor=GREY_LT, spaceBefore=2, spaceAfter=2, leading=13, leftIndent=8, rightIndent=8)
sBullet   = S("sBullet",   fontName="Helvetica",        fontSize=9,  textColor=BLACK,  spaceBefore=1, spaceAfter=1, leading=13, leftIndent=12, bulletIndent=4)
sWarn     = S("sWarn",     fontName="Helvetica-Bold",   fontSize=9,  textColor=ORANGE, spaceBefore=3, spaceAfter=2)
sOk       = S("sOk",       fontName="Helvetica-Bold",   fontSize=9,  textColor=GREEN,  spaceBefore=3, spaceAfter=2)


def hline():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=4, spaceBefore=4)


def section_header(text):
    """Bloc titre de section coloré."""
    tbl = Table([[Paragraph(text, sH1)]], colWidths=[W - 4*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BRAND),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [BRAND]),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return tbl


def badge(label, bg=BRAND_LT, fg=BRAND):
    s = ParagraphStyle("badge", fontName="Helvetica-Bold", fontSize=8, textColor=fg, backColor=bg)
    return Paragraph(label, s)


def cred_table(rows, col_w=None):
    """Tableau de credentials stylé."""
    col_w = col_w or [4.5*cm, 11.5*cm]
    data = [["Champ", "Valeur"]] + rows
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BRAND),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  9),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 9),
        ("BACKGROUND",    (0,1), (0,-1),  GREY_LT),
        ("FONTNAME",      (0,1), (0,-1),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,1), (0,-1),  9),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_LT]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t


def scenario_table(rows):
    """Tableau des scénarios."""
    header = [
        Paragraph("N°", S("h", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
        Paragraph("Action", S("h", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE)),
        Paragraph("Résultat attendu", S("h", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE)),
        Paragraph("Statut", S("h", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
    ]
    data = [header]
    for r in rows:
        no, action, expected, _ = r
        status_cell = badge("☐ À tester", bg=GREY_LT, fg=GREY)
        data.append([
            Paragraph(str(no), S("c", fontName="Helvetica-Bold", fontSize=9, alignment=TA_CENTER, textColor=BRAND)),
            Paragraph(action, sBody),
            Paragraph(expected, sBody),
            status_cell,
        ])
    t = Table(data, colWidths=[0.9*cm, 6.5*cm, 7.5*cm, 2.1*cm])
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  BRAND),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_LT]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ]
    t.setStyle(TableStyle(style))
    return t


# ════════════════════════════════════════════════════════════
# CONTENU
# ════════════════════════════════════════════════════════════

story = []

# ── PAGE DE COUVERTURE ──────────────────────────────────────
cover = Table(
    [[Paragraph("REMEDY", sTitle)],
     [Paragraph("Plateforme de gestion des réclamations santé", sSubtitle)],
     [Paragraph(" ", sSubtitle)],
     [Paragraph("GUIDE DE TEST — RECETTE FONCTIONNELLE", S("gt", fontName="Helvetica-Bold", fontSize=16, textColor=WHITE, alignment=TA_CENTER))],
     [Paragraph(" ", sSubtitle)],
     [Paragraph(f"Généré le {datetime.date.today().strftime('%d/%m/%Y')}", S("d", fontName="Helvetica", fontSize=10, textColor=BRAND_LT, alignment=TA_CENTER))],
    ],
    colWidths=[W - 4*cm]
)
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), BRAND),
    ("TOPPADDING",    (0,0), (-1,-1), 16),
    ("BOTTOMPADDING", (0,0), (-1,-1), 16),
    ("LEFTPADDING",   (0,0), (-1,-1), 20),
    ("RIGHTPADDING",  (0,0), (-1,-1), 20),
]))
story.append(Spacer(1, 3*cm))
story.append(cover)
story.append(Spacer(1, 1.5*cm))

# Notice sur la page de couverture
notice_data = [
    [Paragraph("URL de test", S("nl", fontName="Helvetica-Bold", fontSize=9, textColor=BRAND)),
     Paragraph("https://remedy.tickets-place.net", S("nv", fontName="Courier-Bold", fontSize=10, textColor=BLACK))],
    [Paragraph("Navigateur recommandé", S("nl", fontName="Helvetica-Bold", fontSize=9, textColor=BRAND)),
     Paragraph("Chrome 120+ ou Firefox 120+ (bureau)", sBody)],
    [Paragraph("Statut du site", S("nl", fontName="Helvetica-Bold", fontSize=9, textColor=BRAND)),
     Paragraph("✅ En ligne — HTTPS valide jusqu'au 21/05/2026", S("nv", fontName="Helvetica", fontSize=9, textColor=GREEN))],
    [Paragraph("Contact technique", S("nl", fontName="Helvetica-Bold", fontSize=9, textColor=BRAND)),
     Paragraph("Équipe dev — remonter les bugs avec capture d'écran + URL + compte utilisé", sBody)],
]
notice = Table(notice_data, colWidths=[4.5*cm, 11.5*cm])
notice.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), BRAND_LT),
    ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#93c5fd")),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(notice)
story.append(PageBreak())

# ── 1. ACCÈS DE TEST ────────────────────────────────────────
story.append(section_header("1. COMPTES DE TEST"))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Chaque compte correspond à un rôle distinct dans l'application. "
    "Le mot de passe est à demander au responsable technique ou à définir avant la campagne de test.",
    sBody
))
story.append(Spacer(1, 6))

accounts = [
    # (Role, Username, Mot de passe, Droits, Couleur)
    ("SUPERADMIN / System Admin",  "admin",      "admin2024!",    "Accès total : configuration, utilisateurs, tous les dossiers, notifications", BRAND, WHITE),
    ("SUPERADMIN (2ᵉ compte)",     "superadmin", "Superadmin2024!","Identique au précédent — permet de tester les actions admin croisées",       BRAND, WHITE),
    ("IPM Admin — IPM SANTE PLUS", "ipmadmin1",  "Ipm2024!",      "Voit tous les dossiers de l'IPM SANTE PLUS ; config formules & règles",      colors.HexColor("#7c3aed"), WHITE),
    ("IPM Admin — FatouIPM",       "fatou",      "Fatou2024!",    "Voit tous les dossiers de FatouIPM",                                          colors.HexColor("#7c3aed"), WHITE),
    ("Prestataire — Médecin",      "doctor1",    "Doctor2024!",   "Crée/soumet ses propres dossiers (patients IPM SANTE PLUS)",                  GREEN, WHITE),
    ("Prestataire — Clinique",     "aminata",    "Aminata2024!",  "Crée/soumet ses propres dossiers (Clinique Espoir)",                          GREEN, WHITE),
    ("Prestataire — Pharmacie",    "pharma",     "Pharma2024!",   "Rôle Pharmacie — même flux que médecin",                                      GREEN, WHITE),
]

for role, username, pwd, rights, bg, fg in accounts:
    block = KeepTogether([
        Table([[Paragraph(f"  {role}", S("rh", fontName="Helvetica-Bold", fontSize=9.5, textColor=fg))]],
              colWidths=[W - 4*cm],
              style=TableStyle([
                  ("BACKGROUND",    (0,0), (-1,-1), bg),
                  ("TOPPADDING",    (0,0), (-1,-1), 6),
                  ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                  ("LEFTPADDING",   (0,0), (-1,-1), 12),
              ])),
        cred_table([
            ["Identifiant", username],
            ["Mot de passe", pwd],
            ["Périmètre",   rights],
        ]),
        Spacer(1, 8),
    ])
    story.append(block)

story.append(Paragraph(
    "⚠️  Avant le test : changer les mots de passe si l'environnement est accessible depuis l'extérieur.",
    sWarn
))
story.append(PageBreak())

# ── 2. DONNÉES DE TEST ──────────────────────────────────────
story.append(section_header("2. DONNÉES EXISTANTES EN BASE"))
story.append(Spacer(1, 8))

story.append(Paragraph("2.1  Patients enregistrés", sH2))
story.append(cred_table([
    ["Moussa Diop",       "N° adhérent M-1001 | IPM : IPM SANTE PLUS | Formule Standard (Consult. 70%, Pharmacie 60%)"],
    ["Aicha Ndiaye",      "N° adhérent M-1002 | IPM : IPM SANTE PLUS | Formule Standard"],
    ["Abbbb xdfxdfx",     "N° adhérent 12 | IPM : FatouIPM | Formule standard (toutes catégories 80%)"],
], col_w=[4*cm, 12*cm]))
story.append(Spacer(1, 8))

story.append(Paragraph("2.2  Dossiers existants (pour tests sans création)", sH2))
story.append(cred_table([
    ["Dossier #1",  "Moussa Diop / Pharmacie | READY_FOR_PAYMENT | Prestataire : doctor1"],
    ["Dossier #2",  "Moussa Diop / Consultation | BLOCKED | Prestataire : doctor1"],
    ["Dossier #4",  "Abbbb xdfxdfx / Consultation | BLOCKED | Prestataire : aminata"],
    ["Dossier #5",  "Abbbb xdfxdfx / Biologie | DRAFT | Prestataire : aminata — peut être soumis"],
    ["Dossier #6",  "Abbbb xdfxdfx / Biologie | READY_FOR_PAYMENT | Prestataire : aminata"],
], col_w=[3*cm, 13*cm]))
story.append(Spacer(1, 8))

story.append(Paragraph("2.3  Établissements & IPM", sH2))
story.append(cred_table([
    ["IPM SANTE PLUS",  "id=1 — 2 patients, plusieurs dossiers"],
    ["FatouIPM",        "id=2 — 1 patient (Abbbb xdfxdfx)"],
    ["Clinique Espoir", "id=1 — Hôpital (type HOSPITAL) — lié à aminata"],
], col_w=[4.5*cm, 11.5*cm]))
story.append(Spacer(1, 8))

story.append(Paragraph("2.4  Catégories disponibles (26 au total)", sH2))
story.append(Paragraph(
    "Consultation, Pharmacie, Consultation générale, Consultation spécialisée, Hospitalisation, "
    "Urgences, Chirurgie, Anesthésie, Imagerie, Radiologie, Échographie, Scanner, IRM, Laboratoire, "
    "Biologie, Analyse sanguine, Soins dentaires, Ophtalmologie, Maternité, Pédiatrie, "
    "Kinésithérapie, Vaccination, Médicaments génériques, Médicaments de marque, "
    "Dispositifs médicaux, Consommables médicaux.",
    sBody
))
story.append(PageBreak())

# ── 3. SCÉNARIOS DE TEST ────────────────────────────────────

# ── 3.1 Authentification ────
story.append(section_header("3. SCÉNARIOS DE TEST"))
story.append(Spacer(1, 6))
story.append(Paragraph("3.1  Authentification", sH2))
story.append(scenario_table([
    (1,  "Se connecter avec <b>admin / admin2024!</b>",
         "Redirection vers le tableau de bord Superadmin — stats globales visibles", ""),
    (2,  "Se connecter avec <b>ipmadmin1 / Ipm2024!</b>",
         "Tableau de bord IPM : dossiers de IPM SANTE PLUS uniquement", ""),
    (3,  "Se connecter avec <b>doctor1 / Doctor2024!</b>",
         "Tableau de bord prestataire : ses dossiers uniquement", ""),
    (4,  "Tenter de se connecter avec un mot de passe erroné",
         "Message d'erreur — pas de redirection", ""),
    (5,  "Accéder à /claims/ sans être connecté",
         "Redirection vers la page de connexion", ""),
    (6,  "Se déconnecter depuis le menu",
         "Session terminée, retour à la page de connexion", ""),
]))
story.append(Spacer(1, 10))

# ── 3.2 Cycle de vie dossier ─
story.append(Paragraph("3.2  Cycle complet d'un dossier de réclamation", sH2))
story.append(Paragraph(
    "Flux : <b>DRAFT → SUBMITTED → LOCKED → PATIENT_CONFIRMED → READY_FOR_PAYMENT</b>. "
    "Connectez-vous avec <b>aminata</b> pour créer, puis avec <b>admin</b> pour suivre.",
    sBody
))
story.append(Spacer(1, 4))
story.append(scenario_table([
    (7,  "Connecté en <b>aminata</b> — cliquer « Nouveau dossier »",
         "Formulaire de création affiché avec sélecteur patient, catégorie, montant", ""),
    (8,  "Saisir : Patient = Abbbb xdfxdfx, Catégorie = Consultation, Montant = 25 000 XOF",
         "Calcul automatique de la couverture (80%) affiché sous le montant", ""),
    (9,  "Sauvegarder le dossier",
         "Dossier créé en statut DRAFT, visible dans la liste", ""),
    (10, "Uploader un document PDF (justificatif)",
         "Document visible dans la section « Documents » de la fiche", ""),
    (11, "Cliquer « Soumettre »",
         "Statut passe à SUBMITTED puis LOCKED automatiquement ; lien patient généré", ""),
    (12, "Vérifier que l'email de notification a été reçu",
         "Email avec les détails du dossier envoyé à l'adresse configurée", ""),
    (13, "Copier l'URL du lien patient depuis la fiche",
         "URL de la forme https://remedy.tickets-place.net/verify/<token>/", ""),
    (14, "Ouvrir le lien patient dans un onglet privé (ou autre navigateur)",
         "Page de validation affiche : patient, montant total, part IPM, part patient", ""),
    (15, "Cliquer « Confirmer »",
         "Statut passe à READY_FOR_PAYMENT ; message de confirmation affiché", ""),
    (16, "Ouvrir le lien patient à nouveau",
         "Message « lien déjà utilisé » ou « lien expiré »", ""),
]))
story.append(Spacer(1, 10))

# ── 3.3 Flux contestation ─────
story.append(Paragraph("3.3  Contestation patient", sH2))
story.append(scenario_table([
    (17, "Soumettre un nouveau dossier (avec doc) en tant que <b>doctor1</b>",
         "Dossier en LOCKED avec lien patient généré", ""),
    (18, "Ouvrir le lien patient — cliquer « Contester »",
         "Champ motif de contestation affiché", ""),
    (19, "Saisir un motif et valider",
         "Statut passe à BLOCKED ; motif enregistré dans la fiche", ""),
    (20, "Connecté en <b>ipmadmin1</b> — vérifier la fiche du dossier bloqué",
         "Dossier visible avec statut BLOCKED et motif de contestation", ""),
]))
story.append(Spacer(1, 10))

# ── 3.4 Permissions ──────────
story.append(Paragraph("3.4  Cloisonnement des rôles (sécurité)", sH2))
story.append(scenario_table([
    (21, "Connecté en <b>doctor1</b> — accéder à la fiche d'un dossier de <b>aminata</b>",
         "Accès refusé (403) ou dossier invisible dans la liste", ""),
    (22, "Connecté en <b>ipmadmin1</b> — accéder à un dossier d'un patient FatouIPM",
         "Accès refusé (403)", ""),
    (23, "Connecté en <b>doctor1</b> — tenter d'accéder à /claims/users/",
         "Redirection ou 403 — page réservée à l'admin", ""),
    (24, "Connecté en <b>fatou</b> — vérifier que seuls les patients FatouIPM sont visibles",
         "Dossier #1 (IPM SANTE PLUS) absent de la liste", ""),
    (25, "Connecté en <b>aminata</b> — tenter de supprimer un dossier LOCKED",
         "Suppression impossible — message d'erreur", ""),
]))
story.append(PageBreak())

# ── 3.5 Administration ────────
story.append(section_header("3. SCÉNARIOS DE TEST (suite)"))
story.append(Spacer(1, 6))
story.append(Paragraph("3.5  Administration — Patients, IPM, Hôpitaux (connecté en <b>admin</b>)", sH2))
story.append(scenario_table([
    (26, "Créer un nouveau patient avec n° adhérent unique, IPM SANTE PLUS",
         "Patient enregistré, apparaît dans la liste et dans le select du formulaire dossier", ""),
    (27, "Modifier le patient créé (changer la formule de couverture)",
         "Modification sauvegardée, dossiers futurs utilisent la nouvelle formule", ""),
    (28, "Créer un nouvel IPM « TestIPM »",
         "IPM visible dans la liste et sélectionnable lors de la création d'un patient", ""),
    (29, "Créer un hôpital / pharmacie avec type = PHARMACIE",
         "Établissement enregistré, sélectionnable dans la fiche utilisateur prestataire", ""),
    (30, "Modifier la fiche hôpital — ajouter un moyen de paiement (ex. Orange Money avec numéro)",
         "Moyen de paiement affiché sur la fiche dossier dans le bloc « Moyens de paiement »", ""),
    (31, "Supprimer l'IPM « TestIPM » créé au scénario 28",
         "IPM supprimé ; les patients associés ne doivent pas être perdus", ""),
]))
story.append(Spacer(1, 10))

# ── 3.6 Gestion des utilisateurs ─
story.append(Paragraph("3.6  Gestion des utilisateurs (connecté en <b>admin</b>)", sH2))
story.append(scenario_table([
    (32, "Créer un compte prestataire avec rôle DOCTOR, lié à Clinique Espoir",
         "Compte créé, utilisateur peut se connecter et créer des dossiers", ""),
    (33, "Créer un compte IPM Admin pour « TestIPM »",
         "Connexion avec ce compte : tableau de bord IPM affiché", ""),
    (34, "Désactiver le compte du prestataire créé",
         "Le compte ne peut plus se connecter (message erreur)", ""),
    (35, "Réactiver le compte",
         "Connexion à nouveau possible", ""),
    (36, "Supprimer un utilisateur test",
         "Compte supprimé de la liste ; ses dossiers restent en base", ""),
]))
story.append(Spacer(1, 10))

# ── 3.7 Formules & règles ─────
story.append(Paragraph("3.7  Formules de couverture & règles (connecté en <b>admin</b>)", sH2))
story.append(scenario_table([
    (37, "Créer une nouvelle formule pour IPM SANTE PLUS : « Formule Premium »",
         "Formule disponible dans la liste et sélectionnable pour un patient", ""),
    (38, "Ajouter une règle : Formule Premium / Hospitalisation / 90%",
         "Règle enregistrée et visible dans la liste des règles", ""),
    (39, "Créer un dossier (catégorie Hospitalisation) pour un patient avec Formule Premium",
         "Calcul de couverture = 90% du montant lors de la soumission", ""),
    (40, "Modifier la règle à 85% puis re-soumettre",
         "Nouveau dossier (DRAFT) prend 85%, les anciens snapshots sont inchangés", ""),
    (41, "Désactiver la règle",
         "Couverture = 0% pour les nouveaux dossiers dans cette catégorie", ""),
]))
story.append(PageBreak())

# ── 3.8 Notifications ─────────
story.append(section_header("3. SCÉNARIOS DE TEST (suite)"))
story.append(Spacer(1, 6))
story.append(Paragraph("3.8  Notifications email (connecté en <b>admin</b>)", sH2))
story.append(scenario_table([
    (42, "Aller dans Notifications → canal EMAIL → Tester",
         "Email de test envoyé à l'adresse configurée ; succès affiché dans la page", ""),
    (43, "Vérifier que l'email de test arrive dans la boîte mail",
         "Email reçu avec les variables correctement remplacées (pas de {{placeholder}} brut)", ""),
    (44, "Modifier le sujet et le corps du message EMAIL",
         "Modifications sauvegardées ; l'email de test utilise le nouveau template", ""),
    (45, "Sur la fiche d'un dossier LOCKED/READY — cliquer « Renvoyer la notification »",
         "Email renvoyé ; entrée ajoutée dans le journal des notifications", ""),
    (46, "Vérifier le journal des notifications dans la fiche dossier",
         "Historique : canal, statut (SUCCESS/FAILURE), date, éventuellement message d'erreur", ""),
    (47, "Saisir une adresse SMTP invalide dans la config — tester",
         "Message d'échec affiché dans l'interface ; aucun crash de l'appli", ""),
]))
story.append(Spacer(1, 10))

# ── 3.9 Moyens de paiement ────
story.append(Paragraph("3.9  Moyens de paiement IPM & établissements (connecté en <b>admin</b>)", sH2))
story.append(scenario_table([
    (48, "Aller dans Moyens de paiement — créer un moyen « Wave » type MOBILE_MONEY",
         "Moyen disponible dans la configuration IPM et hôpital", ""),
    (49, "Sur la fiche IPM SANTE PLUS — ajouter Wave avec numéro 77 000 00 00",
         "Option sauvegardée, visible dans la liste des options IPM", ""),
    (50, "Modifier la fiche Clinique Espoir — ajouter Virement avec IBAN de test",
         "Option établissement sauvegardée", ""),
    (51, "Ouvrir la fiche d'un dossier avec Clinique Espoir comme prestataire (connecté ipmadmin1)",
         "Bloc « Moyens de paiement du prestataire » visible avec Virement IBAN", ""),
    (52, "Ouvrir un dossier sans hôpital lié au prestataire",
         "Bloc absent ou vide — pas d'erreur 500", ""),
]))
story.append(Spacer(1, 10))

# ── 3.10 Documents ────────────
story.append(Paragraph("3.10  Documents justificatifs", sH2))
story.append(scenario_table([
    (53, "Uploader un PDF sur un dossier DRAFT",
         "Document visible dans la liste avec nom, type, date", ""),
    (54, "Uploader une image JPG",
         "Fichier accepté et visible", ""),
    (55, "Tenter de soumettre un dossier SANS document",
         "Erreur : « Au moins un document justificatif est requis »", ""),
    (56, "Uploader plusieurs fichiers en une seule fois",
         "Tous les fichiers sont enregistrés", ""),
]))
story.append(PageBreak())

# ── 3.11 Robustesse ──────────
story.append(section_header("3. SCÉNARIOS DE TEST (suite)"))
story.append(Spacer(1, 6))
story.append(Paragraph("3.11  Robustesse & cas limites", sH2))
story.append(scenario_table([
    (57, "Accéder à /claims/9999/ (dossier inexistant)",
         "Page 404 — pas de 500", ""),
    (58, "Accéder à /verify/FAUX_TOKEN/ (token invalide)",
         "Page de vérification affichant « lien invalide » — pas de 500", ""),
    (59, "Laisser la session inactive 30 min puis accéder à une page protégée",
         "Redirection vers login (session expirée)", ""),
    (60, "Soumettre un formulaire avec un montant négatif ou non numérique",
         "Erreur de validation — formulaire réaffiché avec message d'erreur", ""),
    (61, "Accéder au site avec le nom de domaine https://remedy.tickets-place.net/",
         "Site fonctionnel (HTTP 200), certificat SSL valide", ""),
    (62, "Vérifier le SSL : cadenas vert et certificat Let's Encrypt valide",
         "Cert CN=remedy.tickets-place.net, expire le 21/05/2026", ""),
    (63, "Créer deux patients avec le même numéro d'adhérent",
         "Erreur de validation — numéro unique requis", ""),
    (64, "Modifier un dossier LOCKED en tant que prestataire",
         "Modification refusée — message d'erreur approprié", ""),
]))
story.append(Spacer(1, 10))

# ── 3.12 Journal d'audit ──────
story.append(Paragraph("3.12  Journal d'audit (connecté en <b>admin</b> ou <b>ipmadmin</b>)", sH2))
story.append(scenario_table([
    (65, "Ouvrir la fiche d'un dossier complet (READY_FOR_PAYMENT)",
         "Section Audit Log affiche au moins : CREATED, SUBMITTED, LOCKED, PATIENT_CONFIRMED, READY_FOR_PAYMENT", ""),
    (66, "Vérifier qu'un dossier BLOCKED affiche CLAIM_BLOCKED avec raison",
         "Ligne d'audit avec notes = raison du blocage", ""),
    (67, "Vérifier que chaque action (upload doc, submit, lock) génère une entrée dans le journal",
         "Entrées horodatées avec l'acteur (username) et l'événement", ""),
]))
story.append(PageBreak())

# ── 4. STATUTS & TRANSITIONS ─────────────────────────────────
story.append(section_header("4. RÉFÉRENCE — STATUTS & TRANSITIONS"))
story.append(Spacer(1, 10))

statuts = [
    ["Statut", "Label FR", "Prochaine transition", "Acteur"],
    ["DRAFT", "Brouillon", "SUBMITTED (bouton Soumettre)", "Prestataire"],
    ["SUBMITTED", "Soumis", "LOCKED (automatique à la soumission)", "Système"],
    ["LOCKED", "Verrouillé", "PATIENT_CONFIRMED ou BLOCKED (via lien patient)", "Patient (lien unique)"],
    ["PATIENT_CONFIRMED", "Confirmé patient", "READY_FOR_PAYMENT (automatique)", "Système"],
    ["READY_FOR_PAYMENT", "Prêt au paiement", "— (état final positif)", "—"],
    ["DISPUTED", "Contesté", "BLOCKED (automatique)", "Système"],
    ["BLOCKED", "Bloqué", "— (état final négatif — intervention admin requise)", "—"],
]
st = Table(statuts, colWidths=[3.5*cm, 4*cm, 6*cm, 3.5*cm])
st.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  BRAND),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_LT]),
    ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("FONTNAME",      (0,1), (0,-1),  "Courier-Bold"),
    ("TEXTCOLOR",     (0,5), (0,5),   GREEN),
    ("TEXTCOLOR",     (0,7), (0,7),   RED),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(st)
story.append(Spacer(1, 14))

# ── 5. URLS UTILES ────────────────────────────────────────────
story.append(Paragraph("5. URLS UTILES DE L'APPLICATION", sH2))
BASE = "https://remedy.tickets-place.net"
urls_data = [
    ["Page", "URL"],
    ["Connexion",                   f"{BASE}/accounts/login/"],
    ["Tableau de bord",             f"{BASE}/"],
    ["Liste des dossiers",          f"{BASE}/claims/"],
    ["Créer un dossier",            f"{BASE}/claims/create/"],
    ["Liste des patients",          f"{BASE}/claims/patients/"],
    ["Créer un patient",            f"{BASE}/claims/patients/create/"],
    ["Liste des IPM",               f"{BASE}/claims/ipms/"],
    ["Liste des hôpitaux",          f"{BASE}/claims/hospitals/"],
    ["Formules de couverture",      f"{BASE}/claims/formules/"],
    ["Règles de couverture",        f"{BASE}/claims/coverage-rules/"],
    ["Catégories",                  f"{BASE}/claims/categories/"],
    ["Moyens de paiement",          f"{BASE}/claims/payment-methods/"],
    ["Gestion des utilisateurs",    f"{BASE}/claims/users/"],
    ["Notifications",               f"{BASE}/claims/notifications/"],
]
ut = Table(urls_data, colWidths=[6*cm, 11*cm])
ut.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  BRAND),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_LT]),
    ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("FONTNAME",      (0,1), (1,-1),  "Courier"),
    ("FONTSIZE",      (0,1), (1,-1),  8),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(ut)
story.append(PageBreak())

# ── 6. FICHE DE RELEVÉ DES BUGS ──────────────────────────────
story.append(section_header("6. FICHE DE RELEVÉ DES BUGS"))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Pour chaque anomalie constatée, renseigner une ligne du tableau ci-dessous "
    "et transmettre à l'équipe de développement avec capture d'écran.",
    sBody
))
story.append(Spacer(1, 8))

bug_header = ["N°", "Scénario\ntesté", "URL", "Compte\nutilisé", "Description de l'anomalie", "Criticité\n(1-3)", "Statut"]
bug_rows = [bug_header] + [
    [str(i), "", "", "", "", "", "Ouvert"] for i in range(1, 16)
]
bt = Table(bug_rows, colWidths=[0.7*cm, 1.6*cm, 4*cm, 2*cm, 5.8*cm, 1.4*cm, 1.5*cm])
bt.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  BRAND),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,0),  8),
    ("FONTSIZE",      (0,1), (-1,-1), 8),
    ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GREY_LT]),
    ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ("LEFTPADDING",   (0,0), (-1,-1), 5),
    ("RIGHTPADDING",  (0,0), (-1,-1), 5),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("ALIGN",         (0,0), (0,-1),  "CENTER"),
]))
story.append(bt)
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Criticité : <b>1</b> = Bloquant (empêche un flux complet) | <b>2</b> = Majeur (fonctionnalité altérée) | <b>3</b> = Mineur (cosmétique / UX)",
    sNote
))
story.append(Spacer(1, 14))
story.append(hline())
story.append(Spacer(1, 6))
story.append(Paragraph(
    f"REMEDY — Guide de Test — Généré le {datetime.date.today().strftime('%d %B %Y')} — Confidentiel",
    S("footer", fontName="Helvetica-Oblique", fontSize=8, textColor=GREY, alignment=TA_CENTER)
))

# ════════════════════════════════════════════════════════════
# GÉNÉRATION
# ════════════════════════════════════════════════════════════

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawRightString(W - 1.5*cm, 1.2*cm, f"Page {doc.page}")
    canvas.drawString(1.5*cm, 1.2*cm, "REMEDY — Guide de Test — Confidentiel")
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="REMEDY – Guide de Test",
    author="Équipe REMEDY",
)
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF généré : {OUT}")
