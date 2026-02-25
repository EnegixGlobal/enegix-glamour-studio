import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_software.settings")  
django.setup()

from dashboard_app.models import Service  # 👈 apna app name

# ===============================
# SERVICE SEED DATA
# 42+ Services - 7 Categories x 6 Services each
# Series wise insert: SRV001 se start
# ===============================

SERVICE_DATA = [

    # ================================================================
    # 1. HAIR SERVICES (6 services)
    # ================================================================
    {
        "service_name": "Haircut & Styling",
        "category": "hair_service",
        "duration_minutes": 45,
        "base_price": 299,
        "description": "Professional haircut tailored to your face shape and style preference. Includes wash, cut, blow dry and basic styling for a fresh and polished look.",
        "display_on_website": True,
    },
    {
        "service_name": "Hair Wash & Blow Dry",
        "category": "hair_service",
        "duration_minutes": 30,
        "base_price": 199,
        "description": "Deep cleansing hair wash with premium shampoo and conditioner followed by professional blow dry for smooth, shiny and voluminous hair.",
        "display_on_website": True,
    },
    {
        "service_name": "Hair Coloring",
        "category": "hair_service",
        "duration_minutes": 120,
        "base_price": 999,
        "description": "Full hair coloring service using premium quality hair color brands. Includes root to tip application, processing time, wash and basic styling. Price varies by hair length.",
        "display_on_website": True,
    },
    {
        "service_name": "Keratin Treatment",
        "category": "hair_service",
        "duration_minutes": 180,
        "base_price": 2499,
        "description": "Professional keratin smoothing treatment that eliminates frizz and adds intense shine. Results last up to 3-4 months. Includes wash, treatment application and blow dry.",
        "display_on_website": True,
    },
    {
        "service_name": "Hair Spa",
        "category": "hair_service",
        "duration_minutes": 60,
        "base_price": 599,
        "description": "Relaxing and rejuvenating hair spa treatment with deep conditioning mask, scalp massage, steaming and nourishing serum application for healthy and lustrous hair.",
        "display_on_website": True,
    },
    {
        "service_name": "Highlights & Balayage",
        "category": "hair_service",
        "duration_minutes": 150,
        "base_price": 1999,
        "description": "Expert highlighting or balayage technique to add dimension and brightness to your hair. Creates a natural sun-kissed effect. Includes toning, wash and styling.",
        "display_on_website": True,
    },

    # ================================================================
    # 2. BEAUTY & SKIN CARE SERVICES (6 services)
    # ================================================================
    {
        "service_name": "Basic Facial",
        "category": "beauty_service",
        "duration_minutes": 60,
        "base_price": 499,
        "description": "Classic facial treatment including deep cleansing, steam, exfoliation, blackhead removal, face massage and moisturizing mask. Perfect for glowing and refreshed skin.",
        "display_on_website": True,
    },
    {
        "service_name": "Gold Facial",
        "category": "beauty_service",
        "duration_minutes": 75,
        "base_price": 999,
        "description": "Luxurious gold facial using premium VLCC gold kit. Provides intense hydration, reduces fine lines and gives an instant radiant glow. Ideal for special occasions.",
        "display_on_website": True,
    },
    {
        "service_name": "Full Body Waxing",
        "category": "beauty_service",
        "duration_minutes": 90,
        "base_price": 1299,
        "description": "Complete full body waxing using Rica or Nads premium wax for smooth and long-lasting hair removal. Includes legs, arms, underarms and stomach.",
        "display_on_website": True,
    },
    {
        "service_name": "Eyebrow Threading & Shaping",
        "category": "beauty_service",
        "duration_minutes": 15,
        "base_price": 79,
        "description": "Precise eyebrow threading and shaping to define and frame your face beautifully. Done by expert beauticians for clean, symmetrical and well-arched brows.",
        "display_on_website": True,
    },
    {
        "service_name": "Detan Treatment",
        "category": "beauty_service",
        "duration_minutes": 45,
        "base_price": 699,
        "description": "Professional detan treatment using O3+ detan pack to remove sun tan, lighten skin tone and restore natural complexion. Covers face, neck, hands and arms.",
        "display_on_website": True,
    },
    {
        "service_name": "Bleach & Cleanup",
        "category": "beauty_service",
        "duration_minutes": 50,
        "base_price": 399,
        "description": "Gentle bleaching treatment to lighten facial hair and even skin tone, followed by a refreshing cleanup with exfoliation and moisturizing for clean and bright skin.",
        "display_on_website": True,
    },

    # ================================================================
    # 3. MAKEUP SERVICES (6 services)
    # ================================================================
    {
        "service_name": "Party Makeup",
        "category": "makeup_service",
        "duration_minutes": 60,
        "base_price": 1499,
        "description": "Stunning party makeup look using premium brands like Lakme, Maybelline and L'Oreal. Includes base prep, eye makeup, contouring, highlighter and long-lasting finish.",
        "display_on_website": True,
    },
    {
        "service_name": "Engagement Makeup",
        "category": "makeup_service",
        "duration_minutes": 90,
        "base_price": 2999,
        "description": "Elegant and photo-ready engagement makeup with flawless base, defined eyes and perfectly lined lips. Designed to look stunning in photographs and last all day.",
        "display_on_website": True,
    },
    {
        "service_name": "Airbrush Makeup",
        "category": "makeup_service",
        "duration_minutes": 90,
        "base_price": 3499,
        "description": "Premium airbrush makeup technique for an ultra-smooth, flawless and long-lasting finish. Perfect for photography, weddings and events. Lightweight and transfer-resistant.",
        "display_on_website": True,
    },
    {
        "service_name": "Natural Day Makeup",
        "category": "makeup_service",
        "duration_minutes": 45,
        "base_price": 999,
        "description": "Light and natural daytime makeup for a fresh-faced, polished look. Ideal for office, casual outings or daily use. Focuses on skin-like finish with minimal product.",
        "display_on_website": True,
    },
    {
        "service_name": "HD Makeup",
        "category": "makeup_service",
        "duration_minutes": 75,
        "base_price": 2499,
        "description": "High-definition makeup using HD products that look flawless on camera and in person. Perfect for photoshoots, videos and high-profile events.",
        "display_on_website": True,
    },
    {
        "service_name": "Saree Draping with Makeup",
        "category": "makeup_service",
        "duration_minutes": 75,
        "base_price": 1999,
        "description": "Complete look package including professional saree draping in your preferred style along with elegant makeup to create a stunning traditional or fusion look.",
        "display_on_website": True,
    },

    # ================================================================
    # 4. SPA & MASSAGE SERVICES (6 services)
    # ================================================================
    {
        "service_name": "Full Body Massage",
        "category": "spa_service",
        "duration_minutes": 60,
        "base_price": 1499,
        "description": "Relaxing full body massage using aromatic oils to relieve muscle tension, reduce stress and improve blood circulation. Choose from Swedish or deep tissue technique.",
        "display_on_website": True,
    },
    {
        "service_name": "Head Massage",
        "category": "spa_service",
        "duration_minutes": 30,
        "base_price": 399,
        "description": "Soothing head and scalp massage using warm oil to relieve headaches, reduce stress and promote hair growth. Deeply relaxing and rejuvenating experience.",
        "display_on_website": True,
    },
    {
        "service_name": "Back & Shoulder Massage",
        "category": "spa_service",
        "duration_minutes": 45,
        "base_price": 799,
        "description": "Targeted back and shoulder massage to release tension, reduce pain and improve posture. Perfect for those with desk jobs or chronic back discomfort.",
        "display_on_website": True,
    },
    {
        "service_name": "Foot Reflexology",
        "category": "spa_service",
        "duration_minutes": 45,
        "base_price": 699,
        "description": "Therapeutic foot reflexology massage that stimulates pressure points to promote relaxation, improve circulation and relieve body fatigue. Includes foot soak.",
        "display_on_website": True,
    },
    {
        "service_name": "Aroma Therapy Session",
        "category": "spa_service",
        "duration_minutes": 75,
        "base_price": 1799,
        "description": "Holistic aromatherapy massage using essential oils blended to your needs - relaxing, energizing or balancing. Full body treatment for mind, body and soul wellness.",
        "display_on_website": True,
    },
    {
        "service_name": "De-stress Body Wrap",
        "category": "spa_service",
        "duration_minutes": 90,
        "base_price": 2199,
        "description": "Luxurious body wrap treatment with exfoliation, nourishing mask application and wrap to detoxify skin, hydrate deeply and leave body feeling silky smooth.",
        "display_on_website": True,
    },

    # ================================================================
    # 5. NAIL CARE SERVICES (6 services)
    # ================================================================
    {
        "service_name": "Basic Manicure",
        "category": "nail_service",
        "duration_minutes": 30,
        "base_price": 299,
        "description": "Classic manicure including nail shaping, cuticle care, hand soak, exfoliation, hand massage and nail paint application of your choice.",
        "display_on_website": True,
    },
    {
        "service_name": "Basic Pedicure",
        "category": "nail_service",
        "duration_minutes": 45,
        "base_price": 399,
        "description": "Relaxing pedicure with foot soak, scrubbing, callus removal, cuticle cleaning, foot massage and nail paint application for soft and beautiful feet.",
        "display_on_website": True,
    },
    {
        "service_name": "Gel Nail Extensions",
        "category": "nail_service",
        "duration_minutes": 90,
        "base_price": 1299,
        "description": "Professional gel nail extension service to add length and strength to your nails. Includes shaping, gel application and nail art or solid color of your choice.",
        "display_on_website": True,
    },
    {
        "service_name": "Nail Art",
        "category": "nail_service",
        "duration_minutes": 45,
        "base_price": 499,
        "description": "Creative and intricate nail art designs using premium nail paints, glitters, stickers and tools. From simple patterns to detailed artwork based on your preference.",
        "display_on_website": True,
    },
    {
        "service_name": "Spa Manicure & Pedicure Combo",
        "category": "nail_service",
        "duration_minutes": 90,
        "base_price": 899,
        "description": "Complete spa manicure and pedicure combo with luxurious treatment including scrub, massage, mask and nail paint. Best value for hands and feet together.",
        "display_on_website": True,
    },
    {
        "service_name": "Gel Polish Application",
        "category": "nail_service",
        "duration_minutes": 30,
        "base_price": 399,
        "description": "Long-lasting gel polish application on natural nails for a chip-free, glossy finish that lasts up to 3 weeks. Huge range of colors available to choose from.",
        "display_on_website": True,
    },

    # ================================================================
    # 6. BRIDAL PACKAGES (6 services)
    # ================================================================
    {
        "service_name": "Bridal Makeup Package",
        "category": "bridal_service",
        "duration_minutes": 180,
        "base_price": 9999,
        "description": "Complete bridal makeup package for the big day including pre-bridal consultation, HD or airbrush base, detailed eye makeup, contouring, and long-lasting finish that lasts all day.",
        "display_on_website": True,
    },
    {
        "service_name": "Pre-Bridal Grooming Package",
        "category": "bridal_service",
        "duration_minutes": 240,
        "base_price": 7999,
        "description": "Comprehensive pre-bridal package to be done 1-2 days before wedding. Includes full body waxing, facial, detan, eyebrow threading, manicure and pedicure.",
        "display_on_website": True,
    },
    {
        "service_name": "Bridal Hair Styling",
        "category": "bridal_service",
        "duration_minutes": 120,
        "base_price": 3999,
        "description": "Elegant bridal hair styling including trial session, on-day styling with bun, braids or open hairstyle using premium products for long-lasting hold and shine.",
        "display_on_website": True,
    },
    {
        "service_name": "Mehendi Application",
        "category": "bridal_service",
        "duration_minutes": 180,
        "base_price": 4999,
        "description": "Intricate bridal mehendi design on both hands and feet by expert mehendi artists. Includes traditional, Arabic or fusion designs as per your preference.",
        "display_on_website": True,
    },
    {
        "service_name": "Bridal Saree Draping",
        "category": "bridal_service",
        "duration_minutes": 60,
        "base_price": 1999,
        "description": "Expert bridal saree draping in Nivi, Bengali, Gujarati or any regional style with perfect pleating, pinning and finishing touch for a royal and elegant look.",
        "display_on_website": True,
    },
    {
        "service_name": "Complete Bridal Package",
        "category": "bridal_service",
        "duration_minutes": 360,
        "base_price": 24999,
        "description": "All-inclusive complete bridal package covering pre-bridal sessions, bridal makeup, hair styling, saree draping and post-wedding party look. Best value for the bride.",
        "display_on_website": True,
    },

    # ================================================================
    # 7. OTHER SERVICES (6 services)
    # ================================================================
    {
        "service_name": "Ear Piercing",
        "category": "other",
        "duration_minutes": 15,
        "base_price": 199,
        "description": "Safe and hygienic ear piercing service using sterilized equipment. Includes basic aftercare advice and a pair of basic studs to start healing comfortably.",
        "display_on_website": True,
    },
    {
        "service_name": "Eyebrow Microblading Consultation",
        "category": "other",
        "duration_minutes": 30,
        "base_price": 299,
        "description": "One-on-one consultation session for eyebrow microblading or permanent makeup. Understand the process, view sample results and get a personalized treatment plan.",
        "display_on_website": True,
    },
    {
        "service_name": "Eyelash Extension",
        "category": "other",
        "duration_minutes": 90,
        "base_price": 1999,
        "description": "Professional eyelash extension service for fuller, longer and voluminous lashes. Choose from classic, volume or hybrid sets. Lasts 4-6 weeks with proper care.",
        "display_on_website": True,
    },
    {
        "service_name": "Skin Analysis & Consultation",
        "category": "other",
        "duration_minutes": 30,
        "base_price": 199,
        "description": "Expert skin analysis to understand your skin type, concerns and needs. Receive a customized skincare routine and treatment plan from our certified skin specialist.",
        "display_on_website": True,
    },
    {
        "service_name": "Makeup Lesson",
        "category": "other",
        "duration_minutes": 60,
        "base_price": 999,
        "description": "One-on-one personalized makeup lesson to learn techniques suited to your face and skill level. Learn contouring, eye looks, base application and more from our experts.",
        "display_on_website": True,
    },
    {
        "service_name": "Special Occasion Hairstyle",
        "category": "other",
        "duration_minutes": 60,
        "base_price": 799,
        "description": "Customized hairstyling for festivals, parties, graduations or any special event. Includes braid styles, updos, curls or blow-out based on your outfit and preference.",
        "display_on_website": True,
    },
]


def seed_services():
    created = 0
    skipped = 0

    print(f"\n{'='*65}")
    print(f"  Starting Service Seeding...")
    print(f"  Total services to insert: {len(SERVICE_DATA)}")
    print(f"{'='*65}\n")

    for service_data in SERVICE_DATA:
        try:
            # Check if already exists
            if Service.objects.filter(service_name=service_data["service_name"]).exists():
                print(f"  SKIP (already exists): {service_data['service_name']}")
                skipped += 1
                continue

            service = Service.objects.create(
                service_name=service_data["service_name"],
                category=service_data["category"],
                duration_minutes=service_data["duration_minutes"],
                base_price=service_data["base_price"],
                description=service_data["description"],
                display_on_website=service_data["display_on_website"],
                is_active=True
            )
            created += 1
            print(f"  OK {service.service_id} | [{service.get_category_display():<30}] | {service.service_name:<35} | {service.duration_minutes}min | Rs.{service.base_price}")

        except Exception as e:
            print(f"  ERROR [{service_data['service_name']}]: {e}")
            skipped += 1

    print(f"\n{'='*65}")
    print(f"  Successfully Created : {created} services")
    print(f"  Skipped              : {skipped} services")
    print(f"  Total                : {created + skipped} services")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    seed_services()