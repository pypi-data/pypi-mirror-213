import typing as t
from flask.views import View, MethodView
from flask import render_template, redirect

class FView(View):

    @staticmethod
    def render(*args, **kwargs):
        return render_template(*args, **kwargs)

    @staticmethod
    def redirect(*args, **kwargs):
        return redirect(*args, **kwargs)

class FMethodView(MethodView):

    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)

    @staticmethod
    def render(*args, **kwargs):
        return render_template(*args, **kwargs)

    @staticmethod
    def redirect(*args, **kwargs):
        return redirect(*args, **kwargs)
