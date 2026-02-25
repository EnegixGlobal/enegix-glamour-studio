import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_software.settings")
django.setup()

from dashboard_app.models import Vendor, Product, PurchaseEntry, AdminUser

PURCHASE_DATA = [
    # MAKEUP
    {"vendor_id": "VEN001", "product_id": "PRD001", "qty": 50, "price": 310, "date": "2025-11-03", "invoice": "INV-GC-001", "remarks": "Monthly restocking"},
    {"vendor_id": "VEN005", "product_id": "PRD001", "qty": 30, "price": 315, "date": "2025-12-10", "invoice": "INV-RS-001", "remarks": "Urgent stock"},
    {"vendor_id": "VEN001", "product_id": "PRD001", "qty": 40, "price": 310, "date": "2026-01-08", "invoice": "INV-GC-002", "remarks": "January restock"},
    {"vendor_id": "VEN007", "product_id": "PRD001", "qty": 25, "price": 318, "date": "2026-02-05", "invoice": "INV-AC-001", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD002", "qty": 40, "price": 440, "date": "2025-11-05", "invoice": "INV-AC-002", "remarks": "Festive season stock"},
    {"vendor_id": "VEN001", "product_id": "PRD002", "qty": 20, "price": 445, "date": "2025-12-12", "invoice": "INV-GC-003", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD002", "qty": 35, "price": 440, "date": "2026-01-15", "invoice": "INV-AC-003", "remarks": "Jan restock"},
    {"vendor_id": "VEN005", "product_id": "PRD002", "qty": 15, "price": 448, "date": "2026-02-10", "invoice": "INV-RS-002", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD003", "qty": 35, "price": 280, "date": "2025-11-07", "invoice": "INV-GC-004", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD003", "qty": 25, "price": 285, "date": "2025-12-15", "invoice": "INV-RS-003", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD003", "qty": 30, "price": 280, "date": "2026-01-10", "invoice": "INV-GC-005", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD003", "qty": 20, "price": 282, "date": "2026-02-08", "invoice": "INV-AC-004", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD004", "qty": 60, "price": 180, "date": "2025-11-10", "invoice": "INV-GC-006", "remarks": "High demand item"},
    {"vendor_id": "VEN007", "product_id": "PRD004", "qty": 40, "price": 182, "date": "2025-12-18", "invoice": "INV-AC-005", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD004", "qty": 50, "price": 180, "date": "2026-01-12", "invoice": "INV-GC-007", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD004", "qty": 30, "price": 185, "date": "2026-02-12", "invoice": "INV-RS-004", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD005", "qty": 25, "price": 570, "date": "2025-11-12", "invoice": "INV-AC-006", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD005", "qty": 20, "price": 575, "date": "2025-12-20", "invoice": "INV-JB-001", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD005", "qty": 25, "price": 570, "date": "2026-01-18", "invoice": "INV-AC-007", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD005", "qty": 15, "price": 578, "date": "2026-02-14", "invoice": "INV-GC-008", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD006", "qty": 45, "price": 185, "date": "2025-11-14", "invoice": "INV-RS-005", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD006", "qty": 30, "price": 188, "date": "2025-12-22", "invoice": "INV-AC-008", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD006", "qty": 35, "price": 185, "date": "2026-01-20", "invoice": "INV-RS-006", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD007", "qty": 35, "price": 215, "date": "2025-11-16", "invoice": "INV-RS-007", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD007", "qty": 20, "price": 218, "date": "2025-12-25", "invoice": "INV-JB-002", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD007", "qty": 25, "price": 215, "date": "2026-01-22", "invoice": "INV-RS-008", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD007", "qty": 15, "price": 220, "date": "2026-02-16", "invoice": "INV-AC-009", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD008", "qty": 20, "price": 500, "date": "2025-11-18", "invoice": "INV-AC-010", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD008", "qty": 15, "price": 505, "date": "2026-01-05", "invoice": "INV-GC-009", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD008", "qty": 18, "price": 500, "date": "2026-02-08", "invoice": "INV-AC-011", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD009", "qty": 30, "price": 500, "date": "2025-11-20", "invoice": "INV-AC-012", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD009", "qty": 20, "price": 505, "date": "2025-12-28", "invoice": "INV-RS-009", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD009", "qty": 25, "price": 500, "date": "2026-01-25", "invoice": "INV-AC-013", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD010", "qty": 40, "price": 300, "date": "2025-11-22", "invoice": "INV-RS-010", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD010", "qty": 30, "price": 305, "date": "2026-01-08", "invoice": "INV-AC-014", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD010", "qty": 25, "price": 300, "date": "2026-02-10", "invoice": "INV-RS-011", "remarks": ""},
    # HAIR CARE
    {"vendor_id": "VEN002", "product_id": "PRD011", "qty": 50, "price": 410, "date": "2025-11-03", "invoice": "INV-SG-001", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD011", "qty": 30, "price": 415, "date": "2025-12-05", "invoice": "INV-MK-001", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD011", "qty": 40, "price": 410, "date": "2026-01-06", "invoice": "INV-SG-002", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD011", "qty": 20, "price": 418, "date": "2026-02-06", "invoice": "INV-JB-003", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD012", "qty": 60, "price": 340, "date": "2025-11-05", "invoice": "INV-SG-003", "remarks": "Best seller"},
    {"vendor_id": "VEN003", "product_id": "PRD012", "qty": 40, "price": 345, "date": "2025-12-08", "invoice": "INV-MK-002", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD012", "qty": 50, "price": 340, "date": "2026-01-10", "invoice": "INV-SG-004", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD012", "qty": 25, "price": 348, "date": "2026-02-08", "invoice": "INV-GT-001", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD013", "qty": 55, "price": 295, "date": "2025-11-08", "invoice": "INV-MK-003", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD013", "qty": 35, "price": 298, "date": "2025-12-12", "invoice": "INV-SG-005", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD013", "qty": 45, "price": 295, "date": "2026-01-14", "invoice": "INV-MK-004", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD013", "qty": 20, "price": 300, "date": "2026-02-10", "invoice": "INV-JB-004", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD014", "qty": 45, "price": 380, "date": "2025-11-10", "invoice": "INV-SG-006", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD014", "qty": 30, "price": 385, "date": "2025-12-15", "invoice": "INV-MK-005", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD014", "qty": 35, "price": 380, "date": "2026-01-16", "invoice": "INV-SG-007", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD015", "qty": 70, "price": 125, "date": "2025-11-12", "invoice": "INV-MK-006", "remarks": "Fast moving"},
    {"vendor_id": "VEN002", "product_id": "PRD015", "qty": 50, "price": 128, "date": "2025-12-18", "invoice": "INV-SG-008", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD015", "qty": 60, "price": 125, "date": "2026-01-18", "invoice": "INV-MK-007", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD015", "qty": 40, "price": 130, "date": "2026-02-12", "invoice": "INV-GT-002", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD016", "qty": 50, "price": 215, "date": "2025-11-14", "invoice": "INV-MK-008", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD016", "qty": 30, "price": 218, "date": "2025-12-20", "invoice": "INV-SG-009", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD016", "qty": 40, "price": 215, "date": "2026-01-20", "invoice": "INV-MK-009", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD017", "qty": 20, "price": 610, "date": "2025-11-16", "invoice": "INV-JB-005", "remarks": "Premium item"},
    {"vendor_id": "VEN002", "product_id": "PRD017", "qty": 12, "price": 618, "date": "2026-01-22", "invoice": "INV-SG-010", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD017", "qty": 10, "price": 610, "date": "2026-02-14", "invoice": "INV-JB-006", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD018", "qty": 80, "price": 105, "date": "2025-11-18", "invoice": "INV-MK-010", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD018", "qty": 60, "price": 108, "date": "2025-12-22", "invoice": "INV-GT-003", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD018", "qty": 70, "price": 105, "date": "2026-01-24", "invoice": "INV-MK-011", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD018", "qty": 50, "price": 108, "date": "2026-02-16", "invoice": "INV-SG-011", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD019", "qty": 35, "price": 370, "date": "2025-11-20", "invoice": "INV-SG-012", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD019", "qty": 20, "price": 375, "date": "2025-12-25", "invoice": "INV-JB-007", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD019", "qty": 25, "price": 370, "date": "2026-01-26", "invoice": "INV-SG-013", "remarks": ""},
    # SKIN CARE
    {"vendor_id": "VEN008", "product_id": "PRD020", "qty": 45, "price": 245, "date": "2025-11-04", "invoice": "INV-GT-004", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD020", "qty": 30, "price": 248, "date": "2025-12-06", "invoice": "INV-DS-001", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD020", "qty": 40, "price": 245, "date": "2026-01-08", "invoice": "INV-GT-005", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD020", "qty": 20, "price": 250, "date": "2026-02-06", "invoice": "INV-JB-008", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD021", "qty": 80, "price": 125, "date": "2025-11-06", "invoice": "INV-GT-006", "remarks": "High demand"},
    {"vendor_id": "VEN003", "product_id": "PRD021", "qty": 60, "price": 128, "date": "2025-12-08", "invoice": "INV-MK-012", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD021", "qty": 70, "price": 125, "date": "2026-01-10", "invoice": "INV-GT-007", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD021", "qty": 50, "price": 128, "date": "2026-02-08", "invoice": "INV-DS-002", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD022", "qty": 30, "price": 440, "date": "2025-11-08", "invoice": "INV-DS-003", "remarks": "Trending"},
    {"vendor_id": "VEN004", "product_id": "PRD022", "qty": 20, "price": 445, "date": "2025-12-10", "invoice": "INV-JB-009", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD022", "qty": 25, "price": 440, "date": "2026-01-12", "invoice": "INV-DS-004", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD022", "qty": 15, "price": 448, "date": "2026-02-10", "invoice": "INV-GT-008", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD023", "qty": 65, "price": 178, "date": "2025-11-10", "invoice": "INV-GT-009", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD023", "qty": 45, "price": 182, "date": "2025-12-12", "invoice": "INV-MK-013", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD023", "qty": 55, "price": 178, "date": "2026-01-14", "invoice": "INV-GT-010", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD023", "qty": 35, "price": 182, "date": "2026-02-12", "invoice": "INV-DS-005", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD024", "qty": 50, "price": 295, "date": "2025-11-12", "invoice": "INV-DS-006", "remarks": "Summer prep"},
    {"vendor_id": "VEN008", "product_id": "PRD024", "qty": 35, "price": 298, "date": "2025-12-14", "invoice": "INV-GT-011", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD024", "qty": 45, "price": 295, "date": "2026-01-16", "invoice": "INV-DS-007", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD024", "qty": 25, "price": 300, "date": "2026-02-14", "invoice": "INV-JB-010", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD025", "qty": 20, "price": 630, "date": "2025-11-14", "invoice": "INV-JB-011", "remarks": "Bridal season"},
    {"vendor_id": "VEN009", "product_id": "PRD025", "qty": 12, "price": 638, "date": "2025-12-16", "invoice": "INV-DS-008", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD025", "qty": 15, "price": 630, "date": "2026-01-18", "invoice": "INV-JB-012", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD026", "qty": 25, "price": 770, "date": "2025-11-16", "invoice": "INV-JB-013", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD026", "qty": 15, "price": 778, "date": "2025-12-18", "invoice": "INV-DS-009", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD026", "qty": 18, "price": 770, "date": "2026-01-20", "invoice": "INV-JB-014", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD027", "qty": 70, "price": 105, "date": "2025-11-18", "invoice": "INV-GT-012", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD027", "qty": 50, "price": 108, "date": "2025-12-20", "invoice": "INV-MK-014", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD027", "qty": 60, "price": 105, "date": "2026-01-22", "invoice": "INV-GT-013", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD028", "qty": 40, "price": 310, "date": "2025-11-20", "invoice": "INV-DS-010", "remarks": ""},
    {"vendor_id": "VEN004", "product_id": "PRD028", "qty": 25, "price": 315, "date": "2025-12-22", "invoice": "INV-JB-015", "remarks": ""},
    {"vendor_id": "VEN009", "product_id": "PRD028", "qty": 30, "price": 310, "date": "2026-01-24", "invoice": "INV-DS-011", "remarks": ""},
    # TOOLS
    {"vendor_id": "VEN006", "product_id": "PRD029", "qty": 10, "price": 1280, "date": "2025-11-05", "invoice": "INV-OE-001", "remarks": "Capital item"},
    {"vendor_id": "VEN010", "product_id": "PRD029", "qty": 6,  "price": 1290, "date": "2025-12-10", "invoice": "INV-MB-001", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD029", "qty": 8,  "price": 1280, "date": "2026-01-15", "invoice": "INV-OE-002", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD030", "qty": 10, "price": 960,  "date": "2025-11-08", "invoice": "INV-OE-003", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD030", "qty": 8,  "price": 968,  "date": "2025-12-12", "invoice": "INV-MB-002", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD030", "qty": 6,  "price": 960,  "date": "2026-01-18", "invoice": "INV-OE-004", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD030", "qty": 5,  "price": 968,  "date": "2026-02-15", "invoice": "INV-MB-003", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD031", "qty": 8,  "price": 1130, "date": "2025-11-10", "invoice": "INV-OE-005", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD031", "qty": 5,  "price": 1140, "date": "2025-12-15", "invoice": "INV-MB-004", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD031", "qty": 6,  "price": 1130, "date": "2026-01-20", "invoice": "INV-OE-006", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD032", "qty": 6,  "price": 1130, "date": "2025-11-12", "invoice": "INV-MB-005", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD032", "qty": 4,  "price": 1138, "date": "2025-12-18", "invoice": "INV-OE-007", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD032", "qty": 5,  "price": 1130, "date": "2026-01-22", "invoice": "INV-MB-006", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD033", "qty": 6,  "price": 960,  "date": "2025-11-14", "invoice": "INV-MB-007", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD033", "qty": 4,  "price": 968,  "date": "2025-12-20", "invoice": "INV-OE-008", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD033", "qty": 4,  "price": 960,  "date": "2026-01-24", "invoice": "INV-MB-008", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD034", "qty": 10, "price": 830,  "date": "2025-11-16", "invoice": "INV-OE-009", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD034", "qty": 8,  "price": 838,  "date": "2025-12-22", "invoice": "INV-MB-009", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD034", "qty": 6,  "price": 830,  "date": "2026-01-26", "invoice": "INV-OE-010", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD035", "qty": 5,  "price": 1620, "date": "2025-11-18", "invoice": "INV-MB-010", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD035", "qty": 4,  "price": 1630, "date": "2026-01-10", "invoice": "INV-OE-011", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD035", "qty": 3,  "price": 1620, "date": "2026-02-10", "invoice": "INV-MB-011", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD036", "qty": 5,  "price": 1420, "date": "2025-11-20", "invoice": "INV-MB-012", "remarks": ""},
    {"vendor_id": "VEN006", "product_id": "PRD036", "qty": 3,  "price": 1430, "date": "2025-12-25", "invoice": "INV-OE-012", "remarks": ""},
    {"vendor_id": "VEN010", "product_id": "PRD036", "qty": 4,  "price": 1420, "date": "2026-01-28", "invoice": "INV-MB-013", "remarks": ""},
    # CONSUMABLES
    {"vendor_id": "VEN003", "product_id": "PRD037", "qty": 20, "price": 760, "date": "2025-11-05", "invoice": "INV-MK-015", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD037", "qty": 15, "price": 768, "date": "2025-12-08", "invoice": "INV-RS-012", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD037", "qty": 18, "price": 760, "date": "2026-01-10", "invoice": "INV-MK-016", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD037", "qty": 12, "price": 765, "date": "2026-02-08", "invoice": "INV-SG-014", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD038", "qty": 100,"price": 148, "date": "2025-11-07", "invoice": "INV-SG-015", "remarks": "Daily use"},
    {"vendor_id": "VEN003", "product_id": "PRD038", "qty": 80, "price": 152, "date": "2025-12-10", "invoice": "INV-MK-017", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD038", "qty": 90, "price": 148, "date": "2026-01-12", "invoice": "INV-SG-016", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD038", "qty": 70, "price": 152, "date": "2026-02-10", "invoice": "INV-GT-014", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD039", "qty": 120,"price": 70,  "date": "2025-11-09", "invoice": "INV-SG-017", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD039", "qty": 100,"price": 72,  "date": "2025-12-12", "invoice": "INV-MK-018", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD039", "qty": 110,"price": 70,  "date": "2026-01-14", "invoice": "INV-SG-018", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD039", "qty": 80, "price": 72,  "date": "2026-02-12", "invoice": "INV-GT-015", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD040", "qty": 150,"price": 48,  "date": "2025-11-11", "invoice": "INV-SG-019", "remarks": "Bulk order"},
    {"vendor_id": "VEN003", "product_id": "PRD040", "qty": 120,"price": 50,  "date": "2025-12-14", "invoice": "INV-MK-019", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD040", "qty": 130,"price": 48,  "date": "2026-01-16", "invoice": "INV-SG-020", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD040", "qty": 100,"price": 50,  "date": "2026-02-14", "invoice": "INV-GT-016", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD041", "qty": 100,"price": 85,  "date": "2025-11-13", "invoice": "INV-MK-020", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD041", "qty": 80, "price": 88,  "date": "2025-12-16", "invoice": "INV-SG-021", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD041", "qty": 90, "price": 85,  "date": "2026-01-18", "invoice": "INV-MK-021", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD042", "qty": 40, "price": 185, "date": "2025-11-15", "invoice": "INV-MK-022", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD042", "qty": 30, "price": 188, "date": "2025-12-18", "invoice": "INV-SG-022", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD042", "qty": 35, "price": 185, "date": "2026-01-20", "invoice": "INV-MK-023", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD042", "qty": 25, "price": 188, "date": "2026-02-15", "invoice": "INV-GT-017", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD043", "qty": 40, "price": 300, "date": "2025-11-17", "invoice": "INV-MK-024", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD043", "qty": 30, "price": 305, "date": "2025-12-20", "invoice": "INV-SG-023", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD043", "qty": 35, "price": 300, "date": "2026-01-22", "invoice": "INV-MK-025", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD044", "qty": 50, "price": 215, "date": "2025-11-19", "invoice": "INV-GT-018", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD044", "qty": 35, "price": 218, "date": "2025-12-22", "invoice": "INV-SG-024", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD044", "qty": 45, "price": 215, "date": "2026-01-24", "invoice": "INV-GT-019", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD044", "qty": 30, "price": 218, "date": "2026-02-16", "invoice": "INV-MK-026", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD045", "qty": 80, "price": 118, "date": "2025-11-21", "invoice": "INV-GT-020", "remarks": ""},
    {"vendor_id": "VEN002", "product_id": "PRD045", "qty": 60, "price": 120, "date": "2025-12-24", "invoice": "INV-SG-025", "remarks": ""},
    {"vendor_id": "VEN008", "product_id": "PRD045", "qty": 70, "price": 118, "date": "2026-01-26", "invoice": "INV-GT-021", "remarks": ""},
    {"vendor_id": "VEN003", "product_id": "PRD045", "qty": 50, "price": 120, "date": "2026-02-14", "invoice": "INV-MK-027", "remarks": ""},
    # OTHER
    {"vendor_id": "VEN005", "product_id": "PRD046", "qty": 40, "price": 272, "date": "2025-11-05", "invoice": "INV-RS-013", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD046", "qty": 25, "price": 275, "date": "2025-12-08", "invoice": "INV-AC-015", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD046", "qty": 35, "price": 272, "date": "2026-01-10", "invoice": "INV-RS-014", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD046", "qty": 20, "price": 278, "date": "2026-02-08", "invoice": "INV-GC-010", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD047", "qty": 80, "price": 62,  "date": "2025-11-07", "invoice": "INV-GC-011", "remarks": ""},
    {"vendor_id": "VEN005", "product_id": "PRD047", "qty": 60, "price": 65,  "date": "2025-12-10", "invoice": "INV-RS-015", "remarks": ""},
    {"vendor_id": "VEN001", "product_id": "PRD047", "qty": 70, "price": 62,  "date": "2026-01-12", "invoice": "INV-GC-012", "remarks": ""},
    {"vendor_id": "VEN007", "product_id": "PRD047", "qty": 50, "price": 65,  "date": "2026-02-10", "invoice": "INV-AC-016", "remarks": ""},
]


def seed_purchases():
    try:
        admin = AdminUser.objects.filter(role='super_admin').first()
        if not admin:
            admin = AdminUser.objects.first()
        print(f"Admin: {admin}")
    except Exception as e:
        print(f"AdminUser error: {e}")
        admin = None

    created = 0
    skipped = 0

    print(f"\n{'='*65}")
    print(f"  Starting Purchase Entry Seeding...")
    print(f"  Total entries to insert: {len(PURCHASE_DATA)}")
    print(f"{'='*65}\n")

    for entry in PURCHASE_DATA:
        try:
            vendor  = Vendor.objects.get(vendor_id=entry["vendor_id"])
            product = Product.objects.get(product_id=entry["product_id"])
            purchase = PurchaseEntry.objects.create(
                vendor=vendor,
                product=product,
                quantity_purchased=entry["qty"],
                purchase_price=entry["price"],
                purchase_date=entry["date"],
                invoice_number=entry["invoice"],
                remarks=entry.get("remarks", ""),
                added_by=admin
            )
            created += 1
            print(f"  OK {purchase.purchase_id} | {vendor.company_name[:18]:<18} -> {product.product_name[:25]:<25} | Qty:{entry['qty']:>4} | Rs.{entry['price']}")
        except Vendor.DoesNotExist:
            print(f"  ERROR: Vendor not found: {entry['vendor_id']}")
            skipped += 1
        except Product.DoesNotExist:
            print(f"  ERROR: Product not found: {entry['product_id']}")
            skipped += 1
        except Exception as e:
            print(f"  ERROR [{entry['vendor_id']} -> {entry['product_id']}]: {e}")
            skipped += 1

    print(f"\n{'='*65}")
    print(f"  Successfully Created : {created} entries")
    print(f"  Skipped              : {skipped} entries")
    print(f"  Total                : {created + skipped} entries")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    seed_purchases()