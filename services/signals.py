import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
from services.models import ServiceBooking

@receiver(post_save, sender=ServiceBooking)
def send_service_booking_alert(sender, instance, created, **kwargs):
    if created:  # Only when new booking is created

        subject = f"New Service Booking: Carbon Craft Studio #{instance.id}"

        message = (
            f"You have a new service booking!\n\n"
            f"Customer: {instance.first_name} {instance.last_name}\n"
            f"Service: {instance.service.service_name}\n"
            f"Price: Rs. {instance.service.price}\n"
            f"Date: {instance.booking_date}\n"
            f"Time: {instance.booking_time}\n"
            f"Phone: {instance.phone}\n"
            f"Email: {instance.email}\n"
            f"Address: {instance.address}\n"
            f"Car: {instance.notes}\n\n"
            f"Check admin panel for full details."
        )

        send_mail(
            subject,
            message,
            instance.email,   # From email
            ['carboncraftstudio4@gmail.com'], # Admin email
            fail_silently=False,
        )

        # Generate PDF receipt in a card format
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Dimensions for the card
        card_x = 50
        card_y = 400
        card_w = 512
        card_h = 350
        
        # Draw shadow
        p.setFillColorRGB(0.85, 0.85, 0.85)
        p.roundRect(card_x + 5, card_y - 5, card_w, card_h, 15, fill=1, stroke=0)
        
        # Draw main card
        p.setFillColor(colors.white)
        p.setStrokeColorRGB(0.8, 0.8, 0.8)
        p.roundRect(card_x, card_y, card_w, card_h, 15, fill=1, stroke=1)
        
        # Draw Title (Header)
        p.setFont("Helvetica-Bold", 18)
        p.setFillColor(colors.red)
        title_part1 = "Carbon Craft Studio "
        p.drawString(card_x + 30, card_y + card_h - 40, title_part1)
        p.setFillColor(colors.black)
        title_width = p.stringWidth(title_part1, "Helvetica-Bold", 18)
        p.drawString(card_x + 30 + title_width, card_y + card_h - 40, "- Booking Receipt")
        
        # Line separator under header
        p.setStrokeColorRGB(0.9, 0.9, 0.9)
        p.line(card_x + 30, card_y + card_h - 55, card_x + card_w - 30, card_y + card_h - 55)
        
        # Details text
        p.setFont("Helvetica", 12)
        y = card_y + card_h - 85
        details = [
            f"Booking ID: #{instance.id}",
            f"Customer Name: {instance.first_name} {instance.last_name}",
            f"Service: {instance.service.service_name}",
            f"Price: Rs. {instance.service.price}",
            f"Booking Date: {instance.booking_date}",
            f"Booking Time: {instance.booking_time}",
            f"Phone: {instance.phone}",
            f"Address: {instance.address}",
            f"Car: {instance.notes}"
        ]
        
        p.setFillColor(colors.black)
        for detail in details:
            p.drawString(card_x + 40, y, detail)
            y -= 25
            
        # Line separator above footer
        p.setStrokeColorRGB(0.9, 0.9, 0.9)
        p.line(card_x + 30, y + 5, card_x + card_w - 30, y + 5)
            
        # Footer
        y -= 20
        p.setFillColor(colors.black)
        thank_you = "Thank you for choosing "
        
        footer_text_width = p.stringWidth(thank_you, "Helvetica", 12) + p.stringWidth("Carbon Craft Studio!", "Helvetica-Bold", 12)
        footer_x = card_x + (card_w - footer_text_width) / 2
        
        p.drawString(footer_x, y, thank_you)
        
        thank_you_width = p.stringWidth(thank_you, "Helvetica", 12)
        p.setFillColor(colors.red)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(footer_x + thank_you_width, y, "Carbon Craft Studio!")
            
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()

        # Send email with PDF attachment to the customer
        customer_email = EmailMessage(
            subject="Booking Confirmed - Carbon Craft Studio",
            body="Your service booking has been received! Please find your receipt attached.",
            from_email='carboncraftstudio4@gmail.com',
            to=[instance.email],
        )
        customer_email.attach(f'receipt_{instance.id}.pdf', pdf, 'application/pdf')
        customer_email.send(fail_silently=False)