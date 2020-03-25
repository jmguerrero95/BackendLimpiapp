import json
#from django.conf import settings
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
#from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import user
from .models import admin
from .models import auxi
from .models import skills
from .models import tipo_mod
from .models import agendado
from .models import fecha_agenda
from .serializer import userSerializer
from .serializer import adminSerializer
from .serializer import auxiSerializer
from .serializer import loginSerializer
from .serializer import skillsSerializer
from .serializer import tipo_modSerializer
from .serializer import agendadoSerializer
from .serializer import fechaSerializer
#from .serializer import fecha_filterSerializer
from .serializer import auxiliaresSerializer
from .serializer import guardarAgendSerializer
from rest_framework.response import Response
#from rest_framework.decorators import action
from .my_app import MyPaginationMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.renderers import TemplateHTMLRenderer


def send_emailCreateUser(request):
    email = request.data.get('user_email')
    context = {
        'usuario': request.data.get('user_email'), 
        'clave': request.data.get('password'), 
    }

    msg_html = render_to_string('index.html',context)
    email = EmailMessage(
        subject='Creación de usuario',
        body=msg_html,
        to=[email])
    email.content_subtype='html'
    email.send()


def send_emailCreateUserAgend(request, admins, client, auxi, fechas, correo):
    context = {
        'cliente': client, 
        'auxiliar': auxi,
        'fechas': fechas,
    }
    msg_html1 = render_to_string('servicio-agendado-cliente.html',context)
    msg_html2 = render_to_string('servicio-agendado-admin.html',context)
    email = EmailMessage(
        subject='Aviso de agendamiento',
        body=msg_html1,
        to=[correo])
    email.content_subtype='html'
    email.send()
    #email2 = EmailMessage(
    #    subject='Mensaje de prueba',
    #    body=msg_html,
    #    to=['josemanuelguerreroduarte@gmail.com'])
    #email2.content_subtype='html'
    #email2.send()
    datos = list()
    for item in admins:
        datos.append(item.user_email)
    print(datos)
    email3 = EmailMessage(
        subject='Aviso de agendamiento',
        body=msg_html2,
        to=datos)
    email3.content_subtype='html'
    email3.send()


def send_emailApro(request, admins, client, auxi, fechas, email_clien, email_aux):
    context = {
        'cliente': client, 
        'auxiliar': auxi,
        'fechas': fechas,
    }
    msg_html1 = render_to_string('servicio-agendado-cliente-apro.html',context)
    msg_html2 = render_to_string('servicio-agendado-admin-apro.html',context)
    msg_html3 = render_to_string('servicio-agendado-aux.html',context)
    email = EmailMessage(
        subject='Aprobación de agenda',
        body=msg_html1,
        to=[email_clien])
    email.content_subtype='html'
    email.send()
    email2 = EmailMessage(
        subject='Aprobación de agenda',
        body=msg_html3,
        to=[email_aux])
    email2.content_subtype='html'
    email2.send()
    datos = list()
    for item in admins:
        datos.append(item.user_email)
    print(datos)
    email3 = EmailMessage(
        subject='Aprobación de agenda',
        body=msg_html2,
        to=datos)
    email3.content_subtype='html'
    email3.send()


def send_emailDene(request, admins, client, auxi, fechas, email_clien, email_aux):
    context = {
        'cliente': client, 
        'auxiliar': auxi,
        'fechas': fechas,
    }
    msg_html1 = render_to_string('servicio-agendado-cliente-dene.html',context)
    msg_html2 = render_to_string('servicio-agendado-admin-dene.html',context)
    email = EmailMessage(
        subject='Denegación de agenda',
        body=msg_html1,
        to=[email_clien])
    email.content_subtype='html'
    email.send()
    #email2 = EmailMessage(
    #    subject='Mensaje de prueba',
    #    body=msg_html,
    #    to=['josemanuelguerreroduarte@gmail.com'])
    #email2.content_subtype='html'
    #email2.send()
    datos = list()
    for item in admins:
        datos.append(item.user_email)
    print(datos)
    email3 = EmailMessage(
        subject='Denegación de agenda',
        body=msg_html2,
        to=datos)
    email3.content_subtype='html'
    email3.send()


