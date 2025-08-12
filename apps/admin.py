from django.contrib import admin
from .models import User, Line, Guarantee, Loan, CollateralType, Cheque, ChequeStatus

admin.site.register(User)
admin.site.register(Line)
admin.site.register(Guarantee)
admin.site.register(Loan)
admin.site.register(CollateralType)
admin.site.register(Cheque)
admin.site.register(ChequeStatus)