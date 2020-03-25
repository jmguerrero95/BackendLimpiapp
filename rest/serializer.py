from .models import user
from .models import admin
from .models import auxi
from .models import skills
from .models import tipo_mod
from .models import agendado
from .models import fecha_agenda
from rest_framework import serializers
from rest_framework.decorators import APIView
from rest_framework import generics
from rest_framework_jwt.settings import api_settings



#class usercifrSerializer(serializers.ModelSerializer):
#    def get_token(self, object):
#        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#        payload = jwt_payload_handler(object)
#        token = jwt_encode_handler(payload)

#        return token

#    class Meta:
#        model = user
#        fields = ('token', 'id', 'firs_name', 'last_name', 'user_email', 'password', 'tipo')


class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class login(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['user_email', 'password']
        #def __init__(self, data):
            #email = user.objects.filter(data=self.fields[0])
        #    if data['user_email'] == self.fields['user_email'] != 0:
                #passw = user.objects.filter(data=self.fields[1])
        #        if data['password'] == self.fields['password'] != 0:
        #            return True
        #    else:
        #        return None
           # pass
        #fields = ['user_email']
# class login(generics.ListCreateAPIView):
#    def post(self):
#        if self.request.method == 'POST':
#            return "hola"
        #username = request.POST.get('username')
        # return username,
    """def __init__(self, user, password):
        self.user = user
        self.password = password"""


class adminSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin
        fields = '__all__'


class auxiSerializer(serializers.ModelSerializer):
    class Meta:
        model = auxi
        fields = '__all__'


class skillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = skills
        fields = '__all__'


class tipo_modSerializer(serializers.ModelSerializer):
    class Meta:
        model = tipo_mod
        fields = '__all__'


class userSerializer(serializers.ModelSerializer):
    this_skills = skillsSerializer(many=True, read_only=True)
    this_mod = tipo_modSerializer(many=True, read_only=True)
    class Meta:
        model = user
        fields = '__all__'


class fechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = fecha_agenda
        fields = '__all__'


class fecha_filterSerializer(serializers.ModelSerializer):
    class Meta:
        model = fecha_agenda
        fields = ('grupo')


class auxiliaresSerializer(serializers.ModelSerializer):
    this_skills = skillsSerializer(many=True)
    class Meta:
        model = user
        fields = ('id','firs_name','last_name','user_email','tipo','image','ident','userPhone','user_Address','birthDay', 'this_skills')


class agendadoSerializer(serializers.ModelSerializer):
    #id_auxi = userSerializer
    this_agenda = fechaSerializer(many=True)
    #id_auxi = serializers.RelatedField(read_only=True)
    #this_auxi = userSerializer(many=True)
    class Meta:
        model = agendado
        fields = ('id','id_user','modalidad','tipo_servi','hora','id_auxi','pers_Acargo','direccion','observaciones','lugar','estado','realizado','this_agenda')
        depth = 1



class guardarAgendSerializer(serializers.ModelSerializer):
    class Meta:
        model = agendado
        fields = '__all__'
