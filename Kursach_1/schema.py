import graphene
from django.core.exceptions import ValidationError
from graphene_django import DjangoObjectType
from home.models import Events, EventTime, EventImportant, EventImage, Actors, EventActors, Seat, Tickets
from django.contrib.auth.models import User


        #ТБАЛИЦА User#

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'






           #ТАБЛИЦА Tikets#


class SeatType(DjangoObjectType):
    class Meta:
        model = Seat
        fields = '__all__'

    available_seats_count = graphene.Int()

    def resolve_available_seats_count(self, info):
        seats = Seat.objects.filter(status='available')
        return seats.count()


class TicketType(DjangoObjectType):
    class Meta:
        model = Tickets
        fields = '__all__'

# Мутация для создания билетов
class CreateTickets(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        seat_ids = graphene.List(graphene.ID, required=True)

    tickets = graphene.List(TicketType)

    def mutate(self, info, user_id, seat_ids):
        # Получаем пользователя по ID
        user = User.objects.get(id=user_id)

        # Получаем места по ID
        seats = Seat.objects.filter(id__in=seat_ids)

        # Проверяем, что все места доступны
        unavailable_seats = [seat for seat in seats if seat.status != 'available']
        if unavailable_seats:
            raise ValidationError("Some of the selected seats are already booked.")

        # Создаем билеты и обновляем статус мест
        tickets = []
        for seat in seats:
            # Создаем билет
            ticket = Tickets.objects.create(
                user=user,
                seat=seat
            )
            tickets.append(ticket)

            # Обновляем статус места на "booked"
            seat.status = 'booked'
            seat.save()

        return CreateTickets(tickets=tickets)


class CreateSeat(graphene.Mutation):
    class Arguments:
        event_time_id = graphene.String(required=True)
        row_number = graphene.Int(required=True)
        seat_number = graphene.Int(required=True)

    ok = graphene.Boolean()
    seat = graphene.Field(SeatType)

    def mutate(self, info, event_time_id, row_number, seat_number):
        event_time = EventTime.objects.get(id=event_time_id)
        seat = Seat(event_time=event_time, row_number=row_number, seat_number=seat_number)
        seat.save()
        return CreateSeat(ok=True, seat=seat)


class UpdateSeat(graphene.Mutation):
    class Arguments:
        seat_id = graphene.String(required=True)
        is_sold = graphene.Boolean()  # Обновление статуса мест

    seat = graphene.Field(SeatType)

    def mutate(self, info, seat_id, is_sold):
        seat = Seat.objects.get(id=seat_id)
        seat.is_sold = is_sold
        seat.save()
        return UpdateSeat(seat=seat)

class DeleteSeat(graphene.Mutation):
    class Arguments:
        seat_id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, seat_id):
        seat = Seat.objects.get(id=seat_id)
        seat.delete()
        return DeleteSeat(ok=True)


# Мутация для обновления билета
class UpdateTicket(graphene.Mutation):
    class Arguments:
        ticket_id = graphene.String(required=True)
        seat_number = graphene.Int()
        row_number = graphene.Int()
        price = graphene.Float()

    ticket = graphene.Field(TicketType)



    def mutate(self, info, ticket_id, seat_number=None, row_number=None, price=None):
        ticket = Tickets.objects.get(id=ticket_id)
        if seat_number is not None and row_number is not None:
            seat = Seat.objects.filter(
                event_time=ticket.seat.event_time,
                row_number=row_number,
                seat_number=seat_number
            ).first()
            if seat:
                ticket.seat = seat
        if price is not None:
            ticket.price = price
        ticket.save()
        return UpdateTicket(ticket=ticket)


# Мутация для удаления билета
class DeleteTicket(graphene.Mutation):
    class Arguments:
        ticket_id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, ticket_id):
        ticket = Tickets.objects.get(id=ticket_id)
        ticket.delete()
        return DeleteTicket(ok=True)


# Обновление мутации для создания билета с проверкой доступности места
class CreateTicket(graphene.Mutation):
    class Arguments:
        seat_id = graphene.String(required=True)
        price = graphene.Decimal(required=True)

    ticket = graphene.Field(TicketType)
    error_message = graphene.String()

    def mutate(self, info, seat_id, price):
        seat = Seat.objects.get(id=seat_id)
        if seat.is_sold:
            return CreateTicket(ticket=None, error_message="Seat is already sold")

        ticket = Tickets(seat=seat, price=price)
        ticket.save()

        seat.is_sold = True
        seat.save()

        return CreateTicket(ticket=ticket, error_message=None)






          #ТАБЛИЦА EventTime

