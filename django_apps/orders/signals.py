# orders/signals.py
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
from orders.models import Order

@receiver(post_save, sender=Order)
def send_order_alert(sender, instance, created, **kwargs):
    if created:  # Only send if a NEW order was created, not an update
        subject = f"New Order Alert: Carbon Craft Studio #{instance.id}"
        message = (
            f"You have a new order!\n\n"
            f"Customer: {instance.first_name} {instance.last_name}\n"
            f"Service: {instance.product.product}\n"
            f"Amount: Rs. {instance.total_price}\n"
            f"Category: {instance.product.type}\n"
            f"Address: {instance.address}\n"
            f"City: {instance.city}\n"
            f"Check the admin panel for more details."
        )
        
        send_mail(
            subject,
            message,
            'carboncraftstudio4@gmail.com', # From Email
            ['carboncraftstudio4@gmail.com'], # To Email (Your Admin Email)
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
        p.drawString(card_x + 30 + title_width, card_y + card_h - 40, "- Order Receipt")
        
        # Line separator under header
        p.setStrokeColorRGB(0.9, 0.9, 0.9)
        p.line(card_x + 30, card_y + card_h - 55, card_x + card_w - 30, card_y + card_h - 55)
        
        # Details text
        p.setFont("Helvetica", 12)
        y = card_y + card_h - 85
        details = [
            f"Order ID: #{instance.id}",
            f"Customer Name: {instance.first_name} {instance.last_name}",
            f"Product: {instance.product.product}",
            f"Amount: Rs. {instance.total_price}",
            f"Category: {instance.product.type}",
            f"Phone: {instance.phone}",
            f"Address: {instance.address}",
            f"City: {instance.city}",
            f"Quantity :{instance.quantity}"
        ]
        
        p.setFillColor(colors.black)
        for detail in details:
            p.drawString(card_x + 40, y, detail)
            y -= 25
            
        # Draw Product Image on the right if available
        if instance.product.photo:
            try:
                img_path = instance.product.photo.path
                if os.path.exists(img_path):
                    img_w = 160
                    img_h = 160
                    img_x = card_x + card_w - img_w - 30
                    img_y = card_y + card_h - 75 - img_h
                    
                    p.saveState()
                    # Create a rounded rectangle path for clipping
                    path = p.beginPath()
                    path.roundRect(img_x, img_y, img_w, img_h, 10)
                    p.clipPath(path, stroke=0, fill=0)
                    
                    # Draw the image
                    p.drawImage(img_path, img_x, img_y, width=img_w, height=img_h, preserveAspectRatio=True, anchor='c')
                    p.restoreState()
                    
                    # Draw a subtle border around the image
                    p.setStrokeColorRGB(0.9, 0.9, 0.9)
                    p.roundRect(img_x, img_y, img_w, img_h, 10, fill=0, stroke=1)
            except Exception as e:
                print("Could not draw product image:", e)
                
        # Line separator above footer
        p.setStrokeColorRGB(0.9, 0.9, 0.9)
        # Adjust Y coordinate for footer separator based on whichever is lower: text or image
        footer_sep_y = min(y + 5, card_y + card_h - 75 - 160 - 20) if instance.product.photo else y + 5
        p.line(card_x + 30, footer_sep_y, card_x + card_w - 30, footer_sep_y)
            
        # Footer
        y = footer_sep_y - 20
        p.setFillColor(colors.black)
        thank_you = "Thank you for shopping at "
        
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
            subject="Order Confirmed - Carbon Craft Studio",
            body="Your Order request has been received! contact us on 0300-4433490 for tracking\n\nPlease find your receipt attached.",
            from_email='carboncraftstudio4@gmail.com',
            to=[instance.email],
        )
        customer_email.attach(f'order_receipt_{instance.id}.pdf', pdf, 'application/pdf')
        customer_email.send(fail_silently=False)