def send_emailRecu(request, passw):
    email = list()
    email.append(request.data.get('email'))
    context = {
        'email': request.data.get('email'),
        'pass': passw, 
    }

    msg_html = render_to_string('recover-pass.html',context)
    email = EmailMessage(
        subject='Recuperación de password',
        body=msg_html,
        to=email)
    email.content_subtype='html'
    email.send()


class userViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = userSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['ident']

    def create(self, request, *args, **kwargs):
        response = super(userViewSet, self).create(request, *args, **kwargs)
        print(response)
        send_emailCreateUser(request)
        return response


class recuperar(viewsets.ModelViewSet):
    queryset = user.objects.all()

    def create(self, request, *args, **kwargs):
        queryset = user.objects.all()
        email = request.data.get('email')
        print(email)
        dats = list(queryset.filter(user_email=email))
        print(dats)
        password = dats[0].password
        send_emailRecu(request, password)
        return Response(status=status.HTTP_204_NO_CONTENT)


class recuperardo(viewsets.ModelViewSet):
    queryset = user.objects.all()

    def create(self, request, *args, **kwargs):
        queryset = user.objects.all()
        email = request.data.get('email')
        dats = list(queryset.filter(user_email=email))
        print(dats)
        password = dats[0].password
        send_emailRecu(request, password)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BasicPagination(PageNumberPagination):
    page_size = 100


class adminViewSet(viewsets.ModelViewSet):
    queryset = admin.objects.all()
    serializer_class = adminSerializer


class auxiViewSet(viewsets.ModelViewSet):
    queryset = auxi.objects.all()
    serializer_class = auxiSerializer


class skillsViewSet(viewsets.ModelViewSet):
    queryset = skills.objects.all()
    serializer_class = skillsSerializer

    def delete(self, request, *args, **kwargs):
        id_user = self.request.query_params.get('id_user')
        queryset = skills.objects.all()
        skill = queryset.filter(id_user=id_user)
        #skill = self.get_object(id_user=id_user)
        #skill.delete()
        self.perform_destroy(skill)
        return Response(status=status.HTTP_204_NO_CONTENT)


class tipo_modViewSet(viewsets.ModelViewSet):
    queryset = tipo_mod.objects.all()
    serializer_class = tipo_modSerializer

    def delete(self, request, *args, **kwargs):
        id_user = request.query_params.get('id_user')
        queryset = tipo_mod.objects.all()
        mod = queryset.filter(id_user=id_user)
        #skill = self.get_object(id_user=id_user)
        #skill.delete()
        self.perform_destroy(mod)
        return Response(status=status.HTTP_204_NO_CONTENT)