class EventTimeType(DjangoObjectType):
    class Meta:
        model = EventTime
        fields = '__all__'


    weekday = graphene.String()
    seats = graphene.List(SeatType)
    available_seats_count = graphene.Int()

    def resolve_available_seats_count(self, info):
        seat = self.seats.filter(status='available')
        return seat.count()

    def resolve_seats(self, info):
        return self.seats.all()

    def resolve_weekday(self, info):
        # Здесь `self` — это объект модели EventTime
        return self.weekday

#Создание объекта
class CreateEventTime(graphene.Mutation):
    class Arguments:
        event = graphene.String()
        date = graphene.DateTime()
        price = graphene.Decimal()

    ok = graphene.Boolean()
    eventTime = graphene.Field(EventTimeType)

    def mutate(self, info, event, date, price):
        eventTime = EventTime(event=event, date=date, price=price)
        eventTime.save()
        return CreateEventTime(ok=True, eventTime=eventTime)


#Удаление объекта
class DeleteEventTime(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, id):
        eventTime = EventTime.objects.get(id=id)
        eventTime.delete()
        return DeleteEventTime(ok=True)


#Обновление объекта
class UpdateEventTime(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        event = graphene.String()
        date = graphene.DateTime()
        price = graphene.Decimal()

    ok = graphene.Boolean()
    eventTime = graphene.Field(EventTimeType)

    def mutate(self, info, id, event, date, price):
        eventTime = EventTime.objects.get(id=id)
        eventTime.event = event
        eventTime.date = date
        eventTime.price = price
        eventTime.save()





     #ТАБЛИЦА EventImportant#

class EventImportantType(DjangoObjectType):
    class Meta:
        model = EventImportant
        fields = '__all__'



class EventImageType(DjangoObjectType):
    class Meta:
        model = EventImage
        fields = '__all__'






        # ТАБЛИЦА Actors#

class ActorType(DjangoObjectType):
    class Meta:
        model = Actors
        fields = '__all__'

        # Мутация для создания актера
class CreateActor(graphene.Mutation):
            class Arguments:
                first_name = graphene.String(required=True)
                last_name = graphene.String(required=True)
                image = graphene.String()  # Путь к изображению

            ok = graphene.Boolean()
            actor = graphene.Field(ActorType)

            def mutate(self, info, first_name, last_name, image=None):
                actor = Actors(firstName=first_name, lastName=last_name, image=image)
                actor.save()
                return CreateActor(ok=True, actor=actor)

        # Мутация для обновления актера
class UpdateActor(graphene.Mutation):
            class Arguments:
                actor_id = graphene.String(required=True)
                first_name = graphene.String()
                last_name = graphene.String()
                image = graphene.String()

            ok = graphene.Boolean()
            actor = graphene.Field(ActorType)

            def mutate(self, info, actor_id, first_name=None, last_name=None, image=None):
                actor = Actors.objects.get(id=actor_id)
                if first_name:
                    actor.firstName = first_name
                if last_name:
                    actor.lastName = last_name
                if image:
                    actor.image = image
                actor.save()
                return UpdateActor(ok=True, actor=actor)

        # Мутация для удаления актера
class DeleteActor(graphene.Mutation):
            class Arguments:
                actor_id = graphene.String(required=True)

            ok = graphene.Boolean()

            def mutate(self, info, actor_id):
                actor = Actors.objects.get(id=actor_id)
                actor.delete()
                return DeleteActor(ok=True)





        #ТАБЛИЦА EventActors#

class EventActorType(DjangoObjectType):
            class Meta:
                model = EventActors
                fields = '__all__'

                actors = graphene.List(ActorType)

                def resolve_actors(self, info):
                    return Actors.objects.all()

        # Мутация для создания EventActor
class CreateEventActor(graphene.Mutation):
            class Arguments:
                event_id = graphene.String(required=True)
                actor_id = graphene.String(required=True)
                role = graphene.String()

            event_actor = graphene.Field(EventActorType)

            def mutate(self, info, event_id, actor_id, role=None):
                event = Events.objects.get(id=event_id)
                actor = Actors.objects.get(id=actor_id)
                event_actor = EventActors(event=event, actor=actor, role=role)
                event_actor.save()
                return CreateEventActor(event_actor=event_actor)

        # Мутация для обновления роли EventActor
class UpdateEventActor(graphene.Mutation):
            class Arguments:
                event_actor_id = graphene.String(required=True)
                role = graphene.String()

            event_actor = graphene.Field(EventActorType)

            def mutate(self, info, event_actor_id, role=None):
                event_actor = EventActors.objects.get(id=event_actor_id)
                if role:
                    event_actor.role = role
                event_actor.save()
                return UpdateEventActor(event_actor=event_actor)

        # Мутация для удаления EventActor
class DeleteEventActor(graphene.Mutation):
            class Arguments:
                event_actor_id = graphene.String(required=True)

            ok = graphene.Boolean()

            def mutate(self, info, event_actor_id):
                event_actor = EventActors.objects.get(id=event_actor_id)
                event_actor.delete()
                return DeleteEventActor(ok=True)





        # ТАБЛИЦА Events#

class EventsType(DjangoObjectType):
    class Meta:
        model = Events
        fields = '__all__'

    images = graphene.List(EventImageType)  # Для EventImage
    times = graphene.List(EventTimeType)  # Для EventTime
    important = graphene.Field(EventImportantType)  # Для EventImportant
    actors = graphene.List(EventActorType)


    def resolve_images(self, info):
        return self.images.all()  # Связь через related_name="images"

    def resolve_times(self, info):
        return EventTime.objects.filter(event=self)  # Связь через ForeignKey

    def resolve_important(self, info):
        return getattr(self, 'important', None)  # Связь через OneToOneField

    def resolve_actors(self, info):
        return EventActors.objects.filter(event=self)


# Создание нового объекта
class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        author = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    event = graphene.Field(EventsType)

    def mutate(self, info, name, author, description):
        event = Events(name=name, author=author, description=description)
        event.save()
        return CreateEvent(ok=True, event=event)


# Удаление объекта
class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, id):
        event = Events.objects.get(id=id)
        event.delete()
        return DeleteEvent(ok=True)


