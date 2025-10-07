from rest_framework import generics, permissions, status
def post(self, request, show_id):
show = get_object_or_404(Show, pk=show_id)
serializer = CreateBookingSerializer(data=request.data, context={'show': show})
serializer.is_valid(raise_exception=True)
seat_number = serializer.validated_data['seat_number']


# Transactional booking with retry for concurrency
try:
with transaction.atomic():
# Lock bookings related to this show to prevent race conditions
# We will count currently active booked seats and verify seat availability
# Check if seat already booked (status='booked')
existing = Booking.objects.select_for_update().filter(
show=show,
seat_number=seat_number,
status='booked'
).first()
if existing:
return Response({'detail': 'Seat already booked.'}, status=status.HTTP_400_BAD_REQUEST)


# Check total booked seats < total_seats
current_booked = Booking.objects.select_for_update().filter(show=show, status='booked').count()
if current_booked >= show.total_seats:
return Response({'detail': 'Show is fully booked.'}, status=status.HTTP_400_BAD_REQUEST)


# Create booking
booking = Booking.objects.create(
user=request.user,
show=show,
seat_number=seat_number,
status='booked'
)
except IntegrityError:
# unique_together at DB-level may trigger here; return friendly message
return Response({'detail': 'Could not create booking due to concurrency. Try again.'}, status=status.HTTP_409_CONFLICT)


response_ser = BookingSerializer(booking)
return Response(response_ser.data, status=status.HTTP_201_CREATED)


# Cancel booking
class CancelBookingView(APIView):
permission_classes = [permissions.IsAuthenticated]


def post(self, request, booking_id):
booking = get_object_or_404(Booking, pk=booking_id)
# Security: user cannot cancel another user's booking
if booking.user != request.user:
return Response({'detail': 'You cannot cancel another user\'s booking.'}, status=status.HTTP_403_FORBIDDEN)
if booking.status == 'cancelled':
return Response({'detail': 'Booking already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
booking.status = 'cancelled'
booking.save()
return Response({'detail': 'Booking cancelled.'}, status=status.HTTP_200_OK)


# My bookings
class MyBookingsView(generics.ListAPIView):
serializer_class = BookingSerializer
permission_classes = [permissions.IsAuthenticated]


def get_queryset(self):
return Booking.objects.filter(user=self.request.user).order_by('-created_at')
