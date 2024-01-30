import threading
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BookingTable, Customer, Product
from .serializers import CustomerSerializer, ProductSerializer  
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import smtplib
from django.core.mail import send_mail


class RegisterCustomerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginCustomerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')       
        cus = Customer.objects.filter(email=email).first()

        if cus and check_password(password, cus.password):
            print(cus.first_name)
            return Response({'message': 'Login successful', 'first_name': cus.first_name, 'uid': cus.id}, status=status.HTTP_200_OK)
            # return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid!!!'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductListView(ListView):
    model = Product
    # template_name = 'product_list.html'  

    
class ProductByCategoryView(APIView):
    def get(self, request, category, format=None):
        try:
            products = Product.objects.filter(category=category)
            if not products.exists():
                return JsonResponse({'error': f'No products found for category: {category}'}, status=404)
            
            serializer = ProductSerializer(products, many=True)
            return JsonResponse({'products': serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class ProductDetailsView(APIView):
    def get(self, request, product_id, format=None):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return JsonResponse({'product': serializer.data}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class BookingsView(View):
    def send_email_async(self, subject, text_content, html_content, from_email, recipient_list):
        try:
            # Send the email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list,
            )
            # Attach the HTML version of the email content
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
        except Exception as e:
            print(f"Email sending error: {e}")

    def post(self, request, product_id, customer_id, format=None):
        try:
            product = get_object_or_404(Product, id=product_id)
            serializer = ProductSerializer(product)
            product.quantity -= 1
            product.save()

            booking = BookingTable.objects.create(
                customer_id=customer_id,
                product_id=product_id,
                price=product.price,
            )

            customer = get_object_or_404(Customer, id=customer_id)
            subject = 'Order Details'
            recipient_list = [customer.email]
            # Render the email content as an HTML template
            html_content = render_to_string('booking_receipt.html', {
                'oid': booking.id,
                'product': product,
                'price': product.price,
            })
            # Strip the HTML tags to generate a plain text version of the email content
            text_content = strip_tags(html_content)

            # Create a separate thread to send the email asynchronously
            email_thread = threading.Thread(
                target=self.send_email_async,
                args=(subject, text_content, html_content, settings.EMAIL_HOST_USER, recipient_list)
            )
            email_thread.start()

            return JsonResponse({'product': serializer.data, 'booking_id': booking.id}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

# class Getbookings(APIView):
#     def get(self, request, customer_id,product_id, format=None):
#         try:
#             customer = get_object_or_404(Customer, id=customer_id)
#             product = Product.objects.get(id=product_id)
#             # serializer = ProductSerializer(product)
#             booking=BookingTable.objects.get(customer_id=customer_id)
#             return JsonResponse({'bookings': booking}, status=200)
#         except Product.DoesNotExist:
#             return JsonResponse({'error': 'Bookings not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
        


class GetBookings(View):
    def get(self, request, customer_id, format=None):
        try:
            customer = Customer.objects.get(id=customer_id)
            bookings = BookingTable.objects.filter(customer_id=customer_id)

            if not bookings.exists():
                return JsonResponse({'error': 'Booking not found for the customer'}, status=404)

            booking_data = []
            for booking in bookings:
                # Assuming BookingTable has a ForeignKey to Product named product
                product_name = booking.product.name if booking.product else 'N/A'

                booking_data.append({
                    'booking_id': booking.id,
                    'details': {
                        'customer_name': customer.first_name,
                        'product_name': product_name,
                        'price': booking.price,
                        'created_at': booking.created_at,
                        'user_id':customer_id,
                        'product_id': booking.product_id,
                    },
                })

            return JsonResponse({'bookings': booking_data}, status=200)

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