class agend_ViewSet(viewsets.ModelViewSet):
    queryset = agendado.objects.all()
    serializer_class = guardarAgendSerializer

    def create(self, request, *args, **kwargs):
        fechas = self.request.query_params.get('fechas')
        fechas = json.dumps(fechas).replace('[', '')
        fechas = fechas.replace(']', '')
        fechas = fechas.replace('"', '')
        fechas = fechas.replace('\\', '')
        fechas = fechas.replace(',', ', ')

        response = super(agend_ViewSet, self).create(request, *args, **kwargs)
        queryset2 = user.objects.all()
        queryset3 = fecha_agenda.objects.all()
        users = list(queryset2.filter(id=self.request.data.get('id_user')))
        auxi =  list(queryset2.filter(id=self.request.data.get('id_auxi')))
        print(self.request.data.get('id'))
        client=users[0].firs_name
        correo=users[0].user_email
        auxi=auxi[0].firs_name
        queryset2 = list(queryset2.filter(tipo=3))
        send_emailCreateUserAgend(self, queryset2, client, auxi, fechas, correo)
        return response

    def perform_update(self, serializer):
        queryset4 = agendado.objects.all()
        user_instance = serializer.instance
        request = self.request
        serializer.save()
        if(request.data.get('realizado') == '1'):
            print("bien")
        else:
            queryset2 = user.objects.all()
            dats = user.objects.all()
            dats = list(dats.filter(tipo=3))
            queryset3 = fecha_agenda.objects.all()
            agend = list(queryset4.filter(id=request.query_params.get('id')))
            users = list(queryset2.filter(id=agend[0].id_user.id))
            auxi = list(queryset2.filter(id=agend[0].id_auxi.id))
            fecha = list(queryset3.filter(grupo=agend[0].id))
            client = users[0].firs_name
            email_clien = users[0].user_email
            email_aux = auxi[0].user_email
            auxi = auxi[0].firs_name
            print(agend[0].id)
            fechas = fecha[0].fecha
            num = agend[0].estado
            print(num)
            if(num != 0 and num != 1 and num == '2'):
                send_emailApro(self, dats, client, auxi, fechas, email_clien, email_aux)
                #send_emailAux(self, dats, client, auxi, fechas)
            else:
                send_emailDene(self, dats, client, auxi, fechas, email_clien, email_aux)
            #if(request.data.get('realizado')==1):
            #    send_emailTerm(self, queryset2, client, auxi, fechas)
        return Response(status=status.HTTP_200_OK)



