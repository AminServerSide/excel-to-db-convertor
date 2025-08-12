from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} {self.last_name}"

class CollateralType(models.Model):
    id = models.IntegerField(primary_key=True)
    collateral_type = models.CharField(max_length=100)
    collateral_info = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'collateral_types'

    def __str__(self):
        return self.collateral_type

class Line(models.Model):
    id = models.IntegerField(primary_key=True)
    line_name = models.CharField(max_length=100)
    beneficiary = models.BigIntegerField()
    interest_rate = models.FloatField()
    installment_count = models.IntegerField()
    comission_fee = models.FloatField()
    deposite_rate = models.FloatField()
    collateral_type1 = models.ForeignKey(CollateralType, on_delete=models.SET_NULL, null=True, related_name='line_collateral1')
    collateral_type2 = models.ForeignKey(CollateralType, on_delete=models.SET_NULL, null=True, related_name='line_collateral2')
    collateral_type3 = models.ForeignKey(CollateralType, on_delete=models.SET_NULL, null=True, related_name='line_collateral3')
    leeway = models.IntegerField()
    action1 = models.CharField(max_length=100, null=True, blank=True)
    action2 = models.CharField(max_length=100, null=True, blank=True)
    action3 = models.CharField(max_length=100, null=True, blank=True)
    action4 = models.CharField(max_length=100, null=True, blank=True)
    action5 = models.CharField(max_length=100, null=True, blank=True)
    action6 = models.CharField(max_length=100, null=True, blank=True)
    action7 = models.CharField(max_length=100, null=True, blank=True)
    action8 = models.CharField(max_length=100, null=True, blank=True)
    action9 = models.CharField(max_length=100, null=True, blank=True)
    action10 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'lines'

    def __str__(self):
        return self.line_name

class Guarantee(models.Model):
    id = models.IntegerField(primary_key=True)
    guarantee_number = models.CharField(max_length=50)
    issue_gregorian_date = models.CharField(max_length=20, null=True, blank=True)
    issue_shamsi_date = models.CharField(max_length=20)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)

    class Meta:
        db_table = 'guarantees'

    def __str__(self):
        return self.guarantee_number

class Loan(models.Model):
    id = models.IntegerField(primary_key=True)
    guarantee = models.ForeignKey(Guarantee, on_delete=models.CASCADE)
    loan_number = models.CharField(max_length=50)
    loan_amount = models.BigIntegerField()
    issue_date = models.CharField(max_length=20)
    comission_amount = models.BigIntegerField()
    deposite_amount = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans_user1')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loans_user2')
    user3 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loans_user3')
    collateral = models.ForeignKey('Cheque', on_delete=models.SET_NULL, null=True, blank=True, related_name='loans_collateral1')
    collateral2 = models.ForeignKey('Cheque', on_delete=models.SET_NULL, null=True, blank=True, related_name='loans_collateral2')
    collateral3 = models.ForeignKey('Cheque', on_delete=models.SET_NULL, null=True, blank=True, related_name='loans_collateral3')

    class Meta:
        db_table = 'loans'

    def __str__(self):
        return self.loan_number

class Cheque(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    sayadi_id = models.BigIntegerField(null=True, blank=True)
    cheque_date = models.CharField(max_length=20, null=True, blank=True)
    cheque_amount = models.BigIntegerField(null=True, blank=True)
    holder = models.CharField(max_length=100, null=True, blank=True)
    transfer_date = models.CharField(max_length=20, null=True, blank=True)
    sayad_transfer = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'cheques'

    def __str__(self):
        return f"Cheque {self.id}"

class ChequeStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE)
    cheque_status = models.CharField(max_length=50)
    inquiry_date = models.CharField(max_length=20)

    class Meta:
        db_table = 'cheque_statuses'

    def __str__(self):
        return f"{self.cheque} - {self.cheque_status}"