# Обновление объекта
class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        author = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    event = graphene.Field(EventsType)

    def mutate(self, info, id, name, author, description):
        event = Events.objects.get(id=id)
        event.name = name
        event.author = author
        event.description = description
        event.save()
        return UpdateEvent(ok=True, event=event)






#Возврат объектов
class Query(graphene.ObjectType):
    events = graphene.List(EventsType, id=graphene.ID())
    event_time = graphene.List(EventTimeType, id=graphene.ID())
    event_important = graphene.List(EventImportantType)
    actors = graphene.List(ActorType)  # Все актеры
    event_actors = graphene.List(EventActorType, event_id=graphene.String())  # Актеры в конкретной постановке
    tickets = graphene.List(TicketType, event_time_id=graphene.String())
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))
    seats = graphene.List(SeatType, event_time_id=graphene.String())

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user_by_id(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def resolve_event_time(self, info, id=None):
        if id:
            return EventTime.objects.filter(id=id)
        return EventTime.objects.all()

    def resolve_events(self, info, id=None):
        if id:
            return Events.objects.filter(id=id)
        return Events.objects.all()

    def resolve_event_important(self, info):
        return EventImportant.objects.all()

    def resolve_actors(self, info):
        return Actors.objects.all()

    def resolve_event_actors(self, info, event_id):
        return EventActors.objects.filter(event__id=event_id)

    def resolve_tickets(self, info, event_time_id):
        # Возвращаем все билеты для конкретного времени спектакля
        return Tickets.objects.filter(event_time__id=event_time_id)

    def resolve_seats(self, info, event_time_id):
        return Seat.objects.filter(event_time__id=event_time_id)




# Добавление мутаций и запросов в схему
class Mutation(graphene.ObjectType):
    # Events
    create_event = CreateEvent.Field()
    delete_event = DeleteEvent.Field()
    update_event = UpdateEvent.Field()

    # EventTime
    create_event_time = CreateEventTime.Field()
    delete_event_time = DeleteEventTime.Field()
    update_event_time = UpdateEventTime.Field()

    # Actors
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    delete_actor = DeleteActor.Field()

    # EventActors
    create_event_actor = CreateEventActor.Field()
    update_event_actor = UpdateEventActor.Field()
    delete_event_actor = DeleteEventActor.Field()

    # Tickets
    create_tickets = CreateTickets.Field()
    update_ticket = UpdateTicket.Field()
    delete_ticket = DeleteTicket.Field()

    #Seats
    create_seat = CreateSeat.Field()
    update_seat = UpdateSeat.Field()
    delete_seat = DeleteSeat.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
