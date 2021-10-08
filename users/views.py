import json, re, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from users.models   import User
from my_settings    import SECRET_KEY, ALGORITHM



class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({'message': 'ERROR_ID_ALREADY_EXIST'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'ERROR_ID_ALREADY_EXIST'}, status=400)
            
            if not re.match(r"^(a-z)[0-9]{4,16}$", data['user_id']):
                return JsonResponse({'message': 'INVALID_ID'}, status=404)

            if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=404)
            
            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", data["password"]):
                return JsonResponse({"message": "INVALID_PASSWORD)"}, status=404)

            User.objects.create(
                    user_id  = data['user_id'],
                    password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8'),
                    name     = data['name'],
                    mobile   = data['mobile'],
                    email    = data['email'],
                    birthday = data['birthday'],
            )

            return JsonResponse({'message': 'SUCCESS'})

        except:
            return JsonResponse({'message': 'KEY_ERROR'})

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({'message': 'INVALID_USER_ID'}, status=401)
            
            user = User.objects.get(user_id=data['user_id'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'token':token}, status=200)
                
            return JsonResponse({'message': 'INVALID_USER_PASSWORD'}, status=401)

        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)