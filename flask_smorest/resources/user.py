from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import UserSchema
from db import db
from models import UserModel
from passlib.hash import pbkdf2_sha256
from flask_wt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST


blp = Blueprint("users", __name__, description="Operacoes nos users." )

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(400, message="Um usuario com esse nome ja existe")

        user = UserModel(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()

        return {"message": "Usuario criado com sucesso."}, 201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.passqord):
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {"access_token": access_token, "refresh_token":refresh_token}

        abort(401, message="Credenciais invalidas.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Logout feito com sucesso"}
    

@blp.route("/user/<int:user_id>")
class User(MethodView):
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario deletado"} , 200