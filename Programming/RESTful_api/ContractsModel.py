from init import db, ma


class ContractsModel(db.Model):
    CONTRACTS_LIMIT = 5

    id = db.Column(db.Integer, primary_key=True)
    freelancer_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)


class ContractSchema(ma.Schema):
    class Meta:
        fields = ('id', 'freelancer_id', 'user_id', 'description')
