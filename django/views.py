from .models import Users
from django.contrib.auth.models import UserInfo
from django.views.generic.edit import FormView


class TransferView(FormView):
    
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['userlist'] = self.userlist()

        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['userlist'] = self.userlist()

        amount = float(request.POST['amount'])

        user_from = UserInfo.objects.get(id=request.POST['user_from'])
        
        # ищем сумму на счёте пользователя
        # Нужно искать первую достаточную сумму
        us = user_from.users_set.all()

        if us:
            # Почему только первый акк? Если нужно только первый можно исп .first()
            # Лучше выбрать акк с максимальной суммой или размещать в табл акк в
            # порядке уменьшения суммы --> .first() это акк с самой большой суммой
            acc_sum = us[0].account

            inn_to = Users.objects.filter(inn=request.POST['inn_to'])
            # Здесь надо проверить есть ли inn_to?в

            if inn_to and acc_sum >= amount:
                users_count = len(inn_to)
                sum_part = round(amount / users_count, 2)

                # со счёта донора списать всю сумму
                res_user = user_from.users_set.get()
                result_sum = float(res_user.account) - sum_part * users_count
                res_user.account = result_sum
                res_user.save()

                # на счёт каждого записать по части
                for i in inn_to:
                    result_sum = float(i.account) + sum_part
                    i.account = result_sum
                    i.save()

                ctx['op_result'] = [acc_sum, users_count, sum_part]
            else:
                ctx['op_result'] = 'перевод не выполнен'

        else:
            ctx['op_result'] = 'На счёте недостаточно средств'

        return self.render_to_response(ctx)

    def userlist(self):
         # Можно сразу заполнять лист как list comprehension
        user_list = []
        for i in UserInfo.objects.all():
            cur_user = {}
            cur_user['id'] = i.id
            cur_user['username'] = i.username
            if i.users_set.all():
                tmp = i.users_set.get()
                cur_user['inn'] = tmp.inn
                cur_user['account'] = tmp.account
            user_list.append(cur_user)

        return user_list