class consul_agendClien(APIView, MyPaginationMixin):
    pagination_class = BasicPagination
    serializer_class = agendadoSerializer
    def get(self, request, format=None, *args, **kwargs):
        dat = agendado.objects.all().prefetch_related('id_auxi')
        if self.request.query_params.get('id'):#consulta de agenda para un cliente
            id = self.request.query_params.get('id')
            if self.request.query_params.get('hecho'):
                dat = dat.filter(id_user=id)
                dat = dat.filter(estado=2)
                dat = self.paginate_queryset(dat.filter(realizado=1))
                if dat is not None:
                    #serializer = agendadoSerializer(dat, many=True)
                    #serializer2 = serializer.data
                    serializer = self.get_paginated_response(self.serializer_class(dat, many=True).data)
                else:
                    serializer = self.serializer_class(dat, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                dat = dat.filter(id_user=id)
                dat = dat.filter(realizado=0)
                self.paginate_queryset(dat)
                if dat is not None:
                    serializer = self.get_paginated_response(self.serializer_class(dat, many=True).data)
                else:
                    serializer = self.serializer_class(dat, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        #dat = agendado.objects.all().prefetch_related('id_auxi')
        #serializer = agendadoSerializer(dat, many=True)
        #serializer2 = serializer.data
        #return Response(serializer2)



class consul_agend(APIView, MyPaginationMixin):
    pagination_class = BasicPagination
    serializer_class = agendadoSerializer
    def get(self, request, format=None, *args, **kwargs):
        dat = agendado.objects.all().prefetch_related('id_auxi')
        if self.request.query_params.get('estado'):#consulta de adminitrador para aprobar agenda
            estado = self.request.query_params.get('estado')
            dat = dat.filter(estado=1)
            dat = self.paginate_queryset(dat)
            if dat is not None:
                #serializer = agendadoSerializer(dat, many=True)
                #serializer2 = serializer.data
                #return Response(serializer2)
                serializer = self.get_paginated_response(self.serializer_class(dat, many=True).data)
            else:
                serializer = self.serializer_class(dat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)




        if self.request.query_params.get('realizado'):#consulta de historial de agendas anteriores
            realizado = self.request.query_params.get('realizado')
            print(realizado)
            dat = self.paginate_queryset(dat.filter(realizado=realizado))
            if dat is not None:
                #serializer = agendadoSerializer(dat, many=True)
                #serializer2 = serializer.data
                serializer = self.get_paginated_response(self.serializer_class(dat, many=True).data)
            else:
                serializer = self.serializer_class(dat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



        if self.request.query_params.get('id'):#consulta de agenda para un auxiliar
            id = self.request.query_params.get('id')
            if self.request.query_params.get('hecho'):
                dat = dat.filter(id_auxi=id)
                dat = dat.filter(estado=2)
                dat = dat.filter(realizado=1)
                dat = self.paginate_queryset(dat)
                if dat is not None:
                    #serializer = agendadoSerializer(dat, many=True)
                    #serializer2 = serializer.data
                    serializer = self.get_paginated_response(self.serializer_class(dat, many=True).data)
                else:
                    serializer = self.serializer_class(dat, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                dat = dat.filter(id_auxi=id)
                dat = dat.filter(estado=2)
                dat = dat.filter(realizado=0)
                self.paginate_queryset(dat)
                if dat is not None:
                    serializer = self.get_paginated_response(self.serializer_class(dat, many=True).data)
                else:
                    serializer = self.serializer_class(dat, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        #dat = agendado.objects.all().prefetch_related('id_auxi')
        #serializer = agendadoSerializer(dat, many=True)
        #serializer2 = serializer.data
        #return Response(serializer2)


class consul_agendAuxi(APIView):
    def get(self, request):
        dat = agendado.objects.all().prefetch_related('id_auxi')
        if self.request.query_params.get('estado')==1:#consulta de adminitrador para aprobar agenda
            estado = self.request.query_params.get('estado')
            dat = dat.filter(estado=1)
            serializer = agendadoSerializer(dat, many=True)
            serializer2 = serializer.data
            return Response(serializer2)
        if self.request.query_params.get('realizado')==1:#consulta de historial de agendas anteriores
            realizado = self.request.query_params.get('realizado')
            print(realizado)
            dat = dat.filter(realizado=realizado)
            serializer = agendadoSerializer(dat, many=True)
            serializer2 = serializer.data
            return Response(serializer2)
        if self.request.query_params.get('id'):#consulta de agenda para un auxiliar
            id = self.request.query_params.get('id')
            dat = dat.filter(id_auxi=id)
            dat = dat.filter(estado=2)
            dat = dat-filter(realizado=0)
            serializer = agendadoSerializer(dat, many=True)
            serializer2 = serializer.data
            return Response(serializer2)

        #dat = dat.filter()
        #serializer = agendadoSerializer(dat, many=True)
        #serializer2 = serializer.data
        #jsons = json.dumps(dat)
        #return Response(serializer2)
        #queryset2 = agendado.objects.all()
        #queryset3 = fecha_agenda.objects.all()



class fecha_ViewSet2(viewsets.ModelViewSet):
    queryset = fecha_agenda.objects.all()
    serializer_class = fechaSerializer


class fecha_ViewSet(APIView):
    def get(self, request):
        queryset = fecha_agenda.objects.all()
        id_agenda = self.request.query_params.get('id_agenda')
        fechas = queryset.filter(grupo=id_agenda)
        serializer = fechaSerializer(fechas, many=True)
        serializer2 = serializer.data
        return Response(serializer2)


class skills_filter(APIView):
    def get(self, request):
        queryset = skills.objects.all()
        id = self.request.query_params.get('id')
        #serializer_class = loginSerializer
        if queryset.filter(id_user=id):
            datos = queryset.filter(id_user=id)
            serializer = skillsSerializer(datos, many=True)
            serializer2 = serializer.data
            return Response(serializer2)
        else:
            return Response(False)


class user2ViewSet(APIView):
    def get(self, request):
        queryset = user.objects.all()
        serializer_class = userSerializer

#envio las fechas a agendar, luego con esas fechas consulto las agendas que la usan y de cada agenda ids 
class agenda_filter(APIView):
    def get(self, request):
        fechas = self.request.query_params.get('fechas')
        modalidad = self.request.query_params.get('modalidad')
        list_fecha = json.loads(fechas)
        lista = []
        lista_auxi = []
        dat_auxi2 = []
        dat_auxi = []
        anterior = ''
        for fecha in list_fecha:
            queryset2 = fecha_agenda.objects.all()
            if queryset2.filter(fecha=fecha).exists():
                datos_fecha = list(queryset2.filter(fecha=fecha).only('grupo'))
                #lista.append(datos_fecha[0])
                for elem_lista in datos_fecha:
                    queryset3 = agendado.objects.all()
                    queryset3 = queryset3.filter(id=elem_lista.grupo.id)
                    queryset3 = queryset3.exclude(realizado=1)
                    queryset3 = queryset3.exclude(estado=0)
                    agend = list(queryset3)
                    print(agend)
                    lista_auxi.append(agend)
                for datos in lista_auxi:
                    if(datos):
                        print(datos)
                        queryset4 = user.objects.all()
                        auxiliar = list(queryset4.filter(id=datos[0].id_auxi.id).only('id'))
                        dat_auxi.append(auxiliar[0].id)
        dat_auxi = list(set(dat_auxi))
        #auxiliar = auxiliar.filter(tipo=2)
        #for elemens in dat_auxi:
            #print (elemens)
        queryset4 = user.objects.all()
        final = queryset4.filter(tipo=2).exclude(id__in=dat_auxi)
        final = final.filter(this_mod__modalidad=modalidad)
        serializer = userSerializer(final, many=True)
        serializer2 = serializer.data
        dat_auxi2.append(serializer2)
                    #if anterior == serializer2:
                    #    False
                    #else:
                    #    dat_auxi2.append(serializer2)
                    #    anterior = serializer2
        if dat_auxi2:
            return Response(dat_auxi2)
            #return Response(JSONRenderer().render(dat_auxi))
        else:
            queryset4 = user.objects.all()
            auxiliar = queryset4.filter(tipo=2)
            auxiliar = auxiliar.filter(this_mod__modalidad=modalidad)
            print(modalidad)
            serializer = userSerializer(auxiliar, many=True)
            serializer2 = serializer.data
            dat_auxi2.append(serializer2)
            return Response(dat_auxi2)





class loginAPI(APIView):
    def post(self, request):
        queryset = user.objects.all()
        #serializer_class = loginSerializer
        email = request.data['user_email']
        passw = request.data['password']
        if queryset.filter(user_email=email):
            queryset=queryset.filter(user_email=email)
            if queryset.filter(password=passw):
                datos = queryset.filter(user_email=email)
                serializer = loginSerializer(datos, many=True)
                serializer2 = serializer.data
                return Response(JSONRenderer().render(serializer2[0]))
            else:
                return Response(False)
        else:
            return Response(False)


class auxi_filter(APIView):
    def get(self, request):
        queryset = user.objects.all()
        #serializer_class = loginSerializer
        aux = 2
        if queryset.filter(tipo=aux):
            datos = queryset.filter(tipo=aux)
            serializer = userSerializer(datos, many=True)
            serializer2 = serializer.data
            return Response(serializer2)
        else:
            return Response(False)
        #serializer_class = login
        # if queryset[0] == "josemanuelguerreroduarte@gmail.com":
        #    return Response("bien")
        # else:
        #    return Response("mal")
    #    serializer = login().Meta(request.data)
    #    if serializer==True:
    #        return Response("Bien")
    #    else:
    #        return Response(
    #            "serializer"
    #        )
# class userViewSet2(viewsets.ModelViewSet):
#    @action(detail=True, methods=['POST'])
#    def test(self, request):
#        return Response("hola")
    # def email(self, request):
    #    queryset = "hola"
    #    if request.method == 'POST':
    #        serializer_class = login
    #queryset = user.objects.all()
    #serializer_class = login
    # if request.method == 'POST':
    #    queryset="hola